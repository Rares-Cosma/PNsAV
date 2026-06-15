atom_schema = {
    "type": "object",
    "properties": {
        "atoms": {
            "type": "array",
            "description": "Unique atomic propositions extracted from the text.",
            "items": {
                "type": "object",
                "properties": {
                    "id": { "type": "string", "description": "e.g., a1, a2" },
                    "text": { "type": "string", "description": "The literal text of the proposition." },
                    "kb_type": { "type": "string", "enum": ["axiom", "premise"] },
                    "source_quote": { 
                        "type": "string", 
                        "description": "The EXACT verbatim substring from the original text that justifies this atom. Do not alter the words." 
                    }
                },
                "required": ["id", "text", "kb_type", "source_quote"],
                "additionalProperties": False
            }
        }
    },
    "required": ["atoms"],
    "additionalProperties": False
}


rule_schema = {
    "type": "object",
    "properties": {
        "rules": {
            "type": "array",
            "description": "Rules extracted from the text.",
            "items": {
                "type": "object",
                "properties": {
                    "id": { "type": "string", "description": "e.g., r1, r2" },
                    "conclusion": { "type": "string", "description": "e.g., a1, a2" },
                    "premises": { 
                        "type": "array", 
                        "description": "The IDs of the atoms required to fire this rule.",
                        "items": {"type": "string"},
                        "minItems": 1 
                    },
                    "type": { "type": "string", "enum": ["strict", "defeasible"] }
                },
                "required": ["id", "conclusion", "premises", "type"],
                "additionalProperties": False
            }
        }
    },
    "required": ["rules"],
    "additionalProperties": False
}


argument_schema = {
    "type": "object",
    "properties": {
        "scratchpad": {
            "type": "string",
            "description": "Step-by-step mapping of the text to the graph. 1. List all Base Atoms (Level 0). 2. Identify the explicit flawed/valid reasoning steps in the text. 3. Track the Argument IDs and Leaf Premises before writing the JSON."
            
        },
        "arguments": {
            "type": "array",
            "description": "The complete set of formal arguments derived from atoms and rules.",
            "items": {
                "type": "object",
                "properties": {
                    "id": { "type": "string", "description": "e.g., A1, A2" },
                    "conclusion": { "type": "string", "description": "The ID of the atom this argument supports." },
                    "top_rule": { 
                        "type": ["string", "null"], 
                        "description": "The ID of the final rule applied (null if the argument is a base atom)." 
                    },
                    "sub_arguments": { 
                        "type": "array", 
                        "description": "The IDs of the arguments used to satisfy the top_rule's premises.",
                        "items": {"type": "string"}
                    },
                    "type": { "type": "string", "enum": ["atomic", "strict", "defeasible"] }
                },
                "required": ["id", "conclusion", "top_rule", "sub_arguments", "type"],
                "additionalProperties": False
            }
        }
    },
    "required": ["arguments", "scratchpad"],
    "additionalProperties": False
}