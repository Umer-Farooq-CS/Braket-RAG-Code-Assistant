"""
Validator Agent Test Suite

This module contains a test suite of 20+ Braket code snippets with various categories of errors
(Syntax, Logic, Import, Runtime) derived from the project's Codes.txt examples.

It is designed to be run from the Validator Agent notebook to verify the agent's
ability to detect errors and fix them using the LLM.

Author: Umer Farooq
"""

import time
from typing import List, Dict, Any
import pandas as pd
import logging
import os
import sys
from loguru import logger
from src.agents.validator import ValidatorAgent

def setup_logging():
    """Configure detailed logging to file using Loguru."""
    log_file = os.path.join(os.path.dirname(__file__), 'test_execution.log')
    
    try:
        logger.remove()
    except ValueError:
        pass
        
    logger.add(
        log_file,
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        rotation="10 MB",
        mode="w"
    )
    
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>"
    )
    
    print(f"📝 Logging execution details to: {log_file}")

# ==============================================================================
# TEST CASES
# ==============================================================================

TEST_CASES = [
    # --- GROUP 1: QUANTUM TELEPORTATION ---
    {
        "name": "Teleportation - Valid",
        "description": "Standard Teleportation circuit using Braket SDK",
        "expected_status": "PASS",
        "code": """
from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0)
# Bell pair
circuit.h(1)
circuit.cnot(1, 2)
circuit.cnot(0, 1)
circuit.h(0)
# Measurements
circuit.measure(0)
circuit.measure(1)
circuit.measure(2)
"""
    },
    {
        "name": "Teleportation - Missing Import",
        "description": "Using Circuit without importing it",
        "expected_status": "FAIL",
        "code": """
# Missing import
circuit = Circuit()
circuit.h(0)
"""
    },
    {
        "name": "Teleportation - Typo in Module",
        "description": "Typo 'Circuite' instead of 'Circuit'",
        "expected_status": "FAIL",
        "code": """
from braket.circuits import Circuit
circuit = Circuite()
circuit.h(0)
"""
    },
    {
        "name": "Teleportation - Undefined Variable",
        "description": "Using undefined variable q3",
        "expected_status": "FAIL",
        "code": """
from braket.circuits import Circuit
circuit = Circuit()
# q3 is not defined
circuit.cnot(1, q3)
"""
    },
    {
        "name": "Teleportation - Syntax Error",
        "description": "Missing closing parenthesis",
        "expected_status": "FAIL",
        "code": """
from braket.circuits import Circuit
circuit = Circuit(
# Missing closing paren above
"""
    },

    # --- GROUP 2: DEUTSCH-JOZSA ---
    {
        "name": "Deutsch-Jozsa - Valid",
        "description": "Standard DJ circuit for 2 qubits using Braket",
        "expected_status": "PASS",
        "code": """
from braket.circuits import Circuit
circuit = Circuit()
circuit.x(2)
for q in [0, 1, 2]:
    circuit.h(q)
# Oracle
circuit.cnot(0, 2)
circuit.cnot(1, 2)
# Final H
for q in [0, 1]:
    circuit.h(q)
circuit.measure(0)
circuit.measure(1)
"""
    },
    {
        "name": "Deutsch-Jozsa - Indentation Error",
        "description": "Python indentation error in loop",
        "expected_status": "FAIL",
        "code": """
from braket.circuits import Circuit
circuit = Circuit()
for i in range(3):
circuit.h(i) # Indentation Error
"""
    },
    {
        "name": "Deutsch-Jozsa - Wrong Gate Usage",
        "description": "Passing extra argument to H gate",
        "expected_status": "FAIL",
        "code": """
from braket.circuits import Circuit
circuit = Circuit()
# H gate takes a single qubit index
circuit.h(3.14, 0)
"""
    },
    {
        "name": "Deutsch-Jozsa - Logic/Type Error",
        "description": "Passing a string instead of qubit index",
        "expected_status": "FAIL",
        "code": """
from braket.circuits import Circuit
circuit = Circuit()
# 'zero' is not a valid qubit index
circuit.h("zero")
"""
    },
    {
        "name": "Deutsch-Jozsa - Missing Measurement",
        "description": "Circuit has no measurements",
        "expected_status": "FAIL",
        "code": """
from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0)
circuit.cnot(0, 1)
# No measurement
"""
    },

    # --- GROUP 3: QRNG ---
    {
        "name": "QRNG - Valid",
        "description": "Simple QRNG circuit using Braket",
        "expected_status": "PASS",
        "code": """
from braket.circuits import Circuit
circuit = Circuit()
for q in range(4):
    circuit.h(q)
    circuit.measure(q)
"""
    },
    {
        "name": "QRNG - Type Error in Range",
        "description": "Passing string to range",
        "expected_status": "FAIL",
        "code": """
from braket.circuits import Circuit
# String instead of int
for q in range("4"):
    pass
circuit = Circuit()
"""
    },
    {
        "name": "QRNG - Valid Measure",
        "description": "Braket measure on qubit index",
        "expected_status": "PASS",
        "code": """
from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0)
circuit.measure(0)
"""
    },
    {
        "name": "QRNG - Wrong Attribute",
        "description": "Typo in import path",
        "expected_status": "FAIL",
        "code": """
# Wrong import path
from braket.circuitss import Circuit
circuit = Circuit()
"""
    },
    {
        "name": "QRNG - Logic Error (No Superposition)",
        "description": "Measuring |0> without H gate",
        "expected_status": "PASS",
        "code": """
from braket.circuits import Circuit
circuit = Circuit()
# Missing H gate - will always measure 0
circuit.measure(0)
"""
    },

    # --- GROUP 4: GROVER'S SEARCH ---
    {
        "name": "Grover - Valid",
        "description": "Simple 2-qubit Grover using Braket",
        "expected_status": "PASS",
        "code": """
from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0)
circuit.h(1)
circuit.cz(0, 1)
circuit.h(0)
circuit.h(1)
circuit.x(0)
circuit.x(1)
circuit.cz(0, 1)
circuit.x(0)
circuit.x(1)
circuit.h(0)
circuit.h(1)
circuit.measure(0)
circuit.measure(1)
"""
    },
    {
        "name": "Grover - Argument Mismatch",
        "description": "CZ gate expects 2 qubits",
        "expected_status": "FAIL",
        "code": """
from braket.circuits import Circuit
circuit = Circuit()
# CZ needs 2 args
circuit.cz(0)
"""
    },
    {
        "name": "Grover - Variable Name Typo",
        "description": "Using 'qc' instead of 'circuit'",
        "expected_status": "FAIL",
        "code": """
from braket.circuits import Circuit
circuit = Circuit()
# 'qc' is not defined
qc.h(0)
"""
    },
    {
        "name": "Grover - Unsupported Gate",
        "description": "Using imaginary gate",
        "expected_status": "FAIL",
        "code": """
from braket.circuits import Circuit
circuit = Circuit()
# MagicGate doesn't exist
circuit.magic_gate(0)
"""
    },
    {
        "name": "Grover - Invalid Append Type",
        "description": "Calling non-existent method on Circuit",
        "expected_status": "FAIL",
        "code": """
from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0)
# Invalid: append is not a Braket Circuit method
circuit.append("not_a_gate")
"""
    },

    # --- GROUP 5: MISC ---
    {
        "name": "Misc - Empty Code",
        "description": "Empty string",
        "expected_status": "FAIL",
        "code": ""
    },
    {
        "name": "Misc - Natural Language",
        "description": "Not code at all",
        "expected_status": "FAIL",
        "code": "Please create a quantum circuit for me."
    }
]

