"""
Validator Agent Test Suite

This module contains a test suite of 20+ Cirq code snippets with various categories of errors
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
    
    # Remove default handlers to avoid duplication if re-run
    try:
        logger.remove()
    except ValueError:
        pass
        
    # Add file sink for comprehensive debug logging
    logger.add(
        log_file,
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        rotation="10 MB",
        mode="w"
    )
    
    # Add stderr sink for visibility during test run (optional)
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
        "description": "Standard Teleportation circuit (Separate appends for backend compatibility)",
        "expected_status": "PASS",
        "code": """
import cirq
q0, q1, q2 = cirq.LineQubit.range(3)
circuit = cirq.Circuit()
circuit.append(cirq.H(q0))
# Flattened operations for compatibility
circuit.append(cirq.H(q1))
circuit.append(cirq.CNOT(q1, q2))
circuit.append(cirq.CNOT(q0, q1))
circuit.append(cirq.H(q0))
circuit.append(cirq.measure(q0, key='c0'))
circuit.append(cirq.measure(q1, key='c1'))
# Corrections would happen here in classical control
circuit.append(cirq.measure(q2, key='c2'))
"""
    },
    {
        "name": "Teleportation - Missing Import",
        "description": "Using invalid module to force import error",
        "expected_status": "FAIL",
        "code": """
# Missing import and using non-existent module
q0 = cirq.LineQubit(0)
"""
    },
    {
        "name": "Teleportation - Typo in Module",
        "description": "Typo 'crique' instead of 'cirq'",
        "expected_status": "FAIL",
        "code": """
import cirq
q0 = cirq.LineQubit(0)
# Typo below
circuit = crique.Circuit()
circuit.append(cirq.H(q0))
"""
    },
    {
        "name": "Teleportation - Undefined Variable",
        "description": "Using q3 which is not defined",
        "expected_status": "FAIL",
        "code": """
import cirq
q0, q1, q2 = cirq.LineQubit.range(3)
circuit = cirq.Circuit()
# q3 is not defined
circuit.append(cirq.CNOT(q1, q3)) 
"""
    },
    {
        "name": "Teleportation - Syntax Error",
        "description": "Missing closing parenthesis",
        "expected_status": "FAIL",
        "code": """
