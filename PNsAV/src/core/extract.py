from pipeline import *
import os
import sys

def main():

    if len(sys.argv) < 2:
        print("Error: No input data provided.")
        sys.exit(1)
        
    data = sys.argv[1]

    pipeline = Pipeline("C:\\Users\\rares\\OneDrive\\Desktop\\infoed26\\PNsAV\\src\\agents_prompts")
    atoms, rules, args, logs = pipeline.execute_orchestration(
        agents=["gpt-5.4-mini", "gpt-5.4-mini", "gpt-5.4-mini"],
        data=data,
        schemas=[pipeline.atom_schema, pipeline.rule_schema, pipeline.arg_schema]
    )

    attacks = pipeline.generate_attacks(str(rules), str(args))
    ast_logs=[]
    for i in logs:
        ast_logs.append((i.text,i.type))

    print(atoms, rules, args, attacks, str(ast_logs), sep="@")

    #rules=ast.literal_eval(rules)
    #args=json.loads(args)
    #print("Atoms:", atoms)
    #print("Rules:", rules)
    #print("Arguments:", args)

if __name__ == "__main__":
    main()