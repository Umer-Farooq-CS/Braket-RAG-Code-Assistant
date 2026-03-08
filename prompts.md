# 📝 Generative AI Project - Prompts Log

| **Student** | Umer Farooq |
|-------------|-------------|
| **Roll Number** | 22I-0891 |
| **Project** | Braket-RAG Code Assistant |
| **Description** | Multi-Agent Quantum Circuit Generation System |

---

## Table of Contents
1. [Project Ideation & Planning](#1-project-ideation--planning)
2. [Validator Agent Development](#2-validator-agent-development)
3. [Project Submission Verification](#3-project-submission-verification)
4. [Previous Development Sessions](#4-previous-development-sessions)
5. [Model Selection & Ollama Configuration](#5-model-selection--ollama-configuration)
6. [RAG System Development](#6-rag-system-development)
7. [Agent Architecture & Orchestration](#7-agent-architecture--orchestration)
8. [Debugging & Troubleshooting](#8-debugging--troubleshooting)
9. [Prompt Engineering Techniques](#9-prompt-engineering-techniques)
10. [Quick Reference: All Prompts](#10-quick-reference-all-prompts)

---

## 1. Project Ideation & Planning
*AI Used: DeepSeek*

### Prompt 1.1 - Understanding Project Uniqueness

> ```
> Now understand this proposal and see what I want to do. Then explain to me 
> this, I have already downloaded qwen2.5-coder:14b-instruct-q4_K_M model as 
> my LLM and it generates a nice Braket code as well as other GPTs like ChatGPT 
> and Copilot and Deepseek Claude Gemini all of them give nice codes and the 
> stuff that we are doing.
> 
> Explain to me what can I do there which will make my project actually 
> useful i.e something that these LLMs cant do by default or struggle with etc.
> ```

**Context:** Used to understand what unique value the RAG-based system would provide over vanilla LLM code generation for quantum circuits.

---

## 2. Validator Agent Development
*AI Used: Claude/Antigravity*

### Prompt 2.1 - Knowledge Base Validation

> ```
> Validate Knowledge Base Circuits
> 
> The user's primary objective is to ensure the robustness of the 
> ValidatorAgent's self-correction mechanism and the integrity of the 
> knowledge base circuits. This involves:
> 
> 1. Fixing the ValidatorAgent to trigger LLM-powered code fixing for *all*
>    validation failures, including compilation errors (e.g., ModuleNotFoundError)
>    and cases where no circuit is detected, not just simulation failures.
> 
> 2. Verifying that the system is correctly utilizing the knowledge base for
>    Designer Agent code generation.
> 
> 3. Creating a dedicated test script to systematically run and validate every
>    code example within the curated_designer_examples.jsonl knowledge base,
>    to confirm their correctness and ensure they execute without errors.
> ```

**Context:** Multi-step task to fix validation issues and create KB test script.

---

## 3. Project Submission Verification
*AI Used: Claude/Antigravity*

### Prompt 3.1 - Submission Requirements Check

> ```
> Check if anything is missing from this
> [Project requirements document content...]
> I think we forgot the prompts.txt., check if we missed anything else too
> ```

**Context:** Final verification before project submission.

### Prompt 3.2 - Create Prompts File

> ```
> create a template prompts.txt and add all the prompts that I gave to you 
> above not missing any of them.
> https://chat.deepseek.com/share/24i9j8on0fw03ihyi6
> Also I have added my deepseek chat so use that too
> ```

**Context:** Requested creation of this prompts documentation file.

---

## 4. Previous Development Sessions
*Summarized from conversation history*

| Prompt | Session Date | Description |
|--------|--------------|-------------|
| 4.1 | 2025-12-07 | Updated knowledge base with curated Braket examples |
| 4.2 | 2025-12-07 | Updated notebooks with shared Retriever for RAG |
| 4.3 | 2025-12-06 | Refactored orchestration module and pipeline |
| 4.4 | 2025-12-06 | Implemented custom Ollama Modelfile for designer |
| 4.5 | 2025-12-05 | Enhanced RAG generation demo notebook |
| 4.6 | 2025-12-05 | Implemented hybrid topic scoring for retrieval |
| 4.7 | 2025-12-02 | Completed missing modules and RL optimization |

---

## 5. Model Selection & Ollama Configuration

### Prompt 5.1 - Choosing LLM Provider

> ```
> I want to build a multi-agent system for quantum circuit generation. What 
> are the best options for running LLMs locally? I need something that can 
> run on my machine with a decent GPU (RTX series). Compare Ollama, LM Studio, 
> and vLLM for local deployment. Which one would be easiest to integrate with 
> a Python application?
> ```

**Context:** Selected Ollama for its simple REST API and Python integration.

### Prompt 5.2 - Selecting Models for Different Agents

> ```
> I'm building a multi-agent RAG system with the following agents:
> 1. Designer Agent - generates Braket quantum circuit code from user queries
> 2. Validator Agent - validates and fixes generated code
> 3. Optimizer Agent - optimizes circuits for depth, gate count, etc.
> 4. Educational Agent - explains quantum concepts
> 
> What Ollama models would you recommend for each agent? Consider:
> - Code generation capability (especially for Python/Braket)
> - Instruction following for structured output (JSON)
> - Context window size for RAG retrieval
> - Speed vs accuracy tradeoff
> - My GPU has 8GB VRAM
> ```

**Context:** Selected `qwen2.5-coder:14b-instruct-q4_K_M` for code generation.

### Prompt 5.3 - Configuring Ollama Modelfiles

> ```
> How do I create a custom Ollama Modelfile to configure system prompts and
> generation parameters for my agents? I want:
> - Designer agent to output JSON with "code" and "description" fields
> - Temperature settings for deterministic code generation
> - Specific stop tokens to prevent extra text after JSON
> 
> Show me example Modelfiles for a code generation agent.
> ```

**Context:** Created `config/ollama/designer_agent.Modelfile`.

### Prompt 5.4 - Model Quantization Selection

> ```
> What's the difference between Q4_K_M, Q5_K_M, and Q8_0 quantization for 
> Ollama models? I need to balance quality vs VRAM usage for my 8GB GPU. 
> Which quantization would you recommend for:
> - A 14B parameter coding model (qwen2.5-coder)
> - A 7B parameter general model (llama3.1)
> ```

**Context:** Selected Q4_K_M for 14B model to fit in VRAM.

### Prompt 5.5 - Embedding Model Selection

> ```
> For the RAG system's vector store, what embedding model should I use for
> semantic search over quantum computing code examples? Options:
> - sentence-transformers/all-MiniLM-L6-v2
> - BAAI/bge-small-en
> - nomic-embed-text (via Ollama)
> - OpenAI text-embedding-ada-002
> 
> I want something that works well with code, runs locally, and has good performance.
> ```

**Context:** Selected `all-MiniLM-L6-v2` for balance of speed and quality.

### Prompt 5.6 - Ollama API Integration

> ```
> Show me how to call Ollama's /api/generate endpoint from Python to get
> structured JSON output. I need to:
> - Send a prompt with RAG context
> - Parse the JSON response
> - Handle streaming vs non-streaming modes
> - Set custom parameters like temperature and max_tokens
> ```

**Context:** Implemented `src/rag/generator.py` with proper API calls.

---

## 6. RAG System Development

### Prompt 6.1 - Vector Store Setup

> ```
> How do I set up a ChromaDB vector store for storing quantum circuit code 
> examples? I need to:
> - Store code snippets with metadata (topics, difficulty, algorithm type)
> - Use a local embedding model
> - Support hybrid search (semantic + keyword filtering)
> - Persist the database to disk
> ```

**Context:** Implemented `src/rag/vector_store.py` with ChromaDB.

### Prompt 6.2 - Knowledge Base Curation

> ```
> I need to create a knowledge base of Braket code examples for my RAG system.
> What categories of quantum circuits should I include? Consider:
> - Basic gates and measurements
> - Common algorithms (Grover, Shor, QFT, VQE, QAOA)
> - Error correction codes
> - Hardware-specific optimizations
> 
> How should I structure the JSONL file for easy retrieval?
> ```

**Context:** Designed schema for `curated_designer_examples.jsonl`.

### Prompt 6.3 - Retrieval Strategy

> ```
> What retrieval strategy should I use for my quantum circuit RAG system?
> I want to combine:
> - Semantic similarity (vector search)
> - Topic/keyword matching
> - Difficulty filtering
> 
> How do I implement a hybrid scoring system that boosts results matching
> specific topics mentioned in the query?
> ```

**Context:** Implemented `hybrid_search` with topic boosting in `src/rag/retriever.py`.

---

## 7. Agent Architecture & Orchestration

### Prompt 7.1 - Multi-Agent Pipeline Design

> ```
> Design a multi-agent pipeline for quantum circuit generation:
> 1. Designer generates initial code based on user query + RAG context
> 2. Validator checks if code compiles and runs correctly
> 3. If validation fails, loop back to Designer with error feedback
> 4. Optimizer improves the validated circuit
> 5. Final validation before returning to user
> 
> How should the agents communicate? Should I use a state machine, 
> event-driven architecture, or simple sequential pipeline?
> ```

**Context:** Designed Orchestrator class in `src/orchestration/orchestrator.py`.

### Prompt 7.2 - Self-Correction Mechanism

> ```
> Implement a self-correction mechanism for the Validator agent. When code
> fails to compile or simulate:
> 1. Capture the error message
> 2. Send the code + error to the LLM for fixing
> 3. Retry validation with the fixed code
> 4. Limit retries to prevent infinite loops
> 
> How do I structure the prompt to the LLM to get good code fixes?
> ```

**Context:** Implemented retry loop in `src/agents/validator.py`.

---

## 8. Debugging & Troubleshooting

### Prompt 8.1 - Fixing Braket Deprecated APIs

> ```
> My generated Braket code is using deprecated APIs like braket.circuits.compiler_directives and
> braket.experimental.algorithms.qaoa which don't exist in the current version. How do I:
> 1. Update the knowledge base to use modern Braket syntax
> 2. Add negative examples to prevent the LLM from generating deprecated code
> 3. Use braket.circuits.compiler_directives instead of braket.circuits.compiler_directives
> ```

**Context:** Fixed KB entries and added `modern_api_dont_use_*` examples.

### Prompt 8.2 - Validation Mode Switch

> ```
> My ValidatorAgent is using a remote QCanvas backend but I need local Braket 
> simulation. The config.json says mode="local" but the notebook hardcodes
> mode="remote". How do I:
> 1. Fix the notebook to read from config
> 2. Ensure local Braket simulation works correctly
> 3. Format results to match the expected output structure
> ```

**Context:** Fixed validator mode initialization and local execution logic.

---

## 9. Prompt Engineering Techniques

| Technique | Description | Example |
|-----------|-------------|---------|
| **Context Setting** | Providing background before asking | Explaining multi-agent architecture first |
| **Step-by-Step** | Breaking tasks into numbered steps | "1. Fix... 2. Verify... 3. Create..." |
| **Constraints** | Stating limitations clearly | "must use local Braket, not QCanvas" |
| **References** | Including URLs, paths, snippets | Sharing DeepSeek chat link |
| **Iteration** | Following up to refine | Fixing LLM trigger after feedback |
| **Verification** | Asking AI to validate work | Running tests to confirm fixes |
| **Comparison** | Comparing options | Ollama vs LM Studio analysis |
| **Structured Output** | Specifying exact formats | JSON schema for Modelfiles |

---

## 10. Quick Reference: All Prompts

Below are all prompts without context for quick copy-paste:

---

### Project Ideation
```
Now understand this proposal and see what I want to do. Then explain to me this, 
I have already downloaded qwen2.5-coder:14b-instruct-q4_K_M model as my LLM and 
it generates a nice Braket code as well as other GPTs like ChatGPT and Copilot and 
Deepseek Claude Gemini all of them give nice codes. Explain to me what can I do 
there which will make my project actually useful i.e something that these LLMs 
cant do by default or struggle with etc.
```

---

### Model Selection
```
I want to build a multi-agent system for quantum circuit generation. What are the 
best options for running LLMs locally? Compare Ollama, LM Studio, and vLLM.
```

```
I'm building a multi-agent RAG system with Designer, Validator, Optimizer, and 
Educational agents. What Ollama models would you recommend for each? My GPU has 8GB VRAM.
```

```
How do I create a custom Ollama Modelfile to configure system prompts? I want the 
Designer agent to output JSON with "code" and "description" fields.
```

```
What's the difference between Q4_K_M, Q5_K_M, and Q8_0 quantization? Which for 14B coding model?
```

```
For RAG vector store, what embedding model should I use for code? Compare 
all-MiniLM-L6-v2, bge-small-en, nomic-embed-text, text-embedding-ada-002.
```

```
Show me how to call Ollama's /api/generate endpoint from Python for structured JSON output.
```

---

### RAG System
```
How do I set up ChromaDB vector store for quantum circuit code examples with hybrid search?
```

```
What categories of quantum circuits should I include in my knowledge base? How to structure JSONL?
```

```
What retrieval strategy for hybrid scoring combining semantic + topic/keyword matching?
```

---

### Agent Architecture
```
Design a multi-agent pipeline: Designer → Validator → (retry loop) → Optimizer → Final Validation
```

```
Implement self-correction for Validator: capture error, send to LLM, retry with fixed code.
```

---

### Debugging
```
My Braket code uses deprecated APIs (braket.circuits.compiler_directives, braket.experimental.algorithms.qaoa). How to fix KB?
```

```
ValidatorAgent uses remote backend but should use local Braket. Config says local, notebook says remote.
```

---

### Submission
```
Check if anything is missing from [project requirements]. I think we forgot prompts.txt.
```

```
Create prompts.txt with all the prompts I gave you. Also use my DeepSeek chat link.
```

---

*End of Prompts Document*
