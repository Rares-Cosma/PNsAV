# verify arg type and fix it
# verify data types

import json

#"arguments":[{"id":"A1","conclusion":"a1","top_rule":null,"sub_arguments":[],"type":"atomic"}

def verify_arg_id(arg_id):
    """Check if the argument ID is valid (starts with 'A' followed by digits).
       Verifica daca ID-ul argumentului este valid (incepe cu 'A' urmat de cifre)."""
    if not isinstance(arg_id, str):
        return False # argument ID must be a string/ID-ul argumentului trebuie sa fie un sir de caractere   
    if not arg_id.startswith("A"): # first character 'A'/'A' este primul caracter
        return False
    if not arg_id[1:].isdigit(): # the rest are digits/restul sunt cifre
        return False
    return True

def verify_type(arg_type):
    """Check if the argument type is valid (one of 'atomic', 'defeasible').
       Verifica daca tipul argumentului este valid (unul dintre 'atomic', 'defeasible')."""
    return arg_type in ["atomic", "defeasible"] # check if arg_type is one of the valid types/verifica daca arg_type este unul dintre tipurile valide

def verify_conclusion_match(arg,rules):
    """Check if the argument's conclusion matches the conclusion of its top rule.
       Verifica daca concluzia argumentului corespunde cu concluzia regulii sale superioare."""
    top_rule_id = arg.get("top_rule")
    if top_rule_id is None:
        return True # No top rule to check/fara regula de verificat
    for r in rules:
        if r.get("id") == top_rule_id:
            return r.get("conclusion") == arg.get("conclusion") # check if conclusions match/verifica daca concluziile corespund
    return False # Top rule not found/Regula nu a fost gasita

def verify_sub_arguments(arg, rules, arguments_map):
    """Check if the conclusions of the sub-argument IDs match the premises of the top rule.]
       Verifica daca concluziile ID-urilor sub-argumentelor corespund cu premisele regulii superioare."""
    top_rule_id = arg.get("top_rule")
    if top_rule_id is None:
        return True 
        
    for r in rules:
        if r.get("id") == top_rule_id:
            premises = r.get("premises", [])
            sub_arg_ids = arg.get("sub_arguments", [])
            
            if len(premises) != len(sub_arg_ids):
                return False 
                
            for sub_arg_id, premise in zip(sub_arg_ids, premises):
                sub_arg = arguments_map.get(sub_arg_id)
                if not sub_arg:
                    return False
                    
                if sub_arg.get("conclusion") != premise:
                    return False 
            return True
            
    return False

def validate_arguments(json_string, rules):
    """Validate the structure and types of the arguments JSON. Returns True if valid, False otherwise.
       Valideaza structura si tipurile de date din JSON-ul de argumente. Returneaza adevarat daca este valid, fals altfel."""
    try:
        inp = json.loads(json_string)
    except json.JSONDecodeError:
        return False # LLM returned invalid JSON/LLM-ul a returnat un JSON invalid
        
    for arg in inp["arguments"]:
        if set(["id","conclusion","top_rule","sub_arguments","type"]) != set(arg.keys()):
            return False # each argument must have the required keys/fiecare argument trebuie sa aiba cheile necesare
        if not verify_arg_id(arg["id"]):
            return False # argument ID is invalid/ID-ul argumentului este invalid
        if not verify_type(arg["type"]):
            return False # argument type is invalid/tipul argumentului este invalid
        if not verify_conclusion_match(arg, rules):
            return False # conclusion does not match the top rule/concluzia nu corespunde cu regula superioara
        if not verify_sub_arguments(arg, rules, inp["arguments"]):
            return False # sub-arguments are invalid/sub-argumentele sunt invalide
    return True