import json
import ast
from model import Model
from schema import atom_schema, argument_schema, rule_schema
import symbolic_data_repair.atom as atom
import symbolic_data_repair.arg as arg
import symbolic_data_repair.rule as rule

class Pipeline:
    def __init__(self, prompt_path):
        self.model = Model(prompt_path)
        self.logs = []
        self.atom_schema = atom_schema
        self.rule_schema = rule_schema
        self.arg_schema = argument_schema
    
    def execute_orchestration(self, agents, data, schemas):
        atoms = self.model.run_agent(
            agent_id=agents[0],
            data=[data],
            schema=schemas[0],
            system_prompt=self.model.ATOM_PROMPT
        )

        atom_status, atom_log = atom.validate_atoms(atoms, data)
        self.logs.append(atom_log)
        atoms = atom.remove_duplicate_atoms(atoms)

        rules = self.model.run_agent(
            agent_id=agents[1],
            data=[data,str(atoms)],
            schema=schemas[1],
            system_prompt=self.model.RULE_PROMPT
        )

        rules_status, rules_log = rule.validate_rules(rules)
        self.logs.append(rules_log)
        rules = rule.remove_identity(rules)
        rules = rule.remove_duplicate_rules(str(rules))

        args = self.model.run_agent(
            agent_id=agents[2],
            data=[data,str(atoms),str(rules)],
            schema=schemas[2],
            system_prompt=self.model.ARG_PROMPT
        )

        args_status, args_log = arg.validate_arguments(args, rules)
        self.logs.append(args_log)

        return atoms, rules, args, self.logs

    def generate_attacks(self, rules, args):
        rules = ast.literal_eval(rules)
        args = json.loads(args)["arguments"]

        undercuts = rules["conflicts"]["undercutters"]
        undercutter_attacks = []
        contraries = rules["conflicts"]["contraries"]
        rebuttals = []
        underminers = []

        for pair in contraries:
            for i in range(len(args)):

                if args[i]["conclusion"] == pair[0]:
                    for j in range(len(args)):
                        if args[j]["conclusion"] == pair[1]:
                            if args[j]["type"] != "atomic":
                                rebuttals.append((args[i]["id"], args[j]["id"]))
                            else:
                                underminers.append((args[i]["id"], args[j]["id"]))
                
                if args[i]["conclusion"] == pair[1]:
                    for j in range(len(args)):
                        if args[j]["conclusion"] == pair[0]:
                            if args[j]["type"] != "atomic":
                                rebuttals.append((args[i]["id"], args[j]["id"]))
                            else:
                                underminers.append((args[i]["id"], args[j]["id"]))
        
        for i in range(len(args)):
            for uc in undercuts:
                if args[i]["conclusion"] == uc["attacker"]:
                    for j in range(len(args)):
                        if args[j].get("top_rule") == uc["target_rule"]:
                            undercutter_attacks.append((args[i]["id"], args[j]["id"]))
        
        return {
            "rebuttals": rebuttals,
            "underminers": underminers,
            "undercutters": undercutter_attacks
        }
        