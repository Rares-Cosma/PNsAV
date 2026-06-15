import json

class Rules:
    def __init__(self):
        pass
    def remove_identity(self, json_string):
        try:
            inp = json.loads(json_string)
        except json.JSONDecodeError:
            print("Error: LLM returned invalid JSON")
            return {"rules": []}

        if "rules" not in inp:
            return inp
        
        inp["rules"] = [
            r for r in inp["rules"] 
            if not (len(r.get("premises", [])) == 1 and r["premises"][0] == r["conclusion"])
        ]
        
        return inp