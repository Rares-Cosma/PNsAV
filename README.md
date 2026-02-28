<h1 align="center">PNsAV</h1>
<h3 align="center">Probabilistic Neurosymbolic Argument Validation Model</h3>

## Abstract
PNsAV is a multi-layer neurosymbolic reasoning system designed to perform formal validation of argument structures extracted from natural language. A constrained large language model is employed as a semantic parser, identifying argumentative units, inferential relations, and domain concepts, in consideration of the ontological characteristics of the concepts.These structured arguments are processed by a set of formal validation layers implementing non-monotonic and defeasible reasoning, combined with a probabilistic extension of formal logic. The validation process includes local structural consistency checks and global argument acceptability evaluation. The system identifies logical fallacies, invalid inference patterns, and unsupported conclusions, producing an explicit symbolic explanation of detected errors. PNsAV aims to bridge the gap between statistical language models and formal logic by enforcing explicit logical constraints on natural language reasoning. By integrating formal verification methods with statistical language models, PNsAV provides an alternative to constrained, symbolic reasoning engines or pure neural systems, offering improved stability, predictability, and correctness.

## Text parsing with LLM's
The purpose of this system is to formally verify argument structures, reducing the error of a fully neural system, with the help of symbolic reasoning, used as the "brain" of the model, constraining the neural layer (LLM) to only act as a parser.

In PNsAV, the translation from natural language to an **ASPIC+ like** representation is done in Python, with the help of Ollama and OpenAI.

Early tests concluded that small, local models (phi3:mini, llama3) fail at parsing, as they try to explain their response, introduce made up logic and miss logical errors they've made. A more stable model was found to be **Qwen 2.5 14B**.

Two benchmarks were done after modifying the prompt, testing the system's **variance, stability and accuracy**. A third one tested the model's accuracy between 5 different types of arguments (different types of flaws, including semantic and structural ones), and concluded that prompt-engineering is not enough for a precise parser. As you can see, the model performs good on correct arguments, and rule type detection, but underperforms at sophysms or arguments with logical fallacies.

The first attempt at correcting this inaccurate parser layer is using another LLM prompted with the task of detecting unexpected behaviour of the first one. Benchmarks 3 and 4 showcase the differences between the 2 systems.

By using OpenAI's **GPT-4o-mini** we improve performance, as seen in benchmark 5, but the parser still remains unreliable for extended use. We can switch to a 4 mixed-weight agent orchestration, reducing internal biases towards correcting logic.