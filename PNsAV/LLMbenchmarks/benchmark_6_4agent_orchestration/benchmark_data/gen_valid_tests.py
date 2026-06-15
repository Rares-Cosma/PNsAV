import xml.etree.ElementTree as ET
import json
import os
import glob

def argmicro_to_aspic(xml_filepath):
    tree = ET.parse(xml_filepath)
    root = tree.getroot()

    atoms = []
    rules = []
    arguments = []
    attacks = []

    # 1. Parse Nodes (EDUs)
    nodes = {}
    for edu in root.findall(".//edu"):
        node_id = edu.get("id")
        text = edu.text.strip() if edu.text else ""
        nodes[node_id] = text

    # 2. Extract Edge Topology
    support_edges = []
    add_links = {}
    rebuttals = []
    undercuts = []

    for edge in root.findall(".//edge"):
        etype = edge.get("type")
        src = edge.get("src")
        trg = edge.get("trg")
        eid = edge.get("id")

        if etype == "sup":
            support_edges.append({"eid": eid, "src": src, "trg": trg})
        elif etype == "add":
            # In ArgMicrotexts, 'trg' adds to 'src' to jointly support a conclusion
            if trg not in add_links:
                add_links[trg] = []
            add_links[trg].append(src)
        elif etype == "reb":
            rebuttals.append({"src": src, "trg": trg})
        elif etype == "und":
            undercuts.append({"src": src, "trg": trg}) # Target is usually an edge ID

    # Find True Premises (nodes that are NEVER the target of 'sup')
    supported_nodes = {edge["trg"] for edge in support_edges}

    # 3. Build Atoms & Level 0 Arguments (Knowledge Base)
    arg_map = {} # Maps a node_id to the Argument ID that concludes it
    
    for node_id, text in nodes.items():
        # Differentiate between base axioms/premises and derived claims
        kb_type = "premise" if node_id not in supported_nodes else "conclusion"
        atoms.append({"id": node_id, "text": text, "kb_type": kb_type})

        # Only true premises get Level 0 Atomic Arguments
        if kb_type == "premise":
            arg_id = f"A_{node_id}"
            arguments.append({
                "id": arg_id,
                "conclusion": node_id,
                "top_rule": None,
                "sub_arguments": [],
                "type": "atomic"
            })
            arg_map[node_id] = arg_id

    # 4. Build Rules & Derived Arguments (Iterative Topological Resolution)
    edge_to_rule = {}
    rule_counter = 1
    pending_edges = support_edges.copy()

    # Loop until all arguments are built (resolves chaining bottom-up)
    while pending_edges:
        progress = False
        for edge in pending_edges[:]:
            base_src = edge["src"]
            trg = edge["trg"]
            eid = edge["eid"]

            # Gather all linked premises for this specific rule
            rule_premises = [base_src] + add_links.get(base_src, [])

            # If all sub-arguments for this rule have been built, we can build this one
            if all(p in arg_map for p in rule_premises):
                rule_id = f"r{rule_counter}"
                rule_counter += 1
                edge_to_rule[eid] = rule_id

                # Create the Rule
                rules.append({
                    "id": rule_id,
                    "conclusion": trg,
                    "premises": rule_premises,
                    "type": "defeasible"
                })

                # Create the Derived Argument
                sub_args = [arg_map[p] for p in rule_premises]
                arg_id = f"A_{rule_id}"

                arguments.append({
                    "id": arg_id,
                    "conclusion": trg,
                    "top_rule": rule_id,
                    "sub_arguments": sub_args, # Correctly references prior derived/atomic arguments
                    "type": "defeasible"
                })
                
                # Update map to allow chaining
                arg_map[trg] = arg_id 
                pending_edges.remove(edge)
                progress = True

        if not progress:
            # Failsafe for unresolvable circular loops in dirty data
            break

    # 5. Process Attacks (Conflicts)
    for reb in rebuttals:
        src_node = reb["src"]
        trg_node = reb["trg"]
        # A rebuttal attacks the argument holding the conclusion
        if src_node in arg_map and trg_node in arg_map:
            attacks.append({
                "attacker": arg_map[src_node],
                "target": arg_map[trg_node],
                "type": "rebuttal"
            })

    for und in undercuts:
        src_node = und["src"]
        trg_edge = und["trg"]
        # An undercut attacks the rule/inference application itself
        if src_node in arg_map and trg_edge in edge_to_rule:
            target_rule = edge_to_rule[trg_edge]
            target_arg = f"A_{target_rule}"
            attacks.append({
                "attacker": arg_map[src_node],
                "target": target_arg,
                "type": "undercut"
            })

    return {
        "atoms": {"atoms": atoms},
        "rules": {"rules": rules},
        "arguments": {"arguments": arguments},
        "attacks": {"attacks": attacks} # New crucial ASPIC+ module
    }

def build_gold_standard_db(corpus_folder_path):
    # Minor OS fix: using os.path.join handles Windows/Linux slashes automatically
    gold_db = {}
    xml_files = glob.glob(os.path.join(corpus_folder_path, "*.xml"))
    
    for xml_file in xml_files:
        try:
            tree = ET.parse(xml_file)
            full_text = " ".join([edu.text.strip() for edu in tree.getroot().findall(".//edu") if edu.text])
            aspic_data = argmicro_to_aspic(xml_file)
            gold_db[full_text] = aspic_data
        except Exception as e:
            print(f"Failed to parse {xml_file}: {e}")
            
    # Use cross-platform pathing for your output directory as well
    out_path = os.path.join("PNsAV", "LLMbenchmarks", "benchmark_6_4agent_orchestration", "benchmark_data", "argmicrotexts_gold_standard.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    with open(out_path, "w") as f:
        json.dump(gold_db, f, indent=2)
        
    print(f"Successfully compiled {len(gold_db)} Gold Standard test cases!")

build_gold_standard_db(os.path.join("PNsAV", "evalDatasets", "arg-microtexts", "corpus", "en"))