import cirq
q0 = cirq.LineQubit(0)
circuit = cirq.Circuit(
    cirq.H(q0
    # Missing closing paren above
"""
    },

    # --- GROUP 2: DEUTSCH-JOZSA ---
    {
        "name": "Deutsch-Jozsa - Valid",
        "description": "Standard DJ circuit for 2 qubits (Simplified)",
        "expected_status": "PASS",
        "code": """
import cirq
q0, q1, q2 = cirq.LineQubit.range(3)
circuit = cirq.Circuit()
circuit.append(cirq.X(q2))
# Explicit loops instead of on_each for safety
for q in [q0, q1, q2]:
    circuit.append(cirq.H(q))
# Oracle
circuit.append(cirq.CNOT(q0, q2))
circuit.append(cirq.CNOT(q1, q2))
# Final H
for q in [q0, q1]:
    circuit.append(cirq.H(q))
circuit.append(cirq.measure(q0, key='c0'))
circuit.append(cirq.measure(q1, key='c1'))
"""
    },
    {
        "name": "Deutsch-Jozsa - Indentation Error",
        "description": "Python indentation error in loop",
        "expected_status": "FAIL",
        "code": """
import cirq
q = cirq.LineQubit.range(3)
circuit = cirq.Circuit()
for i in range(3):
cirq.H(q[i]) # Indentation Error
"""
    },
    {
        "name": "Deutsch-Jozsa - Wrong Gate Usage",
        "description": "Using parameters for non-parametric gate",
        "expected_status": "FAIL",
        "code": """
import cirq
q0 = cirq.LineQubit(0)
circuit = cirq.Circuit()
# H gate does not take arguments like this
circuit.append(cirq.H(3.14, q0))
"""
    },
    {
        "name": "Deutsch-Jozsa - Logic/Type Error",
        "description": "Trying to operate on integer instead of qubit",
        "expected_status": "FAIL",
        "code": """
import cirq
circuit = cirq.Circuit()
# 0 is int, not qubit
circuit.append(cirq.H(0))
"""
    },
    {
        "name": "Deutsch-Jozsa - Missing Measurement",
        "description": "Circuit has no measurements",
        "expected_status": "FAIL",
        "code": """
import cirq
q0, q1 = cirq.LineQubit.range(2)
circuit = cirq.Circuit(
    cirq.H(q0),
    cirq.CNOT(q0, q1)
)
# No measurement
"""
    },

    # --- GROUP 3: QRNG ---
    {
        "name": "QRNG - Valid",
        "description": "Simple QRNG circuit",
        "expected_status": "PASS",
        "code": """
import cirq
qubits = cirq.LineQubit.range(4)
circuit = cirq.Circuit()
for q in qubits:
    circuit.append(cirq.H(q))
    circuit.append(cirq.measure(q))
"""
    },
    {
        "name": "QRNG - Type Error in Range",
        "description": "Passing string to range",
        "expected_status": "FAIL",
        "code": """
import cirq
# String instead of int
qubits = cirq.LineQubit.range("4") 
circuit = cirq.Circuit()
"""
    },
    {
        "name": "QRNG - Integer Key (Valid)",
        "description": "Cirq accepts integer keys and auto-converts to string",
        "expected_status": "PASS",
        "code": """
import cirq
q = cirq.LineQubit(0)
circuit = cirq.Circuit()
# Cirq accepts int keys
circuit.append(cirq.measure(q, key=123))
"""
    },
    {
        "name": "QRNG - Wrong Attribute",
        "description": "Typo in LineQubit attribute",
        "expected_status": "FAIL",
        "code": """
import cirq
# Should be LineQubit
q = cirq.LinearQubit(0)
"""
    },
    {
        "name": "QRNG - Logic Error (No Superposition)",
        "description": "Measuring |0> without H gate",
        "expected_status": "PASS", 
        "code": """
import cirq
q = cirq.LineQubit(0)
circuit = cirq.Circuit()
# Missing H gate
circuit.append(cirq.measure(q, key='m'))
"""
    },

    # --- GROUP 4: GROVER'S SEARCH ---
    {
        "name": "Grover - Valid",
        "description": "Simple 2-qubit Grover",
        "expected_status": "PASS",
        "code": """
import cirq
q0, q1 = cirq.LineQubit.range(2)
circuit = cirq.Circuit()
circuit.append(cirq.H(q0))
circuit.append(cirq.H(q1))
circuit.append(cirq.CZ(q0, q1))
circuit.append(cirq.H(q0))
circuit.append(cirq.H(q1))
circuit.append(cirq.X(q0))
circuit.append(cirq.X(q1))
circuit.append(cirq.CZ(q0, q1))
circuit.append(cirq.X(q0))
circuit.append(cirq.X(q1))
circuit.append(cirq.H(q0))
circuit.append(cirq.H(q1))
circuit.append(cirq.measure(q0, key='c0'))
circuit.append(cirq.measure(q1, key='c1'))
"""
    },
    {
        "name": "Grover - Argument Mismatch",
        "description": "CZ gate expects 2 qubits",
        "expected_status": "FAIL",
        "code": """
import cirq
q0 = cirq.LineQubit(0)
circuit = cirq.Circuit()
# CZ needs 2 args
circuit.append(cirq.CZ(q0))
"""
    },
    {
        "name": "Grover - Variable Name Typo",
        "description": "Using 'qc' instead of 'circuit'",
        "expected_status": "FAIL",
        "code": """
import cirq
circuit = cirq.Circuit()
q0 = cirq.LineQubit(0)
# 'qc' is not defined
qc.append(cirq.H(q0))
"""
    },
    {
        "name": "Grover - Unsupported Gate",
        "description": "Using imaginary gate",
        "expected_status": "FAIL",
        "code": """
import cirq
q = cirq.LineQubit(0)
circuit = cirq.Circuit()
# MagicGate doesn't exist
circuit.append(cirq.MagicGate(q))
"""
    },
    {
        "name": "Grover - Invalid Append Type",
        "description": "Appending a list containing non-operation objects",
        "expected_status": "FAIL",
        "code": """
import cirq
q0 = cirq.LineQubit(0)
circuit = cirq.Circuit()
# Invalid: Appending a string is not allowed which should raise TypeError
circuit.append([cirq.H(q0), "not_a_gate"])
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
            "force_llm_fix": True # Always try to fix faults
        }
        
        try:
            # Run validation
            result = validator_agent.execute(task)
            duration = time.time() - start_time
            
            success = result.get("success", False)
            fixed_code = result.get("fixed_code", None)
            
            # Determine pass/fail based on expectation
            # If we expected FAIL, we check if the agent *caught* it (success=False) 
            # OR if it auto-fixed it and the second run passed.
            # Actually, ValidatorAgent returns success=False if initial validation fails.
            # But if it fixes it, it might return fixed_code.
            
            status = "UNKNOWN"
            if test["expected_status"] == "PASS":
                # Expecting valid code to pass immediately
                status = "PASS" if success else "FAIL"
            else:
                # Expecting invalid code using LLM fix
                # It "PASSES" the test if the validator detected failure (success=False)
                # AND suggested a fix (fixed_code is not None)
                if not success and fixed_code:
                    status = "PASS (Fixed)"
                elif not success:
                    status = "PASS (Detected)" # Detected error but maybe no fix
                else:
                    status = "FAIL (False Positive)" # Code passed but should have failed
            
            print(f"-> {status} ({duration:.2f}s)")
            
            results.append({
                "ID": i+1,
                "Name": test["name"],
                "Description": test["description"],
                "Expected": test["expected_status"],
                "Actual_Success": success,
                "Has_Fix": bool(fixed_code),
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
