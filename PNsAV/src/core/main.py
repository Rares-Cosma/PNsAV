import ast
import json
from pipeline import Pipeline

import os

mingw_bin_path = r"C:\\msys64\\mingw64\bin" 

if os.path.exists(mingw_bin_path):
    os.add_dll_directory(mingw_bin_path)
else:
    print(f"Warning: MinGW path not found at {mingw_bin_path}. Check your installation.")


from engine import ArgEngine as module


data="If it is sunny, we have a picnic, unless the park is closed."

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
    engine.add_atom(obj_atom)

for rule in rules["rules"]:
    obj_rule = module.Rule()
    obj_rule.id = rule["id"]
    obj_rule.conclusion = rule["conclusion"]
    obj_rule.premises = rule["premises"]
    obj_rule.type = rule["type"]
    engine.add_rule(obj_rule)

for arg in args["arguments"]:
    obj_arg = module.Argument()
    obj_arg.id = arg["id"]
    obj_arg.conclusion = arg["conclusion"]
    obj_arg.top_rule = arg["top_rule"]
    obj_arg.sub_arguments = arg["sub_arguments"]
    obj_arg.type = arg["type"]
    engine.add_argument(obj_arg)

for uc in attacks["undercutters"]:
    obj_attack = module.Attack()
    obj_attack.attacker = uc["attacker"]
    obj_attack.target = uc["target"]
    obj_attack.type = uc["type"]
    engine.add_attack(obj_attack)

for rb in attacks["rebuttals"]:
    obj_attack = module.Attack()
    obj_attack.attacker = rb["attacker"]
    obj_attack.target = rb["target"]
    obj_attack.type = rb["type"]
    engine.add_attack(obj_attack)

for um in attacks["underminers"]:
    obj_attack = module.Attack()
    obj_attack.attacker = um["attacker"]
    obj_attack.target = um["target"]
    obj_attack.type = um["type"]
    engine.add_attack(obj_attack)

