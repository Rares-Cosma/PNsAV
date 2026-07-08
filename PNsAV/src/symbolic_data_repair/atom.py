import json

def verify_source_quotes(source_quote, source):
    """Check if the source quote is present in the source text.
       Verifica daca citarea sursei este prezenta in textul sursei."""
    return source_quote in source # check if the source quote is present in the source text/verifica daca citarea sursei este prezenta in textul sursei

def verify_atom_id(atom_id):
    """Check if the atom ID is valid (starts with 'a' followed by digits).
       Verifica daca ID-ul atomului este valid (incepe cu 'a' urmat de cifre)."""
    if not atom_id.startswith("a"): # first character 'a'/'a' este primul caracter
        return False
    if not atom_id[1:].isdigit(): # the rest are digits/restul sunt cifre
        return False
    return True

def verify_kb_type(kb_type):
    """Check if the kb_type is valid (one of 'strict', 'defeasible').
       Verifica daca kb_type este valid (unul dintre 'strict', 'defeasible')."""
    return kb_type in ["strict", "defeasible"] # check if kb_type is one of the valid types/verifica daca kb_type este unul dintre tipurile valide

def validate_atoms(json_string, source):
    try:
        inp = json.loads(json_string)
    except json.JSONDecodeError:
        return False # LLM returned invalid JSON/LLM-ul a returnat un JSON invalid
    
    for atom in inp["atoms"]: # id, text, kb_type, source_quote
        if set(["id","text","kb_type","source_quote"]) != set(atom.keys()):
            return False # each atom must have 'id', 'text', 'kb_type', and 'source_quote'/fiecare atom trebuie sa aiba 'id', 'text', 'kb_type', si 'source_quote'
        if not verify_atom_id(atom["id"]):
            return False # atom ID is invalid/ID-ul atomului este invalid
        if not verify_kb_type(atom["kb_type"]):
            return False # kb_type is invalid/tipul kb este invalid
        if not verify_source_quotes(atom["source_quote"], source):
            return False # source quote does not match the text/citarea sursei nu corespunde textului

def remove_duplicate_atoms(json_string):
    """Remove duplicate atoms from the JSON string.
       Elimina atomii duplicati din sirul JSON."""
    try:
        inp = json.loads(json_string)
    except json.JSONDecodeError:
        return False # LLM returned invalid JSON/LLM-ul a returnat un JSON invalid
        
    seen = set()
    unique_atoms = []
    for atom in inp["atoms"]:
        atom_tuple = (atom["text"])
        if atom_tuple not in seen:
            seen.add(atom_tuple)
            unique_atoms.append(atom)
    
    inp["atoms"] = unique_atoms
    return inp