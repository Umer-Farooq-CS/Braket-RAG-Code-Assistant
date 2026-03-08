import sys
import os
from pathlib import Path
import cirq

# Add project root to path
# Assuming we run this from project root
project_root = Path(".").resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.cirq_rag_code_assistant.config import get_config, setup_logging
from src.agents.optimizer import OptimizerAgent

# Setup logging
setup_logging()

# Initialize Agent
print("Initializing Optimizer Agent...")
optimizer = OptimizerAgent()
print("Optimizer Agent initialized.")

# Create Sample Circuit
q0, q1 = cirq.LineQubit.range(2)
circuit = cirq.Circuit(
    cirq.X(q0),
    cirq.X(q0),  # Redundant (Identity)
    cirq.Z(q1),
    cirq.Z(q1),  # Redundant (Identity)
    cirq.CNOT(q0, q1),
    cirq.CNOT(q0, q1), # Redundant (Identity)
    cirq.H(q0),
    cirq.H(q0)   # Redundant (Identity)
)

print("\nOriginal Circuit:")
print(circuit)

# LLM Optimization
print("\n" + "="*40)
print("Running LLM Optimization...")
print("="*40)

llm_task = {
    "circuit": circuit,
    "use_llm": True,
    "use_heuristics": False,
    "use_rl": False
}

try:
    llm_result = optimizer.execute(llm_task)
    
    if llm_result['success']:
        print("Successfully optimized circuit using LLM!")
        print("\nLLM Optimized Circuit:")
        print("-" * 40)
        print(llm_result['optimized_code'])
        print("-" * 40)
        
        # Check for explanation
        explanation = llm_result.get('explanation')
        if explanation:
            print("\nExplanation:")
            print("-" * 40)
            print(explanation)
            print("-" * 40)
        else:
            print("\nWARNING: No explanation returned (JSON parsing might have failed or model is legacy)")
        
        print("\nLLM Metrics:")
        print(f"Depth: {llm_result['optimized_metrics'].get('depth')}")
        print(f"Gate Count: {llm_result['optimized_metrics'].get('num_operations')}")
    else:
        print(f"LLM optimization failed: {llm_result.get('error')}")

except Exception as e:
    print(f"Error executing LLM task: {e}")
