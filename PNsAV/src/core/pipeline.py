import json
import ast
from model import Model
from schema import atom_schema, argument_schema, rule_schema
import symbolic_data_repair.atom as atom
import symbolic_data_repair.arg as arg
import symbolic_data_repair.rule as rule
import time

class Log:
    def __init__(self, text, type):
        self.text = text
        self.type = type

class Pipeline:
    def __init__(self, prompt_path):
        self.model = Model(prompt_path)
        self.logs = []
        self.atom_schema = atom_schema
        self.rule_schema = rule_schema
        self.arg_schema = argument_schema
    
    def execute_orchestration(self, agents, data, schemas):
        start = time.perf_counter()

        atoms = self.model.run_agent(
            agent_id=agents[0],
            data=[data],
            schema=schemas[0],
            system_prompt=self.model.ATOM_PROMPT
        )

        atom_status, atom_logs = atom.validate_atoms(atoms, data)
        for i in atom_logs:
            log = Log(i[0], i[1])
            self.logs.append(log)
        atoms = atom.remove_duplicate_atoms(atoms)

        rules = self.model.run_agent(
            agent_id=agents[1],
            data=[data,str(atoms)],
            schema=schemas[1],
            system_prompt=self.model.RULE_PROMPT
        )

        rules_status, rules_logs = rule.validate_rules(rules)
        for i in rules_logs:
            log = Log(i[0], i[1])
            self.logs.append(log)
        rules = rule.remove_identity(rules)
        rules = rule.remove_duplicate_rules(str(rules))

        args = self.model.run_agent(
            agent_id=agents[2],
            data=[data,str(atoms),str(rules)],
            schema=schemas[2],
            system_prompt=self.model.ARG_PROMPT
        )

        args_status, args_logs = arg.validate_arguments(args, rules)
        for i in args_logs:
            log = Log(i[0], i[1])
            self.logs.append(log)

        self.logs.append(Log(f"Text extraction and validation took: {time.perf_counter()-start:.4f} seconds", "info"))

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
        