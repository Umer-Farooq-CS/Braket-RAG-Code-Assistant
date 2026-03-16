"""
Test script: send one prompt to each AWS Bedrock Nova model (Designer, Validator, Optimizer, Educational)
and print the response. Run from project root with .env set (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION).

Where to set model behavior (instead of Ollama Modelfiles):
  - Model IDs, temperature, max_tokens: config/config.json under agents.designer.model, agents.optimizer.model,
    agents.validator.model, agents.educational.model. Add "temperature" and "max_tokens" under each if you want.
  - System prompts (the "custom instructions" you had in Modelfiles): in code —
    src/rag/generator.py (Designer/Optimizer), src/agents/validator.py (_format_llm_prompt / Converse),
    src/agents/educational.py (_call_llm). Pass system=[{"text": "..."}] in the Converse call to set role/instructions.
"""

import sys
from pathlib import Path

# Ensure project root is on path so config and .env load
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Load config (this also runs load_dotenv from config_loader)
from config import get_config
config = get_config()

from src.braket_rag_code_assistant.bedrock_client import get_bedrock_runtime_client

# Model IDs and prompts from config + one prompt per agent role
AWS = config.get("aws", {})
MODELS = AWS.get("models", {})
AGENTS = config.get("agents", {})

DESIGNER_MODEL = AGENTS.get("designer", {}).get("model", {}).get("model") or MODELS.get("designer", "amazon.nova-pro-v1:0")
VALIDATOR_MODEL = AGENTS.get("validator", {}).get("model", {}).get("model") or MODELS.get("validator", "amazon.nova-premier-v1:0")
OPTIMIZER_MODEL = AGENTS.get("optimizer", {}).get("model", {}).get("model") or MODELS.get("optimizer", "amazon.nova-pro-v1:0")
EDUCATIONAL_MODEL = AGENTS.get("educational", {}).get("model", {}).get("model") or MODELS.get("educational", "amazon.nova-2-lite-v1:0")

# One prompt per agent (same style as you'd use in the app)
PROMPTS = {
    "designer": "Write a short Amazon Braket Python script for a 2-qubit Bell state circuit. Use Circuit().h(0).cnot(0,1) and print the circuit.",
    "validator": "This code has a bug: it creates a circuit but never assigns it to a variable named 'circuit'. Fix it: Circuit().h(0).cnot(0,1)",
    "optimizer": "Suggest one specific optimization for a Braket circuit that has many consecutive single-qubit gates on the same qubit. One short paragraph.",
    "educational": "Explain in 2–3 sentences what a Bell state is in quantum computing, for a beginner.",
}

# System prompts (like your Ollama Modelfiles) — can also add temperature/max_tokens from config per agent
SYSTEM_PROMPTS = {
    "designer": "You are an expert Amazon Braket quantum computing programmer. Generate syntactically correct, executable Braket code. Reply with code only when asked for code.",
    "validator": "You are a code review and debugging expert for Amazon Braket. Fix or improve the given code and explain briefly.",
    "optimizer": "You are an expert in quantum circuit optimization for Amazon Braket. Give concise, actionable advice.",
    "educational": "You are a quantum computing educator. Explain clearly and concisely; use markdown if helpful.",
}

def get_model_params(agent_key: str):
    """Get max_tokens and temperature from config for an agent, or defaults."""
    cfg = AGENTS.get(agent_key, {}).get("model", {})
    return {
        "max_tokens": cfg.get("max_tokens", 2000),
        "temperature": cfg.get("temperature", 0.2),
    }


def call_model(model_id: str, user_message: str, system_text: str, max_tokens: int = 2000, temperature: float = 0.2) -> str:
    client = get_bedrock_runtime_client(read_timeout=120)
    response = client.converse(
        modelId=model_id,
        messages=[{"role": "user", "content": [{"text": user_message}]}],
        system=[{"text": system_text}],
        inferenceConfig={"maxTokens": max_tokens, "temperature": temperature},
    )
    return response["output"]["message"]["content"][0]["text"]


def main():
    print("Testing AWS Bedrock Nova models (one prompt per agent). Ensure .env has AWS credentials.\n")

    tests = [
        ("Designer (Nova Pro)", DESIGNER_MODEL, PROMPTS["designer"], SYSTEM_PROMPTS["designer"], "designer"),
        ("Validator (Nova Premier)", VALIDATOR_MODEL, PROMPTS["validator"], SYSTEM_PROMPTS["validator"], "validator"),
        ("Optimizer (Nova Pro)", OPTIMIZER_MODEL, PROMPTS["optimizer"], SYSTEM_PROMPTS["optimizer"], "optimizer"),
        ("Educational (Nova Lite)", EDUCATIONAL_MODEL, PROMPTS["educational"], SYSTEM_PROMPTS["educational"], "educational"),
    ]

    for label, model_id, user_msg, system_text, agent_key in tests:
        print("=" * 60)
        print(f"  {label}  |  {model_id}")
        print("=" * 60)
        params = get_model_params(agent_key)
        try:
            out = call_model(model_id, user_msg, system_text, params["max_tokens"], params["temperature"])
            print(out.strip() or "(empty response)")
        except Exception as e:
            print(f"  ERROR: {e}")
        print()

    print("Done.")


if __name__ == "__main__":
    main()
