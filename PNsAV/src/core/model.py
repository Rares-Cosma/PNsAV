import os
import openai

class Model:

    def __init__(self, prompt_path):
        """
        Initialize the Model class with the specified prompt path.
        
        Parameters:
        - prompt_path: Path to the directory containing prompt files.
        
        The constructor reads the prompt files (atom_prompt.txt, rule_prompt.txt, arg_prompt.txt, attack_prompt.txt)
        and stores their contents in instance variables for later use. It also initializes the OpenAI client for making API calls.
        """
        self.prompt_path = prompt_path
        self.client = openai.OpenAI()

        self.ATOM_PROMPT = ""
        with open(os.path.join(prompt_path, "atom_prompt.txt"), "r", encoding="utf-8") as f:
            self.ATOM_PROMPT = f.read()

        self.RULE_PROMPT = ""
        with open(os.path.join(prompt_path, "rule_prompt.txt"), "r", encoding="utf-8") as f:
            self.RULE_PROMPT = f.read()

        self.ARG_PROMPT = ""
        with open(os.path.join(prompt_path, "arg_prompt.txt"), "r", encoding="utf-8") as f:
            self.ARG_PROMPT = f.read()

    def run_agent(self, agent_id, data, schema, system_prompt):
        """
        Run the specified agent with the provided data and schema.
        
        Parameters:
        - agent_id: Identifier for the agent to run.
        - data: Input data for the agent.
        - schema: JSON schema for validating the agent's output.
        - system_prompt: System prompt to guide the agent's behavior.
        
        Returns:
        - The agent's response as a string, following the specified JSON schema.
        """

        messages = [{"role": "system", "content": system_prompt}]
    
        for t in data:
            messages.append({"role": "user", "content": t})

        response = self.client.chat.completions.create(
            model=agent_id,
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