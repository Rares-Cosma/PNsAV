import json

def verify_source_quotes(source_quote, source):
    """Check if the source quote is present in the source text."""
    return source_quote in source # check if the source quote is present in the source text

def verify_atom_id(atom_id):
    """Check if the atom ID is valid (starts with 'a' followed by digits)."""
    if not atom_id.startswith("a"): # first character 'a'
        return False
    if not atom_id[1:].isdigit(): # the rest are digits
        return False
    return True

def verify_kb_type(kb_type):
    """Check if the kb_type is valid (one of 'axiom', 'premise')."""
    return kb_type in ["axiom", "premise"] # check if kb_type is one of the valid types

def validate_atoms(json_string, source):
    try:
        inp = json.loads(json_string)
    except json.JSONDecodeError:
        return False, "Invalid JSON format" # LLM returned invalid JSON
    
    logs = []
    
    for atom in inp["atoms"]: # id, text, kb_type, source_quote
        if set(["id","text","kb_type","source_quote"]) != set(atom.keys()):
            logs.append("Required keys missing for atom: {}".format(atom.get("id", "Unknown")))
        if not verify_atom_id(atom["id"]):
            logs.append("Invalid atom ID: {}".format(atom["id"]))
        if not verify_kb_type(atom["kb_type"]):
            logs.append("Invalid knowledge base type for atom {}: {}".format(atom["id"], atom["kb_type"]))
        if not verify_source_quotes(atom["source_quote"], source):
            logs.append("Source quote does not match the text for atom {}: {}".format(atom["id"], atom["source_quote"]))
    
    if logs:
        return False, logs
    return True, ["Correct parsing of the atoms"] # all checks passed

def remove_duplicate_atoms(json_string):
    """Remove duplicate atoms from the JSON string."""
    try:
        inp = json.loads(json_string)
    except json.JSONDecodeError:
        return json_string # LLM returned invalid JSON
        
    seen = set()
    unique_atoms = []
    for atom in inp["atoms"]:
        atom_tuple = (atom["text"])
        if atom_tuple not in seen:
            seen.add(atom_tuple)
            unique_atoms.append(atom)
    
    inp["atoms"] = unique_atoms
    return inp