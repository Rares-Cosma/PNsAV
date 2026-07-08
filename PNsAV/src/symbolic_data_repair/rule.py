import json

def verify_kb_type(kb_type):
    """Check if the kb_type is valid (one of 'strict', 'defeasible').
       Verifica daca kb_type este valid (unul dintre 'strict', 'defeasible')."""
    return kb_type in ["strict", "defeasible"] # check if kb_type is one of the valid types/verifica daca kb_type este unul dintre tipurile valide

def verify_rule_id(rule_id):
    """Check if the rule ID is valid (starts with 'r' followed by digits).
       Verifica daca ID-ul regulii este valid (incepe cu 'r' urmat de cifre)."""
    if not rule_id.startswith("r"): # first character 'r'/'r' este primul caracter
        return False
    if not rule_id[1:].isdigit(): # the rest are digits/restul sunt cifre
        return False
    return True

def validate_rules(json_string):
    """Validate the structure and types of the rules JSON. Returns True if valid, False otherwise.
       Valideaza structura si tipurile de date din JSON-ul de reguli. Returneaza adevarat daca este valid, fals altfel."""
    try:
        inp = json.loads(json_string)
    except json.JSONDecodeError:
        return False # LLM returned invalid JSON/LLM-ul a returnat un JSON invalid
        
    for r in inp["rules"]:
        if "premises" not in r or "conclusion" not in r:
            return False # each rule must have 'premises' and 'conclusion'/fiecare regula trebuie sa aiba 'premises' si 'conclusion'
        if not isinstance(r["premises"], list):
            return False # 'premises' must be a list/'premises' trebuie sa fie o lista
        if not isinstance(r["conclusion"], str):
            return False # 'conclusion' must be a string/'conclusion' trebuie sa fie un sir de caractere
        if not verify_rule_id(r.get("id")):
            return False # rule ID is invalid/ID-ul regulii este invalid
        if not verify_kb_type(r.get("kb_type")):
            return False # kb_type is invalid/tipul kb este invalid
    return True
    
def remove_identity(json_string):
    """Remove identity rules from the JSON string.
       Elimina regulile de identitate din sirul JSON."""
    # regula de identitate este at. cand premisa e identica cu concluzia
    # identity rule is when the premise is identical to the conclusion
    try:
        inp = json.loads(json_string)
    except json.JSONDecodeError:
        return False # LLM returned invalid JSON/LLM-ul a returnat un JSON invalid
        
    inp["rules"] = [
        r for r in inp["rules"] 
        if not (len(r.get("premises", [])) == 1 and r["premises"][0] == r["conclusion"])
    ] # filtera regulile de identitate/filters out identity rules
        
    return inp

def remove_duplicate_rules(json_string):
    """Remove duplicate rules from the JSON string.
       Elimina regulile duplicate din sirul JSON."""
    try:
        inp = json.loads(json_string)
    except json.JSONDecodeError:
        return False # LLM returned invalid JSON/LLM-ul a returnat un JSON invalid
        
    seen = set()
    unique_rules = []
    for r in inp["rules"]:
        rule_tuple = (tuple(r.get("premises", [])), r.get("conclusion"))
        if rule_tuple not in seen:
            seen.add(rule_tuple)
            unique_rules.append(r)
    
    inp["rules"] = unique_rules
    return inp