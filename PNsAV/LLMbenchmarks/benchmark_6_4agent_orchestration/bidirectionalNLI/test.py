import json
import os
from pathlib import Path
from model import get_atoms
import openai
import re

client = openai.OpenAI()

DOC_EVAL_SYSTEM_PROMPT = """
You are an expert logician grading an Argument Mining pipeline.
Your task is to compare a FULL original text against a complete set of formally abstracted atomic propositions extracted from it.

CRITERIA FOR ENTAILMENT:
1. ALLOWED ABSTRACTIONS: The atoms will drop conversational fluff, resolve pronouns across sentences, and flatten rhetorical modifiers (e.g., "urgently", "simply"). Do not penalize for this.
2. FORWARD ENTAILMENT (Text -> Atoms): Are all the facts stated in the atoms logically supported by the original text? (Return false ONLY if the atoms hallucinate new, unstated premises or outside knowledge).
3. BACKWARD ENTAILMENT (Atoms -> Text): Do the combined atoms capture the core argumentative claims and critical constraints of the entire original text? (Return false ONLY if the atoms completely drop a critical condition, target, or the primary conclusion).

Output strictly in this JSON schema:
{
    "forward_entailment": boolean,
    "backward_entailment": boolean,
    "reasoning": "A 1-sentence explanation of your verdict."
}
"""

def evaluate_doc_with_llm(full_text, all_atoms_text):
    """Uses GPT-4o-mini to judge logical entailment at the document level."""
    user_prompt = f"Original Text: '{full_text}'\nExtracted Atoms:\n{all_atoms_text}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": DOC_EVAL_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content.strip())

BASE_DIR = Path(__file__).resolve().parent.parent
data_path = BASE_DIR / "benchmark_data" / "argmicrotexts_gold_standard.json"

with open(data_path, "r") as f:
    data = json.load(f)

early_stop = 150

total_documents = 0
forward_entailed_docs = 0
backward_entailed_docs = 0
strict_equivalence_docs = 0

print("Starting Document-Level LLM-Judge Evaluation...\n")

for full_text, meta in data.items():
    if early_stop <= 0:
        break
    
    total_documents += 1
    
    raw_atoms_response = json.loads(get_atoms(re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', full_text)))
    generated_atoms = [atom["text"] for atom in raw_atoms_response["atoms"]]
    
    all_atoms_text = "\n".join([f"- {atom}" for atom in generated_atoms])
    
    eval_result = evaluate_doc_with_llm(full_text, all_atoms_text)
    
    f_is_entailment = eval_result["forward_entailment"]
    b_is_entailment = eval_result["backward_entailment"]
    
    if f_is_entailment:
        forward_entailed_docs += 1
    if b_is_entailment:
        backward_entailed_docs += 1
    if f_is_entailment and b_is_entailment:
        strict_equivalence_docs += 1
        
    if not (f_is_entailment and b_is_entailment):
        print("\n--- DOCUMENT ENTAILMENT FAILURE ---")
        print(f"Original Text: {full_text}")
        print(f"Forward: {f_is_entailment}  |  Backward: {b_is_entailment}")
        print(f"Judge Reasoning: {eval_result['reasoning']}")

    early_stop -= 1

forward_rate = (forward_entailed_docs / total_documents) * 100 if total_documents else 0
backward_rate = (backward_entailed_docs / total_documents) * 100 if total_documents else 0
strict_rate = (strict_equivalence_docs / total_documents) * 100 if total_documents else 0

print("\n" + "="*50)
print("FINAL METRICS (DOCUMENT-LEVEL)")
print("="*50)
print(f"Total Documents Evaluated: {total_documents}\n")

print(f"Forward Entailment (No Hallucinations): {forward_rate:.1f}%")
print(f"Backward Entailment (Core Argument Retained): {backward_rate:.1f}%")
print(f"Strict Equivalence (Perfect Global Translation): {strict_rate:.1f}%")