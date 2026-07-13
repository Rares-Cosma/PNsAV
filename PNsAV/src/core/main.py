import ast
import json
import sys
from pipeline import Pipeline, Log
import os

def main():
    if len(sys.argv) < 2:
        print("Error: No input data provided.")
        sys.exit(1)
        
    data = sys.argv[1]

    mingw_bin_path = r"C:\\msys64\\mingw64\bin" 

    if os.path.exists(mingw_bin_path):
        os.add_dll_directory(mingw_bin_path)
    else:
        print(f"Warning: MinGW path not found at {mingw_bin_path}. Check your installation.")


    from engine import ArgEngine as module

    def topological_sort_arguments(arguments):
        """
        arguments: list of dicts, each with "id" and "sub_arguments" (list of ids)
        Returns a new list, reordered so every argument appears after all of
        its subarguments.
        """
        id_to_arg = {arg["id"]: arg for arg in arguments}

        in_degree = {arg["id"]: 0 for arg in arguments}
        dependents = {arg["id"]: [] for arg in arguments}

        for arg in arguments:
            for sub_id in arg["sub_arguments"]:
                if sub_id not in id_to_arg:
                    raise ValueError(
                        f"Argument {arg['id']} references unknown subargument {sub_id}"
                    )
                dependents[sub_id].append(arg["id"])
                in_degree[arg["id"]] += 1

        ready = [aid for aid, deg in in_degree.items() if deg == 0]
        sorted_ids = []

        while ready:
            current = ready.pop()
            sorted_ids.append(current)
            for dep in dependents[current]:
                in_degree[dep] -= 1
                if in_degree[dep] == 0:
                    ready.append(dep)

        return [id_to_arg[aid] for aid in sorted_ids]

    pipeline = Pipeline("C:\\Users\\rares\\OneDrive\\Desktop\\infoed26\\PNsAV\\src\\agents_prompts")
    atoms, rules, args, logs = pipeline.execute_orchestration(
        agents=["gpt-5.4-mini", "gpt-5.4-mini", "gpt-5.4-mini"],
        data=data,
        schemas=[pipeline.atom_schema, pipeline.rule_schema, pipeline.arg_schema]
    )

    attacks = pipeline.generate_attacks(str(rules), str(args))

    rules=ast.literal_eval(rules)
    args=json.loads(args)
    #print("Atoms:", atoms)
    #print("Rules:", rules)
    #print("Arguments:", args)

    engine = module.Engine()

    for atom in atoms["atoms"]:
        obj_atom = module.Atom()
        obj_atom.id = atom["id"]
        obj_atom.text = atom["text"]
        obj_atom.kb_type = atom["kb_type"]
        obj_atom.source_quote = atom["source_quote"]
        obj_atom.strength = 1.0 if atom["kb_type"] == "axiom" else 0.9
        engine.add_atom(obj_atom)

    for rule in rules["rules"]:
        obj_rule = module.Rule()
        obj_rule.id = rule["id"]
        obj_rule.conclusion = rule["conclusion"]
        obj_rule.premises = rule["premises"]
        obj_rule.type = rule["type"]
        obj_rule.strength = 1.0 if rule["type"] == "strict" else 0.95
        engine.add_rule(obj_rule)

    sorted_args = topological_sort_arguments(args["arguments"])

    for arg in sorted_args:
        obj_arg = module.Argument()
        obj_arg.id = arg["id"]
        obj_arg.conclusion = arg["conclusion"]
        obj_arg.top_rule = arg["top_rule"]
        obj_arg.sub_arguments = arg["sub_arguments"]
        obj_arg.type = arg["type"]
        obj_arg.strength = 1.0
        engine.add_argument(obj_arg)

    for uc in attacks["undercutters"]:
        obj_attack = module.Attack()
        obj_attack.attacker = uc[0]
        obj_attack.target = uc[1]
        obj_attack.type = "undercutter"
        engine.add_attack(obj_attack)

    for rb in attacks["rebuttals"]:
        obj_attack = module.Attack()
        obj_attack.attacker = rb[0]
        obj_attack.target = rb[1]
        obj_attack.type = "rebuttal"
        engine.add_attack(obj_attack)

    for um in attacks["underminers"]:
        obj_attack = module.Attack()
        obj_attack.attacker = um[0]
        obj_attack.target = um[1]
        obj_attack.type = "underminer"
        engine.add_attack(obj_attack)

    engine.build_attack_map()
    engine.build_argumentadj_vector()

    cycles = engine.compute_cycles()
    engine.compute_argument_strengths()
    engine.propagate_strengths(0.7,0,0.001)

    def print_atom(atom):
        print(atom.id, atom.kb_type, atom.text, atom.strength, sep="|", end="-")

    def print_rule(rule):
        print(rule.id, rule.premises, rule.conclusion, rule.type, rule.strength, sep="|", end="-")

    def print_arg(arg):
        print(arg.id, arg.type, arg.top_rule, arg.sub_arguments, arg.strength, arg.conclusion, sep="|", end="-")

    def print_attack(attack):
        print(attack.type, attack.target, attack.attacker, sep="|", end="-")
    
    def print_log(log):
        print(log.text, log.type, sep="|", end="-")

    for i in engine.atoms:
        print_atom(i)
    print("@", end="")
    for i in engine.rules:
        print_rule(i)
    print("@", end="")
    for i in engine.arguments:
        print_arg(i)
    print("@", end="")
    for i in engine.attacks:
        print_attack(i)
    print("@", end="")
    for i in logs:
        print_log(i)

if __name__ == "__main__":
    main()