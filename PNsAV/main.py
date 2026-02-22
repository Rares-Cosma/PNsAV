import json
import ollama
import re
from pydantic import BaseModel, ValidationError
from typing import List, Literal


# -----------------------------
# SCHEMA
# -----------------------------

class Atom(BaseModel):
    id: str
    text: str


class Rule(BaseModel):
    id: str
    type: Literal["strict"]
    premises: List[str]
    conclusion: str


class Argument(BaseModel):
    id: str
    premises: List[str]
    applied_rules: List[str]
    conclusion: str


class Attack(BaseModel):
    from_arg: str
    to_arg: str
    type: Literal["rebut"]


class DebateStructure(BaseModel):
    atoms: List[Atom]
    rules: List[Rule]
    arguments: List[Argument]
    attacks: List[Attack]


# -----------------------------
# PROMPT
# -----------------------------

SYSTEM_PROMPT = """
You are an expert logician and formal argumentation extractor specializing in the ASPIC+ framework. 

Your sole objective is to analyze natural language text and decompose it into a structured Argumentation Framework. 

You must output ONLY valid, parsable JSON matching the exact schema below. Do not include markdown code blocks (e.g., ```json), conversational filler, explanations, or preamble. Start exactly with '{' and end exactly with '}'.

### JSON SCHEMA
{
  "atoms": [
    {"id": "a1", "text": "<Minimal, atomic logical proposition>"}
  ],
  "rules": [
    {"id": "r1", "type": "<strict|defeasible>", "premises": ["<atom_id>"], "conclusion": "<atom_id>"}
  ],
  "arguments": [
    {"id": "arg1", "premises": ["<atom_id>"], "applied_rules": ["<rule_id>"], "conclusion": "<atom_id>", "sub_arguments": ["<arg_id>"]}
  ],
  "attacks": [
    {"from_arg": "<arg_id>", "to_arg": "<arg_id>", "type": "<rebut|undercut|undermine>"}
  ]
}

### ASPIC+ DEFINITIONS & EXTRACTION RULES

1. ATOMS (Propositions):
   - Break text into the smallest possible, independent logical propositions.
   - Resolve pronouns (e.g., convert "He lied" to "John lied" if John is the subject).
   - Each distinct entity, claim, or fact must be a separate atom.
   - Do NOT merge claims. 

2. RULES (Inferences):
   - "strict": Deductive certainty, logical necessity, or physical laws (e.g., "If x is a bachelor, x is unmarried").
   - "defeasible": Presumptive, typical, or fallible reasoning (e.g., "If x is a bird, x usually flies", "If witness says X, X is true").
   - A rule maps a set of premise atoms to a conclusion atom. 
   - Extract enthymemes (implicit rules) ONLY if strictly necessary to connect stated claims.

3. ARGUMENTS (Tree Structure):
   - An argument applies rules to premises to reach a conclusion.
   - RECURSION: Arguments are tree-like. If an argument uses the conclusion of another argument as its premise, you MUST include the parent argument's ID in the "sub_arguments" array.
   - Base arguments (relying only on direct atoms) have an empty "sub_arguments" list.

4. ATTACKS (Defeats):
   - "rebut": Argument A attacks the CONCLUSION of Argument B (Arg A claims 'not X', Arg B claims 'X'). Only applies if the targeted conclusion comes from a defeasible rule.
   - "undercut": Argument A attacks the RULE APPLICATION / INFERENCE of Argument B (e.g., Arg B uses a witness; Arg A points out the witness is blind. The premise isn't attacked, the conclusion isn't directly attacked, but the link is broken).
   - "undermine": Argument A attacks a PREMISE (atom) used in Argument B.

### STRICT FORMATTING CONSTRAINTS
- IDs must be deterministic and strictly formatted: a1, a2... r1, r2... arg1, arg2...
- Missing elements: If no rules, arguments, or attacks exist, return empty arrays: [].
- NEVER invent information not explicitly stated or logically necessitated by the text.
- JSON key names must perfectly match the schema.

### FEW-SHOT EXAMPLE
Input Text:
"John says the car is red, so the car is red. However, John is colorblind. Also, the car registration says it is blue, meaning it cannot be red."

Expected JSON Output:
{
  "atoms": [
    {"id": "a1", "text": "John says the car is red"},
    {"id": "a2", "text": "The car is red"},
    {"id": "a3", "text": "John is colorblind"},
    {"id": "a4", "text": "The car registration says it is blue"},
    {"id": "a5", "text": "The car is blue"},
    {"id": "a6", "text": "The car cannot be red"}
  ],
  "rules": [
    {"id": "r1", "type": "defeasible", "premises": ["a1"], "conclusion": "a2"},
    {"id": "r2", "type": "defeasible", "premises": ["a4"], "conclusion": "a5"},
    {"id": "r3", "type": "strict", "premises": ["a5"], "conclusion": "a6"}
  ],
  "arguments": [
    {"id": "arg1", "premises": ["a1"], "applied_rules": ["r1"], "conclusion": "a2", "sub_arguments": []},
    {"id": "arg2", "premises": ["a3"], "applied_rules": [], "conclusion": "a3", "sub_arguments": []},
    {"id": "arg3", "premises": ["a4"], "applied_rules": ["r2"], "conclusion": "a5", "sub_arguments": []},
    {"id": "arg4", "premises": [], "applied_rules": ["r3"], "conclusion": "a6", "sub_arguments": ["arg3"]}
  ],
  "attacks": [
    {"from_arg": "arg2", "to_arg": "arg1", "type": "undercut"},
    {"from_arg": "arg4", "to_arg": "arg1", "type": "rebut"}
  ]
}

### LOGIC CHECK - VERIFY BEFORE OUTPUT:
1. Every 'conclusion' in the 'arguments' list must be a text-id from the 'atoms' list.
2. Every 'sub_argument' must be a valid 'arg_id' defined elsewhere in the 'arguments' list.
3. If Arg A attacks Arg B, identify EXACTLY what is being attacked:
   - If A contradicts B's conclusion: type = "rebut".
   - If A attacks a premise in B: type = "undermine".
   - If A attacks the rule linking B's premise to its conclusion: type = "undercut".
4. Ensure no argument is its own premise (Avoid ID circularity: arg1 cannot depend on arg1).

PROCESS THE FOLLOWING TEXT:
"""


# -----------------------------
# TRANSLATOR FUNCTION
# -----------------------------

def translate(text: str) -> DebateStructure:
    response = ollama.chat(
        model="llama3",
        format="json",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        options={"temperature": 0}
    )

    raw_output = response["message"]["content"].strip()

    print(raw_output)  # Debug: Print raw LLM output

    # ✅ Safe JSON extraction using regex
    match = re.search(r"\{.*\}", raw_output, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in LLM output")
    json_str = match.group(0)

    # ✅ Clean invalid control characters
    json_str = re.sub(r'[\x00-\x1f]+', '', json_str)

    # ✅ Load JSON
    data = json.loads(json_str)

    # ✅ Fallback for misnamed keys
    for atom in data.get("atoms", []):
        if "idterm" in atom:
            atom["id"] = atom.pop("idterm")
        if "text" not in atom:
            atom["text"] = atom["id"]

    # Validate strictly
    validated = DebateStructure(**data)

    return validated


# -----------------------------
# MAIN
# -----------------------------

print("Enter debate text:\n")
text = input("> ")

#print(translate(text))

try:
    result = translate(text)
    print("\nValidated Structure:\n")
    print(result.model_dump_json(indent=2))
except ValidationError as e:
    print("\n❌ Schema validation failed:")
    print(e)
except Exception as e:
    print("\n❌ Error:")
    print(e)