import json

def verify_type(type):
    """Check if the type is valid (one of 'strict', 'defeasible')."""
    return type in ["strict", "defeasible"] # check if type is one of the valid types

def verify_rule_id(rule_id):
    """Check if the rule ID is valid (starts with 'r' followed by digits)."""
    if not rule_id.startswith("r"): # first character 'r'
        return False
    if not rule_id[1:].isdigit(): # the rest are digits
        return False
    return True

def validate_rules(json_string):
    """Validate the structure and types of the rules JSON. Returns True if valid, False otherwise.."""
    try:
        inp = json.loads(json_string)
    except json.JSONDecodeError:
        return False, "Invalid JSON format" # LLM returned invalid JSON
    
    logs = []

    for r in inp["rules"]:
        if "premises" not in r or "conclusion" not in r:
            logs.append(("Required keys missing for rule: {}".format(r.get("id", "Unknown")), "error"))
        if not isinstance(r["premises"], list):
            logs.append(("Invalid premises type for rule {}: {}".format(r.get("id", "Unknown"), r["premises"]),"error"))
        if not isinstance(r["conclusion"], str):
            logs.append(("Invalid conclusion type for rule {}: {}".format(r.get("id", "Unknown"), r["conclusion"]),"error"))
        if not verify_rule_id(r.get("id")):
            logs.append(("Invalid rule ID for rule {}: {}".format(r.get("id", "Unknown"), r["id"]),"error"))
        if not verify_type(r.get("type")):
            logs.append(("Invalid type for rule {}: {}".format(r.get("id", "Unknown"), r["type"]),"error"))
    if logs:
        return False, logs
    return True, [("Correct parsing of the rules","valid")] # all checks passed

def remove_identity(json_string):
    """Remove identity rules from the JSON string."""
    # identity rule is when the premise is identical to the conclusion
    try:
        inp = json.loads(json_string)
    except json.JSONDecodeError:
        return json_string # LLM returned invalid JSON
        
    inp["rules"] = [
        r for r in inp["rules"] 
        if not (len(r.get("premises", [])) == 1 and r["premises"][0] == r["conclusion"])
    ] # filtera regulile de identitate
        
    return inp

def remove_duplicate_rules(json_string):
    """Remove duplicate rules from the JSON string."""
    try:
        inp = json.loads(json_string)
    except json.JSONDecodeError:
        return json_string # LLM returned invalid JSON
        
    seen = set()
    unique_rules = []
    for r in inp["rules"]:
        rule_tuple = (tuple(r.get("premises", [])), r.get("conclusion"))
        if rule_tuple not in seen:
            seen.add(rule_tuple)
            unique_rules.append(r)
    
    inp["rules"] = unique_rules
    return inp