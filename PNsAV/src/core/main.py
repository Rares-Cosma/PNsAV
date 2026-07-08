from pipeline import Pipeline
import os

data="If it is sunny, we have a picnic, unless the park is closed."

pipeline = Pipeline(os.path.join(os.getcwd(), "PNsAV\\src\\agents_prompts"))
atoms, rules, args = pipeline.execute_orchestration(
    agents=["gpt-5.4-mini", "gpt-5.4-mini", "gpt-5.4-mini"],
    data=data,
    schemas=[pipeline.atom_schema, pipeline.rule_schema, pipeline.arg_schema]
)

print(pipeline.generate_attacks(str(rules), str(args)))