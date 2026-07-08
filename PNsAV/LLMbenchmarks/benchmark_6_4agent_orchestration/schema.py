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
        "scratchpad": {
            "type": "object",
            "description": "Pre-parsing analysis zone to isolate logical components before writing syntax rules.",
            "properties": {
                "extracted_connectors": {
                    "type": "array",
                    "description": "List every explicit forward/backward trigger word found in the text (e.g., 'because', 'if', 'therefore').",
                    "items": {"type": "string"}
                },
                "disjunction_split_plan": {
                    "type": "string",
                    "description": "Identify any 'OR' triggers and explicitly state how many separate rules they must split into (per Principle 5)."
                },
                "inversion_check": {
                    "type": "string",
                    "description": "Identify structural keywords like 'requires' and plan the correct directional mapping (per Principle 11)."
                },
                "conflict_check": {
                    "type": "string",
                    "description": "Identify explicitly opposing atoms (contraries) or explicit rule exceptions (undercutters)."
                }
            },
            "required": ["extracted_connectors", "disjunction_split_plan", "inversion_check", "conflict_check"],
            "additionalProperties": False
        },
        "rules": {
            "type": "array",
            "description": "Rules extracted from the text based strictly on the scratchpad mapping plan.",
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
        },
        "conflicts": {
            "type": "object",
            "description": "Explicit logical conflicts extracted for ASPIC+ evaluation.",
            "properties": {
                "contraries": {
                    "type": "array",
                    "description": "Pairs of Atom IDs that represent mutually exclusive or directly opposite conclusions.",
                    "items": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 2,
                        "maxItems": 2
                    }
                },
                "undercutters": {
                    "type": "array",
                    "description": "Atoms that act as exceptions, attacking the application of a specific rule.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "attacker": { "type": "string", "description": "The Atom ID acting as the exception." },
                            "target_rule": { "type": "string", "description": "The Rule ID (e.g., 'r1') being attacked by the exception." }
                        },
                        "required": ["attacker", "target_rule"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["contraries", "undercutters"],
            "additionalProperties": False
        }
    },
    "required": ["scratchpad", "rules", "conflicts"],
    "additionalProperties": False
}

argument_schema = {
    "type": "object",
    "properties": {
        "scratchpad": {
            "type": "object",
            "properties": {
                "text_connectors_found": {
                    "type": "array",
                    "description": "List every single explicit logical trigger found in the text (e.g., 'because', 'therefore', 'if').",
                    "items": { "type": "string" }
                },
                "rule_firing_verification": {
                    "type": "string",
                    "description": "A clear description of which parsed rules successfully fire given the active premises, and why others fail."
                }
            },
            "required": ["text_connectors_found", "rule_firing_verification"],
            "additionalProperties": False
        },
        "arguments": {
            "type": "array",
            "description": "The complete derivation tree. Conclusion must name an atom ID (e.g., a1, a2). top-rule: the rule ID that directly supports this argument, or null if it's an atomic argument. sub-arguments: the IDs of the arguments that support this one. (eg. A1, A2)",
            "items": {
                "type": "object",
                "properties": {
                    "id": { "type": "string" },
                    "conclusion": { "type": "string" },
                    "top_rule": { "type": ["string", "null"] },
                    "sub_arguments": { "type": "array", "items": {"type": "string"} },
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