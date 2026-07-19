import json
import sys
import time
from pipeline import Log
import os
import platform

def main():
    mingw_bin_path = r"C:\\msys64\\mingw64\bin"

    if os.path.exists(mingw_bin_path):
        os.add_dll_directory(mingw_bin_path)
    else:
        print(f"Warning: MinGW path not found at {mingw_bin_path}. Check your installation.", file=sys.stderr)

    from engine import ArgEngine as module

    def topological_sort_arguments(arguments):
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

        if len(sorted_ids) != len(arguments):
            raise ValueError(
                "Cycle detected in argument construction graph — "
                "this should never happen; check the validation layer."
            )

        return [id_to_arg[aid] for aid in sorted_ids]

    payload = json.loads(sys.stdin.read())

    atoms_payload = payload["atoms"]
    rules_payload = payload["rules"]
    args_payload = payload["args"]
    attacks_payload = payload["attacks"]
    prior_logs = payload.get("logs", [])
    kappa = payload["kappa"]
    epsilon = payload["epsilon"]
    iters = payload["iters"]

    logs = [Log(l[0], l[1]) for l in prior_logs]

    start = time.perf_counter()

    engine = module.Engine()

    for atom in atoms_payload:
        obj_atom = module.Atom()
        obj_atom.id = atom["id"]
        obj_atom.text = atom["text"]
        obj_atom.kb_type = atom["kb_type"]
        obj_atom.source_quote = atom["source_quote"]
        obj_atom.strength = atom["strength"]
        engine.add_atom(obj_atom)

    for rule in rules_payload:
        obj_rule = module.Rule()
        obj_rule.id = rule["id"]
        obj_rule.conclusion = rule["conclusion"]
        obj_rule.premises = rule["premises"]
        obj_rule.type = rule["type"]
        obj_rule.strength = rule["strength"]
        engine.add_rule(obj_rule)

    sorted_args = topological_sort_arguments(args_payload)

    for arg in sorted_args:
        obj_arg = module.Argument()
        obj_arg.id = arg["id"]
        obj_arg.conclusion = arg["conclusion"]
        obj_arg.top_rule = arg["top_rule"]
        obj_arg.sub_arguments = arg["sub_arguments"]
        obj_arg.type = arg["type"]
        obj_arg.strength = 1.0
        engine.add_argument(obj_arg)

    for uc in attacks_payload["undercutters"]:
        obj_attack = module.Attack()
        obj_attack.attacker = uc[0]
        obj_attack.target = uc[1]
        obj_attack.type = "undercutter"
        engine.add_attack(obj_attack)

    for rb in attacks_payload["rebuttals"]:
        obj_attack = module.Attack()
        obj_attack.attacker = rb[0]
        obj_attack.target = rb[1]
        obj_attack.type = "rebuttal"
        engine.add_attack(obj_attack)

    for um in attacks_payload["underminers"]:
        obj_attack = module.Attack()
        obj_attack.attacker = um[0]
        obj_attack.target = um[1]
        obj_attack.type = "underminer"
        engine.add_attack(obj_attack)

    engine.build_attack_map()
    engine.build_argumentadj_vector()

    cycles = engine.compute_cycles()
    engine.compute_argument_strengths()
    rounds = engine.propagate_strengths(kappa, iters, epsilon)

    logs.append(Log(f"Rounds executed until strength converged: {rounds}.", "info"))
    logs.append(Log(f"Found {len(cycles)} cycles in the graph.", "info"))
    logs.append(Log(f"Engine took {time.perf_counter()-start:.4f} seconds to run.", "info"))

    def print_atom(atom):
        print(atom.id, atom.kb_type, atom.text, atom.strength, atom.source_quote, sep="|", end="-")

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