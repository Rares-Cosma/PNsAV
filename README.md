<h1 align="center">PNsAV</h1>
<h3 align="center">Probabilistic Neurosymbolic Argument Validation Model</h3>

## Abstract
PNsAV is a multi-layer neurosymbolic reasoning system designed to perform formal validation of argument structures extracted from natural language. A constrained large language model orchestration is employed as a semantic parser, identifying argumentative units, inferential relations, and domain concepts, in consideration of the ontological characteristics of the concepts. These structured arguments are processed by a set of formal validation layers implementing non-monotonic and defeasible reasoning, combined with a probabilistic extension of formal logic. The validation process includes local structural consistency checks and global argument acceptability evaluation. The system identifies logical fallacies, invalid inference patterns, and unsupported conclusions, producing an explicit symbolic explanation of detected errors. PNsAV aims to bridge the gap between statistical language models and formal logic by enforcing explicit logical constraints on natural language reasoning. By integrating formal verification methods with statistical language models, PNsAV provides an alternative to constrained, symbolic reasoning engines or pure neural systems, offering improved stability, predictability, and correctness in the analysis of arguments and their relations.

## Related work

## Technical details
In PNsAV, the translation from natural language to an **ASPIC+** representation **[2]** is done in Python, with the help of Ollama and OpenAI **[3]**.

## Text parsing with LLMs
The purpose of this system is to formally verify argument structures, reducing the error of a fully neural system, with the help of symbolic reasoning, used as the "brain" of the model, constraining the neural layer (LLM) to only act as a parser.

Early tests concluded that small, local models (phi3:mini, llama3 7B) fail at parsing, as they try to explain their response, essentially breaking the JSON schema, introduce made up logic and miss logical errors they've made. A more stable model was found to be **Qwen 2.5 14B [4]**.

Two benchmarks were done after modifying the prompt, testing the system's **variance, stability and accuracy**. A third one tested the model's accuracy between 5 different types of arguments (different types of flaws, including semantic and structural ones), and concluded that prompt-engineering **[6]** is not enough for a precise parser, when using small models. As you can see, the model performs good on correct arguments, and rule type detection, but underperforms at sophisms or arguments with logical fallacies, concluding a tendency of the model to *fix* the logic, instead of translating it.

The first attempt at correcting this inaccurate parser layer is using another LLM prompted with the task of detecting unexpected behaviour of the first one (benchmarks 4 and 5). The results showcase a bias of the verification layer to *overcorrect* the parsing, either by removing valid translation, or by introducing unspecified logic.

By using OpenAI's **GPT-4o-mini [3]** we improve performance, as seen in benchmark 5, but the parser still remains unreliable for extended use. The obvious path is to switch to a 3 mixed-weight agent orchestration, reducing internal biases towards correcting logic.

The first agent is trained to identify atoms, break down conditional and relational sentences and decide the *knowledge base* label (axiom/premise). The second is tasked with providing the rules of the framework **[2]**, and determining if they are **strict** or **defeasible**, while the third extracts the arguments, and their corresponding meta-data (such as the top rule and subarguments).

Assessing the translating layer's performance, we've tested the results against a ground truth dataset compiled from the **arg-microtexts** corpus **[1]**. The correctness of the atoms was tested using a LLM judging **[5]** approach, as the generated atoms present noticeable discrepancies from the Elementary Discourse Units (EDUs) present in the dataset in terms of semantic and linguistic structure. LLM judging is crucial for validation as it computes the entailment between the standard EDUs and their corresponding generated atoms, showcasing information loss (recall) and hallucinations (precision) of our translator. 

The bidirectional entailment judging extracted these results across 112 documents:
* Forward Entailment (No Hallucinations): 96.4%
* Backward Entailment (Core Argument Retained): 90.2%
* Strict Equivalence (Perfect Global Translation): 90.2%

An error of +/- 5% has to be taken into consideration because of the volatility that the judging LLM presents.

## Bibliography

**[1]** A. Peldszus and M. Stede, "An annotated corpus of argumentative microtexts," in *Proc. 1st European Conf. Argumentation*, Lisbon, Portugal, 2015, pp. 801–815.

**[2]** S. Modgil and H. Prakken, "The ASPIC+ framework for structured argumentation: A tutorial," *Argument & Computation*, vol. 5, no. 1, pp. 31–62, 2014.

**[3]** OpenAI, "GPT-4o-mini: Advancing cost-efficient intelligence," 2024. [Online]. Available: https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/

**[4]** Qwen Team, "Qwen2.5: A Party of Foundation Models," *Qwen Blog*, 2024. [Online]. Available: https://qwenlm.github.io/blog/qwen2.5/

**[5]** L. Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena," *arXiv preprint arXiv:2306.05685*, 2023.

**[6]** J. Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models," in *Proc. NeurIPS*, 2022.