def run_tests(validator_agent):
    """
    Run the defined test cases using the provided validator agent.
    Returns a DataFrame with results.
    """
    results = []
    setup_logging()
    
    print(f"🚀 Starting Validator Test Suite ({len(TEST_CASES)} cases)...\n")
    
    for i, test in enumerate(TEST_CASES):
        print(f"[{i+1}/{len(TEST_CASES)}] Testing: {test['name']}...", end=" ", flush=True)
        
        start_time = time.time()
        
        task = {
            "code": test["code"],
            "description": test["description"],
            "force_llm_fix": True
        }
        
        try:
            result = validator_agent.execute(task)
            duration = time.time() - start_time
            
            success = result.get("success", False)
            fixed_code = result.get("fixed_code", None)
            validation_attempts = result.get("validation_attempts", 1)
            used_fix_retry = validation_attempts > 1
            
            status = "UNKNOWN"
            if test["expected_status"] == "PASS":
                status = "PASS" if success else "FAIL"
            else:
                if (not success and fixed_code) or (success and used_fix_retry):
                    status = "PASS (Fixed)"
                elif not success:
                    status = "PASS (Detected)"
                else:
                    status = "FAIL (False Positive)"
            
            print(f"-> {status} ({duration:.2f}s)")
            
            results.append({
                "ID": i+1,
                "Name": test["name"],
                "Description": test["description"],
                "Expected": test["expected_status"],
                "Actual_Success": success,
                "Has_Fix": bool(fixed_code),
                "Validation_Attempts": validation_attempts,
                "Status": status,
                "Error_Msg": result.get("error", "")[:50] + "..." if result.get("error") else ""
            })
            
        except Exception as e:
            print(f"-> ERROR (Exception): {e}")
            results.append({
                "ID": i+1,
                "Name": test["name"],
                "Description": test["description"],
                "Expected": test["expected_status"],
                "Actual_Success": False,
                "Has_Fix": False,
                "Status": "ERROR",
                "Error_Msg": str(e)
            })
            
    df = pd.DataFrame(results)
    return df
