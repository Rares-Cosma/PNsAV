import json
import ollama

# -----------------------------
# PROMPT
# -----------------------------

SYSTEM_PROMPT = ""
with open("PNsAV\global_system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()


# -----------------------------
# TRANSLATOR FUNCTION
# -----------------------------

def respond(text: str):
    response = ollama.chat(
        model="qwen2.5:14b",
        format="json",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        options={"temperature": 0}
    )

    raw_output = response["message"]["content"].strip()

    return raw_output

# -----------------------------
# MAIN
# -----------------------------

print("Enter debate text:\n")
text = input("> ")

print(respond(text))