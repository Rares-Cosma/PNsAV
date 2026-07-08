"""
This module only tests atom correctness.
Acest modul testeaza doar corectitudinea propozitiilor.
"""

import openai
from schema import atom_schema, rule_schema, argument_schema
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

atom_path = BASE_DIR / "agents_prompts" / "atom_prompt.txt"
rule_path = BASE_DIR / "agents_prompts" / "rule_prompt.txt"
arg_path = BASE_DIR / "agents_prompts" / "arg_prompt.txt"
attack_path = BASE_DIR / "agents_prompts" / "attack_prompt.txt"

ATOM_PROMPT = ""
with open(atom_path, "r", encoding="utf-8") as f:
    ATOM_PROMPT = f.read()

RULE_PROMPT = ""
with open(rule_path, "r", encoding="utf-8") as f:
    RULE_PROMPT = f.read()

ARG_PROMPT = ""
with open(arg_path, "r", encoding="utf-8") as f:
    ARG_PROMPT = f.read()

ATTACK_PROMPT = ""
with open(attack_path, "r", encoding="utf-8") as f:
    ATTACK_PROMPT = f.read()

client = openai.OpenAI()

def respond(text_list, system_prompt: str, schema: dict):
    """
    text_list: list of strings to be sent to the LLM
    system_prompt: string to be used as the system prompt for the LLM
    schema: dictionary representing the JSON schema for the expected response format
    
    Returns the LLM's response as a string, following the JSON schema.
    Returneaza raspunsul LLM ca un sir de caractere, respectand structura JSON.
    """
    messages = [{"role": "system", "content": system_prompt}]
    
    for t in text_list:
        messages.append({"role": "user", "content": t})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=messages,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "argument_framework",
                "strict": True,
                "schema": schema
            }
        }
    )

    return response.choices[0].message.content.strip()

def get_atoms(text):
    atoms=respond([text], ATOM_PROMPT, atom_schema)
    return atoms