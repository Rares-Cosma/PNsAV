# verify arg type and fix it
# verify data types

import json

#"arguments":[{"id":"A1","conclusion":"a1","top_rule":null,"sub_arguments":[],"type":"atomic"}

def verify_arg_id(arg_id):
    """Check if the argument ID is valid (starts with 'A' followed by digits)."""
    if not isinstance(arg_id, str):
        return False # argument ID must be a string
    if not arg_id.startswith("A"): # first character 'A'
        return False
    if not arg_id[1:].isdigit(): # the rest are digits
        return False
    return True

def verify_type(arg_type):
    """Check if the argument type is valid (one of 'atomic', 'defeasible', 'strict')."""
    return arg_type in ["atomic", "defeasible", "strict"] # check if arg_type is one of the valid types

def verify_conclusion_match(arg,rules):
    """Check if the argument's conclusion matches the conclusion of its top rule."""

    if type(rules) == str:
        try:
            rules = json.loads(rules)
        except json.JSONDecodeError:
            return False, ["Invalid JSON format for rules"] # LLM returned invalid JSON for rules
        
    top_rule_id = arg.get("top_rule")
    if top_rule_id is None:
        return True # no top rule to check
    for r in rules:
        if type(r) != str:
            if r.get("id") == top_rule_id:
                return r.get("conclusion") == arg.get("conclusion") # check if conclusions match
    return False # top rule not found

def verify_sub_arguments(arg, rules, arguments_map):
    """Check if the conclusions of the sub-argument IDs match the premises of the top rule."""

    if type(rules) == str:
        try:
            rules = json.loads(rules)
        except json.JSONDecodeError:
            return False, ["Invalid JSON format for rules"] # LLM returned invalid JSON for rules

    top_rule_id = arg.get("top_rule")
    if top_rule_id is None or top_rule_id == "null":
        return True 
        
    for r in rules:
        if type(r) != str:
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
    """Validate the structure and types of the arguments JSON. Returns True if valid, False otherwise."""
    try:
        inp = json.loads(json_string)
    except json.JSONDecodeError:
        return False, [("Invalid JSON format", "error")] # LLM returned invalid JSON
    
    logs = []
        
    for arg in inp["arguments"]:
        if set(["id","conclusion","top_rule","sub_arguments","type"]) != set(arg.keys()):
            logs.append(("Required keys missing for argument: {}".format(arg.get("id", "Unknown")), "error"))
        if not verify_arg_id(arg["id"]):
            logs.append(("Invalid argument ID: {}".format(arg["id"]), "error"))
        if not verify_type(arg["type"]):
            logs.append(("Invalid argument type for argument {}: {}".format(arg["id"], arg["type"]), "error"))
        if not verify_conclusion_match(arg, rules):
            logs.append(("Conclusion does not match the top rule for argument {}: {}".format(arg["id"], arg["conclusion"]), "warning"))
        if not verify_sub_arguments(arg, rules, inp["arguments"]):
            logs.append(("Sub-arguments are invalid for argument {}: {}".format(arg["id"], arg["sub_arguments"]), "warning"))
    if logs:
        return False, logs
    return True, [("Correct parsing of the arguments", "valid")] # all checks passed