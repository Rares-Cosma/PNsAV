import json
import ollama
import openai

client = openai.OpenAI()

# -----------------------------
# PROMPT
# -----------------------------

SYSTEM_PROMPT = ""
with open("PNsAV/global_system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

VALIDATE_PROMPT = ""
with open("PNsAV/validity_check_prompt.txt", "r", encoding="utf-8") as f:
    VALIDATE_PROMPT = f.read()


# -----------------------------
# TRANSLATOR FUNCTION
# -----------------------------

def respond(text: str, system_prompt: str):
    response = client.responses.create(
        model="gpt-4o-mini",
        temperature=0,
        input=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": text,
            }
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "argument_framework",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "atoms": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "text": {"type": "string"}
                                },
                                "required": ["id", "text"],
                                "additionalProperties": False
                            }
                        },
                        "rules": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "type": {
                                        "type": "string",
                                        "enum": ["strict", "defeasible"]
                                    },
                                    "premises": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "conclusion": {"type": "string"}
                                },
                                "required": ["id", "type", "premises", "conclusion"],
                                "additionalProperties": False
                            }
                        },
                        "arguments": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "premises": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "applied_rules": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "conclusion": {"type": "string"},
                                    "sub_arguments": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                },
                                "required": ["id", "premises", "applied_rules", "conclusion", "sub_arguments"],
                                "additionalProperties": False
                            }
                        },
                        "attacks": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "attacker": {"type": "string"},
                                    "target": {"type": "string"},
                                    "type": {
                                        "type": "string",
                                        "enum": ["rebut", "undercut"]
                                    }
                                },
                                "required": ["attacker", "target", "type"],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["atoms", "rules", "arguments", "attacks"],
                    "additionalProperties": False
                }
            }
        }
    )

    return response.output_text.strip()


# -----------------------------
# MAIN
# -----------------------------

print("Enter debate text:\n")
text = input("> ")

primary_output = respond(text, SYSTEM_PROMPT)
print(primary_output)

validated_output = respond(primary_output, VALIDATE_PROMPT)
print(validated_output)