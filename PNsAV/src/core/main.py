from pipeline import Pipeline
import os

data="If a vehicle has a siren, it is an emergency vehicle. If a vehicle is an emergency vehicle, it can run red lights. Engine 42 has a siren."

pipeline = Pipeline(os.path.join(os.getcwd(), "PNsAV\\src\\agents_prompts"))
atoms, rules, args = pipeline.execute_orchestration(
    agents=["gpt-5.4-mini", "gpt-5.4-mini", "gpt-5.4-mini"],
    data=data,
    schemas=[pipeline.atom_schema, pipeline.rule_schema, pipeline.arg_schema]
)

