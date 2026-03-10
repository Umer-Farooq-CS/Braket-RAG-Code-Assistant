"""
Convert curated_designer_examples.jsonl from Cirq to Amazon Braket.
"""
import json
import re

# Read the source file
INPUT = r"c:\Users\Sahal Saeed\Documents\GitHub\Braket-RAG-Code-Assistant\data\knowledge_base\curated_designer_examples.jsonl"
OUTPUT = r"c:\Users\Sahal Saeed\Documents\GitHub\Braket-RAG-Code-Assistant\data\knowledge_base\curated_designer_examples_braket.jsonl"

# ──────────────────────────────────────────────────────────────────────
# Hard-coded Braket equivalents for each entry (by ID).
# ──────────────────────────────────────────────────────────────────────

BRAKET_ENTRIES = {}

# ── design_basic_adder_template ──
BRAKET_ENTRIES["design_basic_adder_template"] = {
    "task": "Design a reusable function implementing a ripple-carry adder for n-bit integers using Toffoli (CCNot) and CNOT gates in Amazon Braket.",
    "constraints": [
        "Define a function that takes a circuit and 3n qubits (carry, a, b registers)",
        "Use CCNot for carry propagation and CNOT for sum bits",
        "Provide an example circuit that adds two 3-bit numbers"
    ],
    "code": """from braket.circuits import Circuit

def ripple_carry_adder(circuit, carry, a, b):
    n = len(a)
    for i in range(n - 1):
        circuit.ccnot(a[i], b[i], carry[i + 1])
        circuit.cnot(a[i], b[i])
    circuit.cnot(a[n - 1], b[n - 1])
    return circuit

n = 3
carry = list(range(0, 3 * n, 3))
a = list(range(1, 3 * n, 3))
b = list(range(2, 3 * n, 3))

circuit = Circuit()
ripple_carry_adder(circuit, carry, a, b)
"""
}

BRAKET_ENTRIES["design_basic_adder_template_v2"] = {
    "task": "Show how to use the ripple-carry adder function to add two specific 3-bit classical numbers by initializing the a and b registers and measuring the sum in Amazon Braket.",
    "constraints": [
        "Assume ripple_carry_adder function from the previous example is available",
        "Initialize a and b registers to fixed bit patterns using X gates",
        "Measure the sum register and print the result"
    ],
    "code": """from braket.circuits import Circuit
from braket.devices import LocalSimulator

def ripple_carry_adder(circuit, carry, a, b):
    n = len(a)
    for i in range(n - 1):
        circuit.ccnot(a[i], b[i], carry[i + 1])
        circuit.cnot(a[i], b[i])
    circuit.cnot(a[n - 1], b[n - 1])
    return circuit

n = 3
carry = list(range(0, 3 * n, 3))
a = list(range(1, 3 * n, 3))
b = list(range(2, 3 * n, 3))

circuit = Circuit()

# Example: add a=3 (011) and b=5 (101)
for bit, q in zip("011"[::-1], a):
    if bit == '1':
        circuit.x(q)
for bit, q in zip("101"[::-1], b):
    if bit == '1':
        circuit.x(q)

ripple_carry_adder(circuit, carry, a, b)

# Measure sum register (b qubits hold the result)
for q in b:
    circuit.measure(q)

device = LocalSimulator()
result = device.run(circuit, shots=1).result()
print(result.measurements)
"""
}

BRAKET_ENTRIES["design_bb84_round"] = {
    "task": "Write an Amazon Braket circuit that implements one round of the BB84 protocol on a single qubit: Alice chooses a random bit and basis, encodes it, and Bob chooses a random basis to measure.",
    "constraints": [
        "Use a single qubit (qubit 0)",
        "Use numpy to sample Alice and Bob bases",
        "Use Pauli-X to encode the bit and Hadamard to switch bases",
        "Return a circuit that ends with a measurement"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit

q = 0

alice_bit = np.random.randint(0, 2)
alice_basis = np.random.randint(0, 2)

circuit = Circuit()

if alice_bit == 1:
    circuit.x(q)
if alice_basis == 1:
    circuit.h(q)

bob_basis = np.random.randint(0, 2)
if bob_basis == 1:
    circuit.h(q)

circuit.measure(q)
"""
}

BRAKET_ENTRIES["design_bb84_round_v2"] = {
    "task": "Implement a reusable function in Amazon Braket that performs a single BB84 round with random bases for Alice and Bob and returns the bit, bases, and measurement result.",
    "constraints": [
        "Use numpy.random for sampling",
        "Return a tuple (alice_bit, alice_basis, bob_basis, measurement_result)",
        "Use a single qubit for the quantum channel"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit
from braket.devices import LocalSimulator


def bb84_round(rng=None):
    if rng is None:
        rng = np.random.default_rng()

    q = 0
    alice_bit = int(rng.integers(0, 2))
    alice_basis = int(rng.integers(0, 2))
    bob_basis = int(rng.integers(0, 2))

    circuit = Circuit()

    if alice_bit == 1:
        circuit.x(q)
    if alice_basis == 1:
        circuit.h(q)

    if bob_basis == 1:
        circuit.h(q)

    circuit.measure(q)

    device = LocalSimulator()
    result = device.run(circuit, shots=1).result()
    meas = int(result.measurements[0][0])
    return alice_bit, alice_basis, bob_basis, meas
"""
}

BRAKET_ENTRIES["design_bell_state"] = {
    "task": "Design an Amazon Braket circuit that prepares the Bell state (|00> + |11>)/sqrt(2) on two qubits and measures them in the computational basis.",
    "constraints": [
        "Use qubit 0 and qubit 1",
        "Start from |00>",
        "Use a Hadamard on the first qubit and a CNOT to create entanglement",
        "Measure both qubits"
    ],
    "code": """from braket.circuits import Circuit

circuit = Circuit()
circuit.h(0)
circuit.cnot(0, 1)
circuit.measure([0, 1])
"""
}

BRAKET_ENTRIES["design_bell_state_v2"] = {
    "task": "Create an Amazon Braket function that returns a Bell-state preparation circuit on two given qubits, and then build a main script that simulates and prints the measurement counts.",
    "constraints": [
        "Define a function bell_circuit(q0, q1) -> Circuit",
        "Use H on q0 and CNOT(q0, q1)",
        "Add a measurement on both qubits",
        "Use LocalSimulator to sample 1000 shots and print measurement counts"
    ],
    "code": """from braket.circuits import Circuit
from braket.devices import LocalSimulator


def bell_circuit(q0, q1):
    circuit = Circuit()
    circuit.h(q0)
    circuit.cnot(q0, q1)
    circuit.measure([q0, q1])
    return circuit


circuit = bell_circuit(0, 1)

device = LocalSimulator()
result = device.run(circuit, shots=1000).result()
print(result.measurement_counts)
"""
}

BRAKET_ENTRIES["design_bell_state_v3"] = {
    "task": "Design a Bell-state circuit in Amazon Braket that adds gates step by step to highlight the ordering of operations.",
    "constraints": [
        "Build the circuit by adding operations sequentially",
        "First: H on q0",
        "Second: CNOT(q0, q1)",
        "Third: measurement of both qubits"
    ],
    "code": """from braket.circuits import Circuit

q0, q1 = 0, 1

circuit = Circuit()

# Step 1: Hadamard on q0
circuit.h(q0)

# Step 2: CNOT
circuit.cnot(q0, q1)

# Step 3: Measurement
circuit.measure([q0, q1])
"""
}

BRAKET_ENTRIES["design_bernstein_vazirani_general"] = {
    "task": "Create a function that runs the Bernstein-Vazirani algorithm for an arbitrary hidden bitstring `s` using Amazon Braket.",
    "constraints": [
        "Function signature: bv_algorithm(hidden_string: str) -> Circuit",
        "Dynamically create the oracle based on 1s in the string",
        "Return the circuit including measurement"
    ],
    "code": """from braket.circuits import Circuit

def bv_algorithm(hidden_string):
    n = len(hidden_string)
    inputs = list(range(n))
    ancilla = n

    circuit = Circuit()

    # Initialize
    circuit.x(ancilla)
    circuit.h(ancilla)
    for q in inputs:
        circuit.h(q)

    # Oracle
    for i, bit in enumerate(hidden_string):
        if bit == '1':
            circuit.cnot(inputs[i], ancilla)

    # Interference and Measure
    for q in inputs:
        circuit.h(q)
    for q in inputs:
        circuit.measure(q)
    return circuit
"""
}

BRAKET_ENTRIES["design_bernstein_vazirani_noisy"] = {
    "task": "Simulate the Bernstein-Vazirani algorithm under depolarizing noise and return the probability of finding the correct hidden string using Amazon Braket.",
    "constraints": [
        "Hidden string s='110'",
        "Apply depolarizing noise (probability=0.01) after every Hadamard gate",
        "Run simulation 100 times",
        "Return fraction of times result matches '110'"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit, Noise
from braket.devices import LocalSimulator

def run_noisy_bv():
    inputs = [0, 1, 2]
    ancilla = 3

    circuit = Circuit()

    # Init
    circuit.x(ancilla)
    circuit.h(ancilla)
    circuit.depolarizing(ancilla, probability=0.01)

    for q in inputs:
        circuit.h(q)
        circuit.depolarizing(q, probability=0.01)

    # Oracle s='110' (q0, q1)
    circuit.cnot(0, ancilla)
    circuit.cnot(1, ancilla)

    # Interference
    for q in inputs:
        circuit.h(q)
        circuit.depolarizing(q, probability=0.01)

    for q in inputs:
        circuit.measure(q)

    device = LocalSimulator("braket_dm")
    result = device.run(circuit, shots=100).result()

    matches = 0
    for sample in result.measurements:
        if list(sample[:3]) == [1, 1, 0]:
            matches += 1

    return matches / 100.0
"""
}

BRAKET_ENTRIES["design_bernstein_vazirani_specific"] = {
    "task": "Implement the Bernstein-Vazirani algorithm to find the hidden string '101' using 3 input qubits and 1 ancilla in Amazon Braket.",
    "constraints": [
        "Use 4 qubits (0-3)",
        "Initialize ancilla to |->",
        "Apply H to all input qubits",
        "Oracle: Apply CNOT(q0, ancilla) and CNOT(q2, ancilla) (since s='101')",
        "Apply H to inputs and measure"
    ],
    "code": """from braket.circuits import Circuit

inputs = [0, 1, 2]
ancilla = 3

circuit = Circuit()

# Initialize ancilla
circuit.x(ancilla)
circuit.h(ancilla)

# Initialize inputs
for q in inputs:
    circuit.h(q)

# Oracle for s='101'
circuit.cnot(inputs[0], ancilla)
circuit.cnot(inputs[2], ancilla)

# Interference
for q in inputs:
    circuit.h(q)

# Measure
for q in inputs:
    circuit.measure(q)
"""
}

BRAKET_ENTRIES["design_bit_flip_code_correction"] = {
    "task": "Implement a 3-qubit bit-flip code that includes the correction step using quantum control (Toffoli gates) instead of classical feedback in Amazon Braket.",
    "constraints": [
        "Use 3 data qubits and 2 ancilla qubits",
        "Encode |psi> into 3 qubits",
        "Simulate error: X on q0",
        "Measure syndromes into ancillas",
        "Use ancillas to control X gates on data qubits to correct error"
    ],
    "code": """from braket.circuits import Circuit

data = [0, 1, 2]
ancillas = [3, 4]

circuit = Circuit()

# Encode
circuit.cnot(data[0], data[1])
circuit.cnot(data[0], data[2])

# Error (X on q0)
circuit.x(data[0])

# Syndrome Measurement (CNOTs to ancillas)
# a0 checks q0, q1
circuit.cnot(data[0], ancillas[0])
circuit.cnot(data[1], ancillas[0])

# a1 checks q1, q2
circuit.cnot(data[1], ancillas[1])
circuit.cnot(data[2], ancillas[1])

# Correction (Quantum Control)
# Syndrome 10 (a0=1, a1=0) -> Error on q0
circuit.x(ancillas[1])
circuit.ccnot(ancillas[0], ancillas[1], data[0])
circuit.x(ancillas[1])

# Syndrome 11 (a0=1, a1=1) -> Error on q1
circuit.ccnot(ancillas[0], ancillas[1], data[1])

# Syndrome 01 (a0=0, a1=1) -> Error on q2
circuit.x(ancillas[0])
circuit.ccnot(ancillas[0], ancillas[1], data[2])
circuit.x(ancillas[0])

for q in data:
    circuit.measure(q)
"""
}

BRAKET_ENTRIES["design_bit_flip_code_general"] = {
    "task": "Create a generalized function for an n-qubit repetition code (where n is odd) to protect against bit flips using Amazon Braket.",
    "constraints": [
        "Function signature: repetition_code_circuit(n, error_qubit) -> Circuit",
        "Encode |psi> on q0 to n qubits",
        "Apply X error on `error_qubit`",
        "Measure n-1 syndromes",
        "Return circuit (no correction step needed, just syndromes)"
    ],
    "code": """from braket.circuits import Circuit

def repetition_code_circuit(n, error_qubit):
    if n % 2 == 0:
        raise ValueError("n must be odd")

    data_qubits = list(range(n))
    syndromes = list(range(n, 2 * n - 1))

    circuit = Circuit()

    # Encode: CNOT q0 -> q1...q(n-1)
    for i in range(1, n):
        circuit.cnot(data_qubits[0], data_qubits[i])

    # Error
    if 0 <= error_qubit < n:
        circuit.x(data_qubits[error_qubit])

    # Syndrome Measurement: Z_i Z_{i+1}
    for i in range(n - 1):
        circuit.cnot(data_qubits[i], syndromes[i])
        circuit.cnot(data_qubits[i + 1], syndromes[i])

    for q in syndromes:
        circuit.measure(q)
    return circuit
"""
}

BRAKET_ENTRIES["design_bit_flip_logical_x"] = {
    "task": "Implement a logical X gate on a 3-qubit bit-flip encoded state using Amazon Braket.",
    "constraints": [
        "Start with encoded |000>",
        "Apply logical X (X on all qubits)",
        "Verify the state is |111>"
    ],
    "code": """from braket.circuits import Circuit

qubits = [0, 1, 2]
circuit = Circuit()

# Logical X: X on all qubits
# X_L |0_L> = X_L |000> = |111> = |1_L>
for q in qubits:
    circuit.x(q)

for q in qubits:
    circuit.measure(q)
"""
}

BRAKET_ENTRIES["design_decoherence_with_depolarizing_channel"] = {
    "task": "Design a two-qubit Bell-state experiment that inserts a depolarizing noise channel on each qubit before measurement and runs it with the density matrix simulator in Amazon Braket.",
    "constraints": [
        "Start from a standard Bell-state preparation",
        "Apply depolarizing noise (probability=0.05) to both qubits",
        "Use LocalSimulator with density matrix backend to sample outcomes",
        "Return measurement counts"
    ],
    "code": """from braket.circuits import Circuit
from braket.devices import LocalSimulator

circuit = Circuit()
circuit.h(0)
circuit.cnot(0, 1)
circuit.depolarizing(0, probability=0.05)
circuit.depolarizing(1, probability=0.05)
circuit.measure([0, 1])

device = LocalSimulator("braket_dm")
result = device.run(circuit, shots=2000).result()

print(result.measurement_counts)
"""
}

BRAKET_ENTRIES["design_decoherence_with_depolarizing_channel_v2"] = {
    "task": "Extend the noisy Bell-state example to compare the measurement counts with and without depolarizing noise in a single script using Amazon Braket.",
    "constraints": [
        "Construct two circuits: ideal Bell and noisy Bell",
        "Run both with LocalSimulator density matrix backend",
        "Print both measurement counts for comparison"
    ],
    "code": """from braket.circuits import Circuit
from braket.devices import LocalSimulator

# Ideal circuit
ideal = Circuit()
ideal.h(0)
ideal.cnot(0, 1)
ideal.measure([0, 1])

# Noisy circuit
noisy = Circuit()
noisy.h(0)
noisy.cnot(0, 1)
noisy.depolarizing(0, probability=0.05)
noisy.depolarizing(1, probability=0.05)
noisy.measure([0, 1])

device = LocalSimulator("braket_dm")
ideal_result = device.run(ideal, shots=2000).result()
noisy_result = device.run(noisy, shots=2000).result()

print("Ideal:", ideal_result.measurement_counts)
print("Noisy:", noisy_result.measurement_counts)
"""
}

BRAKET_ENTRIES["design_deutsch_jozsa_balanced"] = {
    "task": "Implement the Deutsch-Jozsa algorithm for a 2-qubit system with a balanced oracle (f(x) = x) using Amazon Braket.",
    "constraints": [
        "Use two qubits (q0 input, q1 ancilla)",
        "Initialize q1 to |->",
        "Apply H to q0",
        "Oracle is CNOT(q0, q1)",
        "Apply H to q0 and measure"
    ],
    "code": """from braket.circuits import Circuit

q0, q1 = 0, 1

circuit = Circuit()

# Initialize ancilla q1 to |->
circuit.x(q1)
circuit.h(q1)

# Algorithm steps
circuit.h(q0)

# Balanced Oracle (CNOT)
circuit.cnot(q0, q1)

circuit.h(q0)
circuit.measure(q0)
"""
}

BRAKET_ENTRIES["design_deutsch_jozsa_constant"] = {
    "task": "Implement the Deutsch-Jozsa algorithm for a 2-qubit system with a constant oracle (f(x) = 0) using Amazon Braket.",
    "constraints": [
        "Use two qubits (q0 for input, q1 for ancilla)",
        "Initialize q1 to |-> state",
        "Apply H to q0",
        "Oracle is Identity (do nothing)",
        "Apply H to q0 and measure"
    ],
    "code": """from braket.circuits import Circuit

q0, q1 = 0, 1

circuit = Circuit()

# Initialize ancilla q1 to |->
circuit.x(q1)
circuit.h(q1)

# Algorithm steps
circuit.h(q0)

# Constant Oracle (Identity): do nothing

circuit.h(q0)
circuit.measure(q0)
"""
}

BRAKET_ENTRIES["design_deutsch_jozsa_from_function"] = {
    "task": "Create a Deutsch-Jozsa oracle generator that takes a Python boolean function f(x) and builds the oracle portion of an Amazon Braket circuit for n qubits.",
    "constraints": [
        "Function signature: make_oracle(circuit, f, n, input_qubits, ancilla)",
        "The oracle should operate on n+1 qubits",
        "Implement the oracle logic by iterating over all 2^n inputs and applying X to the ancilla if f(x)=1",
        "Use multi-controlled X gates"
    ],
    "code": """from braket.circuits import Circuit

def make_oracle(circuit, f, n, input_qubits, ancilla):
    for i in range(2**n):
        if f(i) == 1:
            # Flip 0-bits to activate multi-controlled-X
            for j in range(n):
                if not (i >> (n - 1 - j)) & 1:
                    circuit.x(input_qubits[j])

            # Multi-controlled X on ancilla
            if n == 1:
                circuit.cnot(input_qubits[0], ancilla)
            elif n == 2:
                circuit.ccnot(input_qubits[0], input_qubits[1], ancilla)
            else:
                # For n > 2, decompose into Toffoli chain
                # Simplified: use auxiliary qubits or decomposition
                pass

            # Undo the flips
            for j in range(n):
                if not (i >> (n - 1 - j)) & 1:
                    circuit.x(input_qubits[j])
    return circuit
"""
}

BRAKET_ENTRIES["design_deutsch_jozsa_general"] = {
    "task": "Create a generalized function to run the Deutsch-Jozsa algorithm given a black-box oracle function for n qubits using Amazon Braket.",
    "constraints": [
        "Function signature: dj_algorithm(oracle_fn, n) -> Circuit",
        "Input register size n, plus 1 ancilla",
        "oracle_fn takes (circuit, input_qubits, ancilla) and adds oracle gates",
        "Return the full circuit with measurement on input register"
    ],
    "code": """from braket.circuits import Circuit

def dj_algorithm(oracle_fn, n):
    input_qubits = list(range(n))
    ancilla = n

    circuit = Circuit()

    # Initialize ancilla to |->
    circuit.x(ancilla)
    circuit.h(ancilla)

    # Initialize input to |+>
    for q in input_qubits:
        circuit.h(q)

    # Apply Oracle
    oracle_fn(circuit, input_qubits, ancilla)

    # Interference
    for q in input_qubits:
        circuit.h(q)

    # Measure
    for q in input_qubits:
        circuit.measure(q)
    return circuit
"""
}

BRAKET_ENTRIES["design_device_validation_sycamore_example"] = {
    "task": "Write an Amazon Braket example that checks qubit connectivity on an IonQ or Rigetti device by verifying which qubit pairs support two-qubit gates.",
    "constraints": [
        "Use braket.aws.AwsDevice to query device properties",
        "Check the connectivity graph for valid two-qubit gate pairs",
        "Handle the case where a pair is not connected"
    ],
    "code": """from braket.circuits import Circuit
from braket.devices import LocalSimulator

# For local simulation, all qubit pairs are valid.
# On real hardware, check device.properties.paradigm.connectivity.

# Example: Build a valid 2-qubit circuit
q0, q1 = 0, 1
valid_circuit = Circuit()
valid_circuit.cnot(q0, q1)

# Simulate locally (always valid)
device = LocalSimulator()
result = device.run(valid_circuit, shots=10).result()
print("Valid circuit result:", result.measurement_counts)

# For real devices, connectivity can be checked:
# from braket.aws import AwsDevice
# device = AwsDevice("arn:aws:braket:us-east-1::device/qpu/ionq/Harmony")
# connectivity = device.properties.paradigm.connectivity
# print("Connectivity:", connectivity)
"""
}

BRAKET_ENTRIES["design_device_validation_sycamore_example_v2"] = {
    "task": "Wrap a device connectivity check in a helper that takes an arbitrary pair of qubits and reports whether a two-qubit gate is allowed on that device using Amazon Braket.",
    "constraints": [
        "Write a function is_valid_pair(device, q0, q1) -> bool",
        "Check device connectivity from device properties",
        "Return True if the pair is connected, False otherwise"
    ],
    "code": """from braket.devices import LocalSimulator


def is_valid_pair(device, q0, q1):
    \"\"\"Check if a two-qubit gate is valid between q0 and q1 on the device.\"\"\"
    try:
        connectivity = device.properties.paradigm.connectivity
        if connectivity.fullyConnected:
            return True
        graph = connectivity.connectivityGraph
        return str(q1) in graph.get(str(q0), []) or str(q0) in graph.get(str(q1), [])
    except AttributeError:
        # LocalSimulator or device without connectivity info
        return True
"""
}

BRAKET_ENTRIES["design_ghz_state_3_qubit"] = {
    "task": "Create an Amazon Braket circuit to generate the 3-qubit GHZ state |000> + |111>.",
    "constraints": [
        "Use 3 qubits",
        "Start with H on the first qubit",
        "Use CNOTs to entangle the rest",
        "Measure all qubits"
    ],
    "code": """from braket.circuits import Circuit

circuit = Circuit()

# H on first qubit -> (|0> + |1>)00
circuit.h(0)

# CNOT 0->1 -> |00>0 + |11>0
circuit.cnot(0, 1)

# CNOT 1->2 -> |000> + |111>
circuit.cnot(1, 2)

circuit.measure([0, 1, 2])
"""
}

BRAKET_ENTRIES["design_ghz_state_general"] = {
    "task": "Write a function to generate an n-qubit GHZ state using Amazon Braket.",
    "constraints": [
        "Function signature: ghz_circuit(n) -> Circuit",
        "Use H on the first qubit",
        "Chain CNOTs (0->1, 1->2, ..., n-2->n-1)",
        "Return the circuit with measurements"
    ],
    "code": """from braket.circuits import Circuit

def ghz_circuit(n):
    circuit = Circuit()

    circuit.h(0)

    for i in range(n - 1):
        circuit.cnot(i, i + 1)

    circuit.measure(list(range(n)))
    return circuit
"""
}

BRAKET_ENTRIES["design_ghz_state_measurement"] = {
    "task": "Generate a 4-qubit GHZ state and verify it by measuring parity constraints using Amazon Braket.",
    "constraints": [
        "Use 4 qubits",
        "Create GHZ state",
        "Measure all qubits and post-process to verify parity (all bits equal)",
        "All qubits should be 0 or all should be 1"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit
from braket.devices import LocalSimulator

circuit = Circuit()

# GHZ State
circuit.h(0)
for i in range(3):
    circuit.cnot(i, i + 1)

circuit.measure([0, 1, 2, 3])

device = LocalSimulator()
result = device.run(circuit, shots=100).result()

# Check parity: for GHZ |0000> + |1111>, all qubits should be equal
for row in result.measurements:
    assert np.all(row == row[0])  # All elements equal
"""
}

BRAKET_ENTRIES["design_grover_general"] = {
    "task": "Implement a generalized Grover's search algorithm function in Amazon Braket for n qubits.",
    "constraints": [
        "Function signature: grover_search(oracle_fn, n, iterations) -> Circuit",
        "oracle_fn takes (circuit, qubits) and adds oracle gates",
        "Implement the diffusion operator for n qubits using H, X, and a multi-controlled Z gate",
        "Return the full circuit with measurement"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit, Gate

def grover_search(oracle_fn, n, iterations):
    qubits = list(range(n))
    circuit = Circuit()

    # Superposition
    for q in qubits:
        circuit.h(q)

    for _ in range(iterations):
        # Oracle
        oracle_fn(circuit, qubits)

        # Diffusion Operator
        for q in qubits:
            circuit.h(q)
        for q in qubits:
            circuit.x(q)

        # Multi-controlled Z (reflection about |11...1>)
        if n == 2:
            circuit.cz(qubits[0], qubits[1])
        elif n == 3:
            # CCZ = H-CCNot-H on target
            circuit.h(qubits[2])
            circuit.ccnot(qubits[0], qubits[1], qubits[2])
            circuit.h(qubits[2])
        else:
            # General multi-controlled Z decomposition needed
            circuit.h(qubits[-1])
            circuit.ccnot(qubits[0], qubits[1], qubits[-1])
            circuit.h(qubits[-1])

        for q in qubits:
            circuit.x(q)
        for q in qubits:
            circuit.h(q)

    for q in qubits:
        circuit.measure(q)
    return circuit
"""
}

BRAKET_ENTRIES["design_grover_specific_3_qubit"] = {
    "task": "Implement Grover's algorithm for 3 qubits to find the marked state |101> using Amazon Braket.",
    "constraints": [
        "Use 3 qubits",
        "Oracle: Marks |101> (phase flip). Flip q1, apply CCZ, unflip q1.",
        "Diffusion: H, X, CCZ, X, H.",
        "Run for 2 iterations."
    ],
    "code": """from braket.circuits import Circuit

qubits = [0, 1, 2]
circuit = Circuit()

# Superposition
for q in qubits:
    circuit.h(q)

iterations = 2
for _ in range(iterations):
    # Oracle for |101>
    circuit.x(qubits[1])
    # CCZ = H-CCNot-H on target qubit
    circuit.h(qubits[2])
    circuit.ccnot(qubits[0], qubits[1], qubits[2])
    circuit.h(qubits[2])
    circuit.x(qubits[1])

    # Diffusion
    for q in qubits:
        circuit.h(q)
    for q in qubits:
        circuit.x(q)
    circuit.h(qubits[2])
    circuit.ccnot(qubits[0], qubits[1], qubits[2])
    circuit.h(qubits[2])
    for q in qubits:
        circuit.x(q)
    for q in qubits:
        circuit.h(q)

for q in qubits:
    circuit.measure(q)
"""
}

BRAKET_ENTRIES["design_hello_qubit"] = {
    "task": "Create a minimal Amazon Braket circuit on one qubit that prepares the computational basis state |1> from |0> and then measures it in the Z basis.",
    "constraints": [
        "Use a single qubit (qubit 0)",
        "Use a Pauli-X gate to prepare |1>",
        "Add a measurement"
    ],
    "code": """from braket.circuits import Circuit

circuit = Circuit()
circuit.x(0)
circuit.measure(0)
"""
}

BRAKET_ENTRIES["design_hello_qubit_v2"] = {
    "task": "Write a simple Amazon Braket example that flips a single qubit from |0> to |1> and then measures it, printing the measurement results.",
    "constraints": [
        "Use one qubit",
        "Apply a single X gate before measurement",
        "Use LocalSimulator to run with several repetitions",
        "Print the measurement results"
    ],
    "code": """from braket.circuits import Circuit
from braket.devices import LocalSimulator

circuit = Circuit()
circuit.x(0)
circuit.measure(0)

device = LocalSimulator()
result = device.run(circuit, shots=20).result()
print(result.measurements)
"""
}

BRAKET_ENTRIES["design_hello_qubit_v3"] = {
    "task": "Construct a single-qubit Amazon Braket circuit that demonstrates a deterministic measurement outcome by preparing |1> and sampling multiple times.",
    "constraints": [
        "Use qubit 0",
        "Prepare |1> using X",
        "Measure the qubit",
        "Show that all samples are 1 for an ideal simulator"
    ],
    "code": """from braket.circuits import Circuit
from braket.devices import LocalSimulator

circuit = Circuit()
circuit.x(0)
circuit.measure(0)

device = LocalSimulator()
result = device.run(circuit, shots=50).result()
print(result.measurement_counts)
"""
}

BRAKET_ENTRIES["design_hhl_2x2_schematic"] = {
    "task": "Construct the high-level schematic circuit for HHL on a 2x2 matrix using Amazon Braket.",
    "constraints": [
        "Use 1 input qubit (b), 2 clock qubits, 1 ancilla",
        "1. State Prep (load b)",
        "2. QPE (U=e^iAt)",
        "3. Eigenvalue Inversion (Rotation)",
        "4. Inverse QPE",
        "5. Measure Ancilla"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit

# Qubits: b=0, clock0=1, clock1=2, ancilla=3
b_qubit = 0
clock = [1, 2]
ancilla = 3

circuit = Circuit()

# 1. State Prep (Example: |b> = |1>)
circuit.x(b_qubit)

# 2. QPE (Placeholder for actual QPE gates)
for q in clock:
    circuit.h(q)
# ... Controlled-U operations and inverse QFT would go here ...

# 3. Eigenvalue Inversion (Placeholder)
# Controlled rotation on ancilla
circuit.ry(ancilla, 0.1)  # Simplified placeholder

# 4. Inverse QPE (Uncompute clock)
for q in clock:
    circuit.h(q)

# 5. Measure Ancilla (Post-selection on 1)
circuit.measure(ancilla)
circuit.measure(b_qubit)
"""
}

BRAKET_ENTRIES["design_hhl_eigenvalue_inversion"] = {
    "task": "Implement the eigenvalue inversion rotation step of the HHL algorithm for 2 clock qubits using Amazon Braket.",
    "constraints": [
        "Use 2 clock qubits (representing eigenvalues) and 1 ancilla qubit",
        "Apply Ry(theta) on ancilla controlled by clock qubits",
        "Theta should be 2*arcsin(C/lambda) with C=1"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit

clock = [0, 1]
ancilla = 2

circuit = Circuit()

# Eigenvalues: |01>->1, |10>->2, |11>->3

# Controlled by |01>: theta = 2*arcsin(1)
circuit.x(clock[0])
# Controlled-Controlled Ry: decompose as multi-controlled gate
circuit.h(ancilla)
circuit.ccnot(clock[0], clock[1], ancilla)
circuit.h(ancilla)
circuit.x(clock[0])

# Controlled by |10>: theta = 2*arcsin(1/2)
circuit.x(clock[1])
circuit.ry(ancilla, 2 * np.arcsin(0.5))
circuit.x(clock[1])

# Controlled by |11>: theta = 2*arcsin(1/3)
circuit.ry(ancilla, 2 * np.arcsin(1/3))
"""
}

BRAKET_ENTRIES["design_measure_each_example"] = {
    "task": "Design an Amazon Braket circuit that prepares three |+> states and measures each qubit separately, returning measurement counts.",
    "constraints": [
        "Use 3 qubits",
        "Use H on each qubit",
        "Measure each qubit individually",
        "Print measurement counts"
    ],
    "code": """from braket.circuits import Circuit
from braket.devices import LocalSimulator

circuit = Circuit()
for q in range(3):
    circuit.h(q)
for q in range(3):
    circuit.measure(q)

device = LocalSimulator()
result = device.run(circuit, shots=1000).result()

print(result.measurement_counts)
"""
}

BRAKET_ENTRIES["design_measure_each_example_v2"] = {
    "task": "Prepare |+> on three qubits and measure each one, then print measurement counts for each qubit independently using Amazon Braket.",
    "constraints": [
        "Use 3 qubits",
        "Prepare |+> on each qubit",
        "Measure all qubits and analyze per-qubit results"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit
from braket.devices import LocalSimulator

circuit = Circuit()
circuit.h(0)
circuit.h(1)
circuit.h(2)
circuit.measure([0, 1, 2])

device = LocalSimulator()
result = device.run(circuit, shots=1000).result()

measurements = result.measurements
for q_idx, label in enumerate(['q0', 'q1', 'q2']):
    counts = {0: 0, 1: 0}
    for shot in measurements:
        counts[shot[q_idx]] += 1
    print(label, counts)
"""
}

BRAKET_ENTRIES["design_parametric_rotation_sweep"] = {
    "task": "Design a single-qubit Amazon Braket circuit with a parametric rotation and sweep over that parameter, then simulate it to estimate the probability of measuring 1 as a function of the parameter.",
    "constraints": [
        "Use qubit 0",
        "Use FreeParameter for the rotation angle",
        "Sweep over multiple parameter values",
        "Use LocalSimulator to run each"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit, FreeParameter
from braket.devices import LocalSimulator

theta = FreeParameter('theta')

circuit = Circuit()
circuit.rx(0, theta)
circuit.measure(0)

device = LocalSimulator()
theta_values = np.linspace(0.0, 2 * np.pi, 21)

results = []
for val in theta_values:
    bound_circuit = circuit(theta=val)
    result = device.run(bound_circuit, shots=1000).result()
    results.append(result)
"""
}

BRAKET_ENTRIES["design_parametric_rotation_sweep_v2"] = {
    "task": "Design a helper function that builds a single-qubit parametric X-rotation circuit and a separate function that runs a sweep using Amazon Braket, returning the list of mean outcomes.",
    "constraints": [
        "Use qubit 0",
        "Use FreeParameter for the rotation angle",
        "Separate circuit construction from simulation logic",
        "Return a list of mean measurement values over a sweep"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit, FreeParameter
from braket.devices import LocalSimulator


def build_parametric_circuit(theta):
    circuit = Circuit()
    circuit.rx(0, theta)
    circuit.measure(0)
    return circuit


def run_rabi_sweep():
    theta = FreeParameter('theta')
    circuit = build_parametric_circuit(theta)
    device = LocalSimulator()
    angles = np.linspace(0.0, 2 * np.pi, 30)
    means = []
    for val in angles:
        bound_circuit = circuit(theta=val)
        result = device.run(bound_circuit, shots=500).result()
        means.append(np.mean(result.measurements))
    return means
"""
}

BRAKET_ENTRIES["design_qaoa_ansatz_general"] = {
    "task": "Create a generalized function to generate a QAOA circuit for MaxCut on an arbitrary graph for depth p using Amazon Braket.",
    "constraints": [
        "Function signature: qaoa_maxcut_circuit(graph, p, gammas, betas) -> Circuit",
        "Graph is list of edges (u, v)",
        "Input gammas and betas must have length p",
        "Return circuit with measurement"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit

def qaoa_maxcut_circuit(graph, p, gammas, betas):
    max_node = max(max(u, v) for u, v in graph)
    n = max_node + 1
    qubits = list(range(n))

    circuit = Circuit()

    # Initial state
    for q in qubits:
        circuit.h(q)

    for i in range(p):
        gamma = gammas[i]
        beta = betas[i]

        # Problem Unitary: ZZ interactions
        for u, v in graph:
            circuit.zz(u, v, 2 * gamma)

        # Mixer Unitary: Rx rotations
        for q in qubits:
            circuit.rx(q, 2 * beta)

    for q in qubits:
        circuit.measure(q)
    return circuit
"""
}

BRAKET_ENTRIES["design_qaoa_cost_evaluation"] = {
    "task": "Implement a function to calculate the MaxCut cost expectation value from QAOA measurement results using Amazon Braket.",
    "constraints": [
        "Function signature: maxcut_cost(measurements, graph) -> float",
        "measurements is the raw measurement array from result.measurements",
        "Cost function C(x) = sum over edges (u,v) of 0.5 * (1 - z_u * z_v) where z in {-1, 1}",
        "Return expected cost"
    ],
    "code": """import numpy as np

def maxcut_cost(measurements, graph):
    # Convert 0/1 to 1/-1
    spins = 1 - 2 * np.array(measurements)

    total_cost = 0.0
    for u, v in graph:
        z_u = spins[:, u]
        z_v = spins[:, v]
        correlation = np.mean(z_u * z_v)
        total_cost += 0.5 * (1 - correlation)

    return total_cost
"""
}

BRAKET_ENTRIES["design_qaoa_maxcut_layer"] = {
    "task": "Design a single QAOA layer for MaxCut on a 3-node ring graph using Amazon Braket, with parameters gamma and beta.",
    "constraints": [
        "Use three qubits representing graph nodes",
        "Implement ZZ phase separators for each edge",
        "Apply RX mixers on each qubit with angle 2*beta",
        "Use FreeParameter for gamma and beta"
    ],
    "code": """from braket.circuits import Circuit, FreeParameter

gamma = FreeParameter('gamma')
beta = FreeParameter('beta')

circuit = Circuit()

# Edges of a 3-node ring: (0,1), (1,2), (2,0)
edges = [(0, 1), (1, 2), (2, 0)]

# Phase separator
for i, j in edges:
    circuit.zz(i, j, 2 * gamma)

# Mixer
for q in range(3):
    circuit.rx(q, 2 * beta)
"""
}

BRAKET_ENTRIES["design_qaoa_maxcut_layer_v2"] = {
    "task": "Write a generic function that builds a single QAOA layer for MaxCut on an arbitrary graph represented by a NetworkX graph, using Amazon Braket ZZ interactions and RX mixers.",
    "constraints": [
        "Function signature: qaoa_layer(qubits, graph, gamma, beta) -> Circuit",
        "Use graph.edges to determine which ZZ terms to apply",
        "Use ZZ and RX gates"
    ],
    "code": """import networkx as nx
from braket.circuits import Circuit, FreeParameter


def qaoa_layer(qubits, graph, gamma, beta):
    circuit = Circuit()

    for u, v in graph.edges:
        circuit.zz(qubits[u], qubits[v], 2 * gamma)

    for q in qubits:
        circuit.rx(q, 2 * beta)

    return circuit
"""
}

BRAKET_ENTRIES["design_qaoa_maxcut_specific"] = {
    "task": "Implement a p=1 QAOA circuit for MaxCut on a 3-node line graph (0-1-2) with specific gamma and beta parameters using Amazon Braket.",
    "constraints": [
        "Graph edges: (0,1), (1,2)",
        "Parameters: gamma=0.1, beta=0.2",
        "Initial state: |+> on all qubits",
        "Return the circuit with measurement"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit

gamma = 0.1
beta = 0.2

circuit = Circuit()

# Initial state |+>
for q in range(3):
    circuit.h(q)

# Problem Unitary (ZZ interactions)
for u, v in [(0, 1), (1, 2)]:
    circuit.zz(u, v, 2 * gamma)

# Mixer Unitary (RX rotations)
for q in range(3):
    circuit.rx(q, 2 * beta)

circuit.measure([0, 1, 2])
"""
}

BRAKET_ENTRIES["design_qaoa_optimization_loop"] = {
    "task": "Run a full QAOA optimization for a square graph (0-1-2-3-0) with p=1 using scipy.optimize and Amazon Braket.",
    "constraints": [
        "Graph: [(0,1), (1,2), (2,3), (3,0)]",
        "Optimize gamma and beta to maximize MaxCut",
        "Use LocalSimulator to get expectation values",
        "Return optimal parameters"
    ],
    "code": """import numpy as np
from scipy.optimize import minimize
from braket.circuits import Circuit
from braket.devices import LocalSimulator

def qaoa_optimization_square():
    graph = [(0, 1), (1, 2), (2, 3), (3, 0)]
    device = LocalSimulator()

    def run_circuit(params):
        gamma, beta = params
        circuit = Circuit()
        for q in range(4):
            circuit.h(q)

        for u, v in graph:
            circuit.zz(u, v, 2 * gamma)

        for q in range(4):
            circuit.rx(q, 2 * beta)

        circuit.measure([0, 1, 2, 3])

        result = device.run(circuit, shots=1000).result()
        meas = np.array(result.measurements)

        spins = 1 - 2 * meas
        avg_cut = 0
        for u, v in graph:
            corr = np.mean(spins[:, u] * spins[:, v])
            avg_cut += 0.5 * (1 - corr)

        return -avg_cut

    init_params = [0.5, 0.5]
    res = minimize(run_circuit, init_params, method='COBYLA')
    return res.x, -res.fun
"""
}

BRAKET_ENTRIES["design_qft_general"] = {
    "task": "Write a generalized function to generate the QFT circuit for n qubits using Amazon Braket.",
    "constraints": [
        "Function signature: qft_circuit(n) -> Circuit",
        "Use nested loops to apply Hadamards and controlled phase rotations",
        "Include the final SWAP layer to reverse qubit order",
        "Return the circuit"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit

def qft_circuit(n):
    circuit = Circuit()

    for i in range(n):
        circuit.h(i)
        for j in range(i + 1, n):
            angle = np.pi / (2 ** (j - i))
            circuit.cphaseshift(j, i, angle)

    # Swaps to reverse qubit order
    for i in range(n // 2):
        circuit.swap(i, n - 1 - i)

    return circuit
"""
}

BRAKET_ENTRIES["design_qft_inverse"] = {
    "task": "Implement the Inverse QFT on 3 qubits using Amazon Braket by constructing and inverting the QFT circuit.",
    "constraints": [
        "Use 3 qubits",
        "Construct QFT circuit first",
        "Build the inverse QFT by reversing gate order and negating angles",
        "Verify by combining QFT + inverse QFT"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit

def qft_3_qubits():
    c = Circuit()
    c.h(0)
    c.cphaseshift(1, 0, np.pi / 2)
    c.cphaseshift(2, 0, np.pi / 4)
    c.h(1)
    c.cphaseshift(2, 1, np.pi / 2)
    c.h(2)
    c.swap(0, 2)
    return c

def inverse_qft_3_qubits():
    c = Circuit()
    c.swap(0, 2)
    c.h(2)
    c.cphaseshift(2, 1, -np.pi / 2)
    c.h(1)
    c.cphaseshift(2, 0, -np.pi / 4)
    c.cphaseshift(1, 0, -np.pi / 2)
    c.h(0)
    return c

qft_c = qft_3_qubits()
iqft_c = inverse_qft_3_qubits()

# Combine them (should act as identity)
full_circuit = qft_c.add_circuit(iqft_c)
"""
}

BRAKET_ENTRIES["design_qft_standard_3_qubit"] = {
    "task": "Implement the Quantum Fourier Transform (QFT) on 3 qubits using Amazon Braket.",
    "constraints": [
        "Use 3 qubits",
        "Apply Hadamard to q0",
        "Apply controlled phase shift gates between qubits",
        "Apply Hadamard to q1 and q2 with appropriate phase gates",
        "Swap q0 and q2 at the end"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit

circuit = Circuit()

# QFT on 3 qubits
circuit.h(0)
circuit.cphaseshift(1, 0, np.pi / 2)
circuit.cphaseshift(2, 0, np.pi / 4)

circuit.h(1)
circuit.cphaseshift(2, 1, np.pi / 2)

circuit.h(2)

# Swap to reverse order
circuit.swap(0, 2)
"""
}

BRAKET_ENTRIES["design_qft_three_qubits_template"] = {
    "task": "Create a reusable function in Amazon Braket that returns a 3-qubit QFT circuit on given qubits.",
    "constraints": [
        "Define a function qft_3(qubits) -> Circuit",
        "Apply Hadamard and controlled phase rotations",
        "Include final SWAPs to reverse qubit order"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit

def qft_3(qubits):
    circuit = Circuit()
    n = 3
    for i in range(n):
        circuit.h(qubits[i])
        for j in range(i + 1, n):
            angle = np.pi / (2 ** (j - i))
            circuit.cphaseshift(qubits[j], qubits[i], angle)
    circuit.swap(qubits[0], qubits[2])
    return circuit
"""
}

BRAKET_ENTRIES["design_qft_three_qubits_template_v2"] = {
    "task": "Implement a modular 3-qubit QFT template in Amazon Braket that can optionally skip the final SWAP network based on a boolean flag.",
    "constraints": [
        "Function signature: qft_3(qubits, reverse=True)",
        "When reverse=False, do not apply the final SWAPs",
        "Otherwise apply the SWAPs as usual"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit


def qft_3(qubits, reverse=True):
    circuit = Circuit()
    n = 3
    for i in range(n):
        circuit.h(qubits[i])
        for j in range(i + 1, n):
            angle = np.pi / (2 ** (j - i))
            circuit.cphaseshift(qubits[j], qubits[i], angle)
    if reverse:
        circuit.swap(qubits[0], qubits[2])
    return circuit
"""
}

BRAKET_ENTRIES["design_qpe_general"] = {
    "task": "Create a general Quantum Phase Estimation function in Amazon Braket that takes a unitary gate, and the number of counting qubits.",
    "constraints": [
        "Function signature: qpe_circuit(unitary_matrix, n_counting) -> Circuit",
        "Assume eigenstate is |1>",
        "Use controlled unitary operations",
        "Apply inverse QFT on counting qubits"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit

def inverse_qft(circuit, qubits):
    n = len(qubits)
    for i in range(n // 2):
        circuit.swap(qubits[i], qubits[n - 1 - i])
    for i in range(n):
        for j in range(i):
            angle = -np.pi / (2 ** (i - j))
            circuit.cphaseshift(qubits[i], qubits[j], angle)
        circuit.h(qubits[i])

def qpe_circuit(unitary_matrix, n_counting):
    counting = list(range(n_counting))
    psi = n_counting

    circuit = Circuit()

    # Initialize eigenstate |1>
    circuit.x(psi)

    # H on counting
    for q in counting:
        circuit.h(q)

    # Controlled-U^2^k operations
    for i, q in enumerate(counting):
        power = 2 ** (n_counting - 1 - i)
        powered_matrix = np.linalg.matrix_power(unitary_matrix, power)
        circuit.unitary(matrix=powered_matrix, targets=[psi], control=q)

    # Inverse QFT
    inverse_qft(circuit, counting)

    for q in counting:
        circuit.measure(q)
    return circuit
"""
}

BRAKET_ENTRIES["design_qpe_rz"] = {
    "task": "Estimate the phase of an Rz(theta) gate where theta=pi/3 using 3 counting qubits in Amazon Braket.",
    "constraints": [
        "Use 4 qubits (3 counting, 1 eigenstate)",
        "Eigenstate is |1>",
        "Implement QPE to estimate the phase"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit

counting = [0, 1, 2]
psi = 3

circuit = Circuit()

# Eigenstate |1>
circuit.x(psi)

# Superposition
for q in counting:
    circuit.h(q)

# Controlled-U operations
theta = np.pi / 3
for i, q in enumerate(counting):
    k = 2 ** (3 - 1 - i)
    # Controlled-Rz(k * theta) using cphaseshift
    circuit.cphaseshift(q, psi, k * theta / 2)

# Inverse QFT on counting qubits
circuit.swap(counting[0], counting[2])
for i in range(3):
    for j in range(i):
        angle = -np.pi / (2 ** (i - j))
        circuit.cphaseshift(counting[i], counting[j], angle)
    circuit.h(counting[i])

for q in counting:
    circuit.measure(q)
"""
}

BRAKET_ENTRIES["design_qpe_t_gate"] = {
    "task": "Estimate the phase of a T gate (phase = 1/8) using 2 counting qubits in Amazon Braket.",
    "constraints": [
        "Use 3 qubits (2 counting, 1 eigenstate)",
        "Initialize eigenstate to |1> (since T|1> = e^{i pi/4}|1>)",
        "Apply H to counting qubits",
        "Apply controlled T and S gates",
        "Apply Inverse QFT on counting qubits",
        "Measure counting qubits"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit

q0, q1 = 0, 1
psi = 2

circuit = Circuit()

# Initialize eigenstate |1>
circuit.x(psi)

# Initialize counting qubits
circuit.h(q0)
circuit.h(q1)

# Controlled-U operations
# q0 (MSB) controls U^2 = S
circuit.cphaseshift(q0, psi, np.pi / 2)
# q1 (LSB) controls U^1 = T
circuit.cphaseshift(q1, psi, np.pi / 4)

# Inverse QFT on q0, q1
circuit.swap(q0, q1)
circuit.h(q1)
circuit.cphaseshift(q0, q1, -np.pi / 2)
circuit.h(q0)

circuit.measure(q0)
circuit.measure(q1)
"""
}

BRAKET_ENTRIES["design_qrng_biased"] = {
    "task": "Create a biased quantum random number generator that outputs '1' with probability p using Amazon Braket.",
    "constraints": [
        "Function signature: biased_qrng(p) -> Circuit",
        "Use Ry(theta) gate where theta is calculated from p",
        "Probability of |1> is sin^2(theta/2) = p",
        "Return circuit with measurement"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit

def biased_qrng(p):
    theta = 2 * np.arcsin(np.sqrt(p))

    circuit = Circuit()
    circuit.ry(0, theta)
    circuit.measure(0)
    return circuit
"""
}

BRAKET_ENTRIES["design_qrng_byte"] = {
    "task": "Generate a random byte (8 bits) by measuring 8 qubits in superposition using Amazon Braket.",
    "constraints": [
        "Use 8 qubits",
        "Apply H to all qubits",
        "Measure all qubits",
        "Return the circuit"
    ],
    "code": """from braket.circuits import Circuit

circuit = Circuit()

for q in range(8):
    circuit.h(q)

circuit.measure(list(range(8)))
"""
}

BRAKET_ENTRIES["design_qrng_distribution_check"] = {
    "task": "Simulate a 4-qubit QRNG 1000 times and verify that the distribution of outcomes is approximately uniform using Amazon Braket.",
    "constraints": [
        "Use 4 qubits",
        "Circuit: H on all, Measure all",
        "Run simulation",
        "Print the counts for each of the 16 possible outcomes"
    ],
    "code": """from braket.circuits import Circuit
from braket.devices import LocalSimulator

circuit = Circuit()
for q in range(4):
    circuit.h(q)
circuit.measure(list(range(4)))

device = LocalSimulator()
result = device.run(circuit, shots=1000).result()

print(result.measurement_counts)
# Ideally each bin has around 1000/16 ~ 62 counts
"""
}

BRAKET_ENTRIES["design_qrng_single_bit"] = {
    "task": "Create a simple quantum random number generator that produces a single random bit using a Hadamard gate in Amazon Braket.",
    "constraints": [
        "Use 1 qubit",
        "Apply Hadamard gate to create superposition",
        "Measure the qubit",
        "Return the circuit"
    ],
    "code": """from braket.circuits import Circuit

circuit = Circuit()
circuit.h(0)
circuit.measure(0)
"""
}

BRAKET_ENTRIES["design_quantum_walk_1d_coin"] = {
    "task": "Implement a single step of a 1D quantum walk on a line using a coin qubit and position qubits in Amazon Braket.",
    "constraints": [
        "Use 1 coin qubit and 3 position qubits (representing 8 positions)",
        "Coin operator: Hadamard on coin qubit",
        "Shift operator: Conditional increment/decrement of position",
        "Measure coin and position"
    ],
    "code": """from braket.circuits import Circuit

coin = 0
position = [1, 2, 3]

circuit = Circuit()

# Coin toss
circuit.h(coin)

# Shift Operator (simplified placeholder)
# Conditional Increment (controlled by coin=0)
circuit.x(coin)
# Increment logic placeholder
circuit.x(coin)

# Conditional Decrement (controlled by coin=1)
# Decrement logic placeholder

circuit.measure(coin)
for q in position:
    circuit.measure(q)
"""
}

BRAKET_ENTRIES["design_quantum_walk_cycle_3_node"] = {
    "task": "Implement a discrete-time quantum walk on a 3-node cycle graph using Amazon Braket.",
    "constraints": [
        "Use 2 qubits to represent 3 nodes (00, 01, 10)",
        "Use a coin qubit",
        "Implement 1 step: coin flip + shift operator",
        "Measure position qubits"
    ],
    "code": """from braket.circuits import Circuit

coin = 0
nodes = [1, 2]

circuit = Circuit()

# Coin
circuit.h(coin)

# Shift: implement permutation conditioned on coin
# For 3-node cycle, the shift permutations are complex.
# Placeholder using controlled operations
circuit.cnot(coin, nodes[0])
circuit.cnot(coin, nodes[1])

for q in nodes:
    circuit.measure(q)
"""
}

BRAKET_ENTRIES["design_rabi_oscillation_experiment"] = {
    "task": "Design a Rabi oscillation experiment on a single qubit in Amazon Braket, sweeping a rotation angle and measuring excitation probability.",
    "constraints": [
        "Use qubit 0",
        "Use FreeParameter for the angle",
        "Sweep over multiple angle values using LocalSimulator",
        "Compute and print the mean measurement value for each angle"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit, FreeParameter
from braket.devices import LocalSimulator

theta = FreeParameter('theta')

circuit = Circuit()
circuit.rx(0, theta)
circuit.measure(0)

device = LocalSimulator()
angles = np.linspace(0.0, 2 * np.pi, 50)

excited_probs = []
for angle in angles:
    bound = circuit(theta=angle)
    result = device.run(bound, shots=1000).result()
    prob = np.mean(result.measurements)
    excited_probs.append(prob)
"""
}

BRAKET_ENTRIES["design_rabi_oscillation_experiment_v2"] = {
    "task": "Build a Rabi experiment helper in Amazon Braket that returns both the angles and the measured excitation probabilities as NumPy arrays for plotting.",
    "constraints": [
        "Use qubit 0",
        "Use FreeParameter and sweep over values",
        "Return (angles, probs) where both are NumPy arrays"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit, FreeParameter
from braket.devices import LocalSimulator


def rabi_experiment(num_points=100, repetitions=1000):
    theta = FreeParameter('theta')
    circuit = Circuit()
    circuit.rx(0, theta)
    circuit.measure(0)

    device = LocalSimulator()
    angles = np.linspace(0.0, np.pi, num_points)
    probs = []
    for angle in angles:
        bound = circuit(theta=angle)
        result = device.run(bound, shots=repetitions).result()
        probs.append(np.mean(result.measurements))
    return angles, np.array(probs)
"""
}

BRAKET_ENTRIES["design_random_circuit_benchmark"] = {
    "task": "Design a function that generates a random single-layer circuit of parameterized single-qubit rotations and CZ gates on a line of n qubits using Amazon Braket, then simulates it once.",
    "constraints": [
        "Use qubit indices 0..n-1",
        "Use numpy to sample random angles and CZ pairs between neighbors",
        "Return both the circuit and the result from a LocalSimulator"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit
from braket.devices import LocalSimulator

def random_layer_circuit(n, seed=None):
    rng = np.random.default_rng(seed)
    circuit = Circuit()

    # Random single-qubit rotations
    for q in range(n):
        theta = 2 * np.pi * rng.random()
        circuit.rx(q, theta)

    # Random CZs between neighbors
    for i in range(n - 1):
        if rng.random() < 0.5:
            circuit.cz(i, i + 1)

    device = LocalSimulator()
    result = device.run(circuit, shots=1).result()
    return circuit, result
"""
}

BRAKET_ENTRIES["design_random_circuit_benchmark_v2"] = {
    "task": "Extend the random single-layer circuit generator to run multiple seeds and report the average circuit depth over K trials using Amazon Braket.",
    "constraints": [
        "Reuse the random_layer_circuit(n, seed) helper",
        "Loop over several seeds and collect circuit depth",
        "Print the mean depth"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit
from braket.devices import LocalSimulator


def random_layer_circuit(n, seed=None):
    rng = np.random.default_rng(seed)
    circuit = Circuit()
    for q in range(n):
        theta = 2 * np.pi * rng.random()
        circuit.rx(q, theta)
    for i in range(n - 1):
        if rng.random() < 0.5:
            circuit.cz(i, i + 1)
    device = LocalSimulator()
    result = device.run(circuit, shots=1).result()
    return circuit, result


depths = []
for seed in range(10):
    circ, _ = random_layer_circuit(5, seed=seed)
    depths.append(circ.depth)

print("Average depth:", np.mean(depths))
"""
}

BRAKET_ENTRIES["design_repetition_code_bit_flip"] = {
    "task": "Design a 3-qubit bit-flip error correction circuit in Amazon Braket that encodes a qubit, simulates a bit-flip error, and measures syndromes.",
    "constraints": [
        "Use 3 data qubits and 2 ancilla qubits",
        "Encode: CNOT(q0, q1), CNOT(q0, q2)",
        "Error: Apply X to one qubit (e.g., q0)",
        "Syndrome: Measure parities Z0Z1 and Z1Z2 using ancillas"
    ],
    "code": """from braket.circuits import Circuit

data = [0, 1, 2]
ancillas = [3, 4]

circuit = Circuit()

# Encode
circuit.cnot(data[0], data[1])
circuit.cnot(data[0], data[2])

# Error (simulated X on q0)
circuit.x(data[0])

# Syndrome Measurement
# Z0 Z1 -> parity of q0, q1 into a0
circuit.cnot(data[0], ancillas[0])
circuit.cnot(data[1], ancillas[0])

# Z1 Z2 -> parity of q1, q2 into a1
circuit.cnot(data[1], ancillas[1])
circuit.cnot(data[2], ancillas[1])

for q in ancillas:
    circuit.measure(q)
"""
}

BRAKET_ENTRIES["design_repetition_code_phase_flip"] = {
    "task": "Implement a 3-qubit phase-flip error correction code using Amazon Braket.",
    "constraints": [
        "Use 3 data qubits and 2 ancilla qubits",
        "Encoding: CNOT then H to move to |+>/|-> basis",
        "Error: Apply Z to q1",
        "Syndrome: H to return to computational basis, then measure parities"
    ],
    "code": """from braket.circuits import Circuit

data = [0, 1, 2]
ancillas = [3, 4]

circuit = Circuit()

# Encode (|0> -> |+++>, |1> -> |--->)
circuit.cnot(data[0], data[1])
circuit.cnot(data[0], data[2])
for q in data:
    circuit.h(q)

# Error (Z on q1)
circuit.z(data[1])

# Syndrome Measurement
# Rotate back to computational basis
for q in data:
    circuit.h(q)

# Measure parities Z0Z1 and Z1Z2
circuit.cnot(data[0], ancillas[0])
circuit.cnot(data[1], ancillas[0])

circuit.cnot(data[1], ancillas[1])
circuit.cnot(data[2], ancillas[1])

for q in ancillas:
    circuit.measure(q)

# Rotate back to logical basis
for q in data:
    circuit.h(q)
"""
}

BRAKET_ENTRIES["design_shor_code_encoding"] = {
    "task": "Implement the encoding circuit for Shor's 9-qubit code in Amazon Braket.",
    "constraints": [
        "Use 9 qubits",
        "Input state on q0",
        "Phase flip encoding: CNOT(q0, q3), CNOT(q0, q6), then H on q0, q3, q6",
        "Bit flip encoding: CNOTs within each block"
    ],
    "code": """from braket.circuits import Circuit

circuit = Circuit()

# Phase flip encoding (spread to q0, q3, q6)
circuit.cnot(0, 3)
circuit.cnot(0, 6)

circuit.h(0)
circuit.h(3)
circuit.h(6)

# Bit flip encoding
# Block 1: q0 -> q0, q1, q2
circuit.cnot(0, 1)
circuit.cnot(0, 2)

# Block 2: q3 -> q3, q4, q5
circuit.cnot(3, 4)
circuit.cnot(3, 5)

# Block 3: q6 -> q6, q7, q8
circuit.cnot(6, 7)
circuit.cnot(6, 8)
"""
}

BRAKET_ENTRIES["design_shor_general_structure"] = {
    "task": "Create a function that generates the high-level circuit structure for Shor's algorithm given a modular exponentiation unitary using Amazon Braket.",
    "constraints": [
        "Function signature: shor_circuit(n_counting, mod_exp_fn) -> Circuit",
        "mod_exp_fn(circuit, control, target_qubits, power) adds controlled modular exponentiation gates",
        "Use n_counting qubits for the register",
        "Return circuit with QPE structure"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit

def inverse_qft(circuit, qubits):
    n = len(qubits)
    for i in range(n // 2):
        circuit.swap(qubits[i], qubits[n - 1 - i])
    for i in range(n):
        for j in range(i):
            angle = -np.pi / (2 ** (i - j))
            circuit.cphaseshift(qubits[i], qubits[j], angle)
        circuit.h(qubits[i])

def shor_circuit(n_counting, mod_exp_fn, target_qubits):
    counting = list(range(n_counting))

    circuit = Circuit()

    # Superposition
    for q in counting:
        circuit.h(q)

    # Controlled-U operations
    for i in range(n_counting):
        power = 2 ** i
        control_qubit = counting[n_counting - 1 - i]
        mod_exp_fn(circuit, control_qubit, target_qubits, power)

    # Inverse QFT
    inverse_qft(circuit, counting)

    for q in counting:
        circuit.measure(q)
    return circuit
"""
}

BRAKET_ENTRIES["design_simon_sampling"] = {
    "task": "Run Simon's algorithm circuit multiple times to collect linear equations for a hidden string s='11' using Amazon Braket.",
    "constraints": [
        "Use the specific Simon circuit for s='11'",
        "Run 10 times",
        "Return the list of unique non-zero measurement results (bitstrings)"
    ],
    "code": """from braket.circuits import Circuit
from braket.devices import LocalSimulator

def collect_simon_samples():
    inputs = [0, 1]
    outputs = [2, 3]

    circuit = Circuit()
    for q in inputs:
        circuit.h(q)
    circuit.cnot(inputs[0], outputs[0])
    circuit.cnot(inputs[1], outputs[0])
    for q in inputs:
        circuit.h(q)
    for q in inputs:
        circuit.measure(q)

    device = LocalSimulator()
    result = device.run(circuit, shots=10).result()

    samples = []
    for row in result.measurements:
        bitstring = "".join(str(x) for x in row[:2])
        if bitstring != "00" and bitstring not in samples:
            samples.append(bitstring)
    return samples
"""
}

BRAKET_ENTRIES["design_simon_specific"] = {
    "task": "Implement Simon's algorithm for 2 input qubits with hidden string s='11' using Amazon Braket.",
    "constraints": [
        "Use 4 qubits (2 input, 2 output)",
        "Oracle implements f(x) where f(x)=f(x^11)",
        "Use CNOTs to implement f(x) = x0 XOR x1 into the first output qubit",
        "Apply H to inputs, Oracle, H to inputs, Measure inputs"
    ],
    "code": """from braket.circuits import Circuit

inputs = [0, 1]
outputs = [2, 3]

circuit = Circuit()

# Initialize inputs
for q in inputs:
    circuit.h(q)

# Oracle for s='11'
circuit.cnot(inputs[0], outputs[0])
circuit.cnot(inputs[1], outputs[0])

# Interference
for q in inputs:
    circuit.h(q)

# Measure inputs
for q in inputs:
    circuit.measure(q)
"""
}

BRAKET_ENTRIES["design_simple_grover_two_qubits"] = {
    "task": "Construct a two-qubit Amazon Braket circuit that performs one iteration of Grover's algorithm, marking the state |11> and then applying the diffusion operator, followed by measurement.",
    "constraints": [
        "Use two qubits",
        "Initialize with Hadamard on both qubits",
        "Use a CZ gate as the oracle on |11>",
        "Implement the standard two-qubit diffusion operator",
        "Measure both qubits at the end"
    ],
    "code": """from braket.circuits import Circuit

circuit = Circuit()

circuit.h(0)
circuit.h(1)

# Oracle: CZ marks |11>
circuit.cz(0, 1)

# Diffusion operator
circuit.h(0)
circuit.h(1)
circuit.x(0)
circuit.x(1)
circuit.h(1)
circuit.cnot(0, 1)
circuit.h(1)
circuit.x(0)
circuit.x(1)
circuit.h(0)
circuit.h(1)

circuit.measure([0, 1])
"""
}

BRAKET_ENTRIES["design_simple_grover_two_qubits_v2"] = {
    "task": "Refactor the two-qubit Grover iteration into a function that takes an oracle circuit builder as input and appends a single diffusion layer and measurement using Amazon Braket.",
    "constraints": [
        "Define a function grover_iteration(oracle_fn) -> Circuit",
        "oracle_fn takes (circuit, q0, q1) and adds oracle gates",
        "Preserve the standard two-qubit diffusion operator",
        "Place measurement at the end"
    ],
    "code": """from braket.circuits import Circuit


def grover_iteration(oracle_fn):
    q0, q1 = 0, 1
    circuit = Circuit()

    circuit.h(q0)
    circuit.h(q1)

    oracle_fn(circuit, q0, q1)

    # Diffusion operator
    circuit.h(q0)
    circuit.h(q1)
    circuit.x(q0)
    circuit.x(q1)
    circuit.h(q1)
    circuit.cnot(q0, q1)
    circuit.h(q1)
    circuit.x(q0)
    circuit.x(q1)
    circuit.h(q0)
    circuit.h(q1)

    circuit.measure([q0, q1])
    return circuit
"""
}

BRAKET_ENTRIES["design_superdense_coding"] = {
    "task": "Create an Amazon Braket circuit that demonstrates superdense coding: Alice encodes two classical bits into one qubit using a shared Bell pair with Bob, and Bob decodes the bits.",
    "constraints": [
        "Use two qubits",
        "Prepare a Bell state between Alice and Bob",
        "Apply I/X/Z/XZ on Alice's qubit depending on the two-bit message",
        "Have Bob apply a Bell measurement to recover the bits"
    ],
    "code": """from braket.circuits import Circuit

alice, bob = 0, 1

circuit = Circuit()

# Shared Bell pair
circuit.h(alice)
circuit.cnot(alice, bob)

# Example: encode message '10' using Z on Alice
circuit.z(alice)

# Bob decodes
circuit.cnot(alice, bob)
circuit.h(alice)
circuit.measure([alice, bob])
"""
}

BRAKET_ENTRIES["design_superdense_coding_v2"] = {
    "task": "Generalize the superdense coding example so that Alice can choose any two-bit classical message (00, 01, 10, 11) using Amazon Braket.",
    "constraints": [
        "Implement a function encode_message(bits) -> Circuit",
        "Map '00'->I, '01'->X, '10'->Z, '11'->ZX on Alice",
        "Reuse a shared Bell pair between Alice and Bob"
    ],
    "code": """from braket.circuits import Circuit


def encode_message(bits):
    alice, bob = 0, 1
    circuit = Circuit()

    # Shared Bell pair
    circuit.h(alice)
    circuit.cnot(alice, bob)

    # Encode message
    if bits == '01':
        circuit.x(alice)
    elif bits == '10':
        circuit.z(alice)
    elif bits == '11':
        circuit.z(alice)
        circuit.x(alice)

    # Decode
    circuit.cnot(alice, bob)
    circuit.h(alice)
    circuit.measure([alice, bob])
    return circuit
"""
}

BRAKET_ENTRIES["design_swap_network_line"] = {
    "task": "Design a swap network on a line of 4 qubits that reverses their order using nearest-neighbor SWAP gates in Amazon Braket.",
    "constraints": [
        "Use four qubits",
        "Only allow SWAP between adjacent qubits",
        "End state should map logical ordering [0,1,2,3] to [3,2,1,0]"
    ],
    "code": """from braket.circuits import Circuit

circuit = Circuit()

# Layer 1: swap neighbors
circuit.swap(0, 1)
circuit.swap(2, 3)

# Layer 2: swap middle
circuit.swap(1, 2)
"""
}

BRAKET_ENTRIES["design_swap_network_line_v2"] = {
    "task": "Generalize the 4-qubit swap network into a function that returns a circuit reversing a line of n qubits using only nearest-neighbor SWAPs in Amazon Braket.",
    "constraints": [
        "Function signature: reverse_line(qubits) -> Circuit",
        "Use nested loops or a sorting-network style pattern",
        "Do not use SWAP on non-adjacent qubits"
    ],
    "code": """from braket.circuits import Circuit


def reverse_line(qubits):
    n = len(qubits)
    circuit = Circuit()
    for i in range(n // 2):
        left = i
        right = n - 1 - i
        while right - left > 0:
            circuit.swap(qubits[left], qubits[left + 1])
            left += 1
        left -= 1
        while right - left > 0:
            circuit.swap(qubits[right - 1], qubits[right])
            right -= 1
    return circuit
"""
}

BRAKET_ENTRIES["design_swap_test_basic"] = {
    "task": "Implement the Swap Test circuit to measure the overlap between two single-qubit states using Amazon Braket.",
    "constraints": [
        "Use 1 ancilla qubit and 2 data qubits",
        "Initialize ancilla to |+>",
        "Apply CSWAP (Fredkin) gate controlled by ancilla, targeting the two data qubits",
        "Apply H to ancilla",
        "Measure ancilla"
    ],
    "code": """from braket.circuits import Circuit

ancilla = 0
data = [1, 2]

circuit = Circuit()

# Initialize ancilla to |+>
circuit.h(ancilla)

# CSWAP (Fredkin)
circuit.cswap(ancilla, data[0], data[1])

# Interference
circuit.h(ancilla)

# Measure
circuit.measure(ancilla)
"""
}

BRAKET_ENTRIES["design_swap_test_general"] = {
    "task": "Create a generalized Swap Test function for two quantum registers of size n using Amazon Braket.",
    "constraints": [
        "Function signature: swap_test_circuit(reg1, reg2) -> Circuit",
        "Registers must be same size",
        "Use 1 ancilla qubit",
        "Apply CSWAP between corresponding qubits controlled by the same ancilla",
        "Return circuit with ancilla measurement"
    ],
    "code": """from braket.circuits import Circuit

def swap_test_circuit(reg1, reg2):
    if len(reg1) != len(reg2):
        raise ValueError("Registers must be of equal size")

    ancilla = max(max(reg1), max(reg2)) + 1
    circuit = Circuit()

    # Initialize ancilla
    circuit.h(ancilla)

    # CSWAP for each pair
    for q1, q2 in zip(reg1, reg2):
        circuit.cswap(ancilla, q1, q2)

    # Interference
    circuit.h(ancilla)

    # Measure
    circuit.measure(ancilla)
    return circuit
"""
}

BRAKET_ENTRIES["design_swap_test_overlap_calculation"] = {
    "task": "Run a Swap Test simulation to estimate the overlap |<psi|phi>|^2 between |0> and |+> using Amazon Braket.",
    "constraints": [
        "Prepare q1 in |0>",
        "Prepare q2 in |+> (H gate)",
        "Run Swap Test",
        "Calculate overlap from P(0) = 0.5 + 0.5 * |<psi|phi>|^2"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit
from braket.devices import LocalSimulator

ancilla = 0
q0 = 1
q1 = 2

circuit = Circuit()

# Prepare states: q0=|0>, q1=|+>
circuit.h(q1)

# Swap Test
circuit.h(ancilla)
circuit.cswap(ancilla, q0, q1)
circuit.h(ancilla)
circuit.measure(ancilla)

device = LocalSimulator()
result = device.run(circuit, shots=1000).result()

# P(0) = counts(0) / total
counts = result.measurement_counts
p0 = int(counts.get('0', 0)) / 1000

# P(0) = 0.5 + 0.5 * |<psi|phi>|^2
overlap_squared = 2 * p0 - 1
print(f"Estimated overlap squared: {overlap_squared}")
"""
}

BRAKET_ENTRIES["design_vqc_prediction_parity"] = {
    "task": "Implement a prediction function that takes a VQC circuit, parameters, and input data, and returns the probability of class 1 based on parity measurement using Amazon Braket.",
    "constraints": [
        "Function signature: predict_vqc(circuit_fn, params, x_data) -> float",
        "Run simulation",
        "Class 1 probability = Probability of odd parity",
        "Return float"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit
from braket.devices import LocalSimulator

def predict_vqc(circuit_fn, params, x_data):
    circuit = circuit_fn(params, x_data)

    device = LocalSimulator()
    result = device.run(circuit, shots=1000).result()

    measurements = np.array(result.measurements)
    parities = np.sum(measurements, axis=1) % 2
    prob_class_1 = np.mean(parities)
    return prob_class_1
"""
}

BRAKET_ENTRIES["design_vqc_simple_circuit"] = {
    "task": "Construct a simple 2-qubit VQC circuit with a Z-feature map and a hardware-efficient ansatz using Amazon Braket.",
    "constraints": [
        "Use 2 qubits",
        "Feature Map: H on all, then Rz(x_i) on q_i",
        "Ansatz: Ry(theta) on all, CNOT(0,1), Ry(theta) on all",
        "Measure all qubits"
    ],
    "code": """from braket.circuits import Circuit, FreeParameter

# Symbols for data (x) and weights (theta)
x = [FreeParameter(f'x{i}') for i in range(2)]
theta = [FreeParameter(f'theta_{i}') for i in range(4)]

circuit = Circuit()

# Feature Map
circuit.h(0)
circuit.h(1)
circuit.rz(0, x[0])
circuit.rz(1, x[1])

# Ansatz
circuit.ry(0, theta[0])
circuit.ry(1, theta[1])
circuit.cnot(0, 1)
circuit.ry(0, theta[2])
circuit.ry(1, theta[3])

circuit.measure([0, 1])
"""
}

BRAKET_ENTRIES["design_vqe_ansatz_three_qubits"] = {
    "task": "Design a three-qubit hardware-efficient VQE-style ansatz with layers of single-qubit rotations and entangling CNOTs, parametrized by FreeParameters in Amazon Braket.",
    "constraints": [
        "Use three qubits",
        "Use FreeParameter for parameters",
        "Include at least one rotation layer and one entangling layer"
    ],
    "code": """from braket.circuits import Circuit, FreeParameter

theta = [FreeParameter(f'theta_{i}') for i in range(3)]

circuit = Circuit()

# Single-qubit rotation layer
for q in range(3):
    circuit.rx(q, theta[q])

# Entangling layer
circuit.cnot(0, 1)
circuit.cnot(1, 2)
"""
}

BRAKET_ENTRIES["design_vqe_ansatz_three_qubits_v2"] = {
    "task": "Create a layered hardware-efficient three-qubit ansatz in Amazon Braket that alternates rotation layers and a fixed pattern of entangling CZ gates.",
    "constraints": [
        "Use 3 qubits",
        "Use Ry and Rz gates for parameterized rotations",
        "Apply CZ between (0,1) and (1,2) in each entangling layer",
        "Show how to bind numeric values to the parameters"
    ],
    "code": """from braket.circuits import Circuit, FreeParameter
from braket.devices import LocalSimulator

params = [FreeParameter(f'theta_{i}') for i in range(6)]

circuit = Circuit()

for i in range(3):
    circuit.ry(i, params[i])

circuit.cz(0, 1)
circuit.cz(1, 2)

for i in range(3):
    circuit.rz(i, params[3 + i])

# Bind parameters to numeric values
bound_circuit = circuit(**{f'theta_{i}': 0.1 for i in range(6)})

device = LocalSimulator()
result = device.run(bound_circuit, shots=100).result()
"""
}

BRAKET_ENTRIES["design_vqe_custom_hamiltonian"] = {
    "task": "Create a VQE cost function that accepts Hamiltonian terms and estimates energy using Amazon Braket.",
    "constraints": [
        "Function signature: estimate_energy(ansatz_fn, params, hamiltonian_terms) -> float",
        "Hamiltonian terms is list of (coefficient, measurement_basis, qubits)",
        "Iterate terms, append basis change if needed, measure, sum up weighted expectations"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit
from braket.devices import LocalSimulator

def estimate_energy(ansatz_fn, params, hamiltonian_terms):
    device = LocalSimulator()
    total_energy = 0.0

    for coeff, basis, qubits in hamiltonian_terms:
        circuit = ansatz_fn(params)

        # Basis rotation
        for q, b in zip(qubits, basis):
            if b == 'X':
                circuit.h(q)
            elif b == 'Y':
                circuit.si(q)
                circuit.h(q)

        for q in qubits:
            circuit.measure(q)

        result = device.run(circuit, shots=500).result()
        measurements = np.array(result.measurements)

        # Calculate parity expectation
        parity = np.prod(1 - 2 * measurements[:, :len(qubits)], axis=1)
        expectation = np.mean(parity)
        total_energy += coeff * expectation

    return total_energy
"""
}

BRAKET_ENTRIES["design_vqe_hamiltonian_measurement"] = {
    "task": "Implement a function to measure a VQE ansatz circuit in the Pauli bases required for a specific Hamiltonian H = 0.5*Z0 + 0.5*Z1 + 1.0*X0X1 using Amazon Braket.",
    "constraints": [
        "Function signature: measure_hamiltonian(ansatz_fn, params) -> float",
        "Run separate circuits for Z0, Z1 (Z basis) and X0X1 (X basis)",
        "Return the estimated expectation value <H>"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit
from braket.devices import LocalSimulator

def measure_hamiltonian(ansatz_fn, params):
    device = LocalSimulator()

    # Measure Z0 and Z1 (Z basis)
    z_circuit = ansatz_fn(params)
    z_circuit.measure([0, 1])
    z_results = device.run(z_circuit, shots=1000).result()
    z_meas = np.array(z_results.measurements)
    z0_exp = np.mean(1 - 2 * z_meas[:, 0])
    z1_exp = np.mean(1 - 2 * z_meas[:, 1])

    # Measure X0X1 (X basis -> apply H before measure)
    x_circuit = ansatz_fn(params)
    x_circuit.h(0)
    x_circuit.h(1)
    x_circuit.measure([0, 1])
    x_results = device.run(x_circuit, shots=1000).result()
    x_meas = np.array(x_results.measurements)
    x0_vals = 1 - 2 * x_meas[:, 0]
    x1_vals = 1 - 2 * x_meas[:, 1]
    x0x1_exp = np.mean(x0_vals * x1_vals)

    return 0.5 * z0_exp + 0.5 * z1_exp + 1.0 * x0x1_exp
"""
}

BRAKET_ENTRIES["design_vqe_optimization_loop"] = {
    "task": "Implement a full VQE optimization loop using scipy.optimize.minimize to find the ground state energy of a single qubit Hamiltonian H = Z + X using Amazon Braket.",
    "constraints": [
        "Ansatz: Ry(theta)",
        "Hamiltonian: <Z> + <X>",
        "Objective function takes theta, runs circuit, measures <Z> and <X>, returns energy",
        "Use scipy.optimize.minimize to find min energy"
    ],
    "code": """import numpy as np
from scipy.optimize import minimize
from braket.circuits import Circuit
from braket.devices import LocalSimulator

def vqe_optimization():
    device = LocalSimulator()

    def objective(params):
        theta = params[0]

        # Measure <Z>
        circuit_z = Circuit()
        circuit_z.ry(0, theta)
        circuit_z.measure(0)
        res_z = device.run(circuit_z, shots=1000).result()
        z_meas = np.array(res_z.measurements)
        exp_z = np.mean(1 - 2 * z_meas[:, 0])

        # Measure <X>
        circuit_x = Circuit()
        circuit_x.ry(0, theta)
        circuit_x.h(0)
        circuit_x.measure(0)
        res_x = device.run(circuit_x, shots=1000).result()
        x_meas = np.array(res_x.measurements)
        exp_x = np.mean(1 - 2 * x_meas[:, 0])

        return exp_z + exp_x

    init_params = [0.0]
    result = minimize(objective, init_params, method='COBYLA')
    return result.fun, result.x
"""
}

BRAKET_ENTRIES["design_vqe_uccsd_ansatz"] = {
    "task": "Construct a simplified UCCSD-style ansatz for H2 molecule (2 qubits) using Amazon Braket.",
    "constraints": [
        "Use 2 qubits",
        "Implement the unitary exp(-i * theta * X0Y1) as part of UCCSD",
        "Decompose using CNOTs and single qubit rotations"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit, FreeParameter

theta = FreeParameter('theta')

circuit = Circuit()

# exp(-i * theta * X0 Y1)
# Basis change: X -> H, Y -> Rx(pi/2)
circuit.h(0)
circuit.rx(1, np.pi / 2)

# CNOT ladder
circuit.cnot(0, 1)

# Rz(2*theta)
circuit.rz(1, 2 * theta)

# CNOT ladder
circuit.cnot(0, 1)

# Inverse basis change
circuit.rx(1, -np.pi / 2)
circuit.h(0)
"""
}

BRAKET_ENTRIES["designer_char_single_qubit_rb"] = {
    "task": "Implement a function to run single-qubit randomized benchmarking using Amazon Braket.",
    "constraints": [
        "Generate random Clifford gate sequences",
        "Append the inverse Clifford at the end",
        "Measure survival probability"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit
from braket.devices import LocalSimulator

def run_single_qubit_rb(qubit, clifford_depths, shots=100):
    device = LocalSimulator()
    results = {}

    # Single-qubit Clifford gates (simplified set)
    clifford_gates = ['h', 's', 'x', 'y', 'z']

    for depth in clifford_depths:
        survival_count = 0
        for _ in range(shots):
            circuit = Circuit()
            # Apply random Cliffords
            rng = np.random.default_rng()
            for _ in range(depth):
                gate = rng.choice(clifford_gates)
                getattr(circuit, gate)(qubit)
            circuit.measure(qubit)
            result = device.run(circuit, shots=1).result()
            if result.measurements[0][0] == 0:
                survival_count += 1
        results[depth] = survival_count / shots

    return results
"""
}

BRAKET_ENTRIES["designer_char_tomography"] = {
    "task": "Implement a function to perform state tomography on 1 qubit using Amazon Braket by measuring in X, Y, and Z bases.",
    "constraints": [
        "Measure in Z basis (direct measurement)",
        "Measure in X basis (H before measurement)",
        "Measure in Y basis (S†H before measurement)",
        "Return Bloch vector components"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit
from braket.devices import LocalSimulator

def run_state_tomography(prep_circuit_fn, qubit, shots=1000):
    device = LocalSimulator()
    expectations = {}

    for basis in ['Z', 'X', 'Y']:
        circuit = prep_circuit_fn()

        if basis == 'X':
            circuit.h(qubit)
        elif basis == 'Y':
            circuit.si(qubit)
            circuit.h(qubit)

        circuit.measure(qubit)
        result = device.run(circuit, shots=shots).result()
        meas = np.array(result.measurements)
        expectations[basis] = np.mean(1 - 2 * meas[:, 0])

    return expectations
"""
}

BRAKET_ENTRIES["designer_char_two_qubit_rb"] = {
    "task": "Implement a function to run two-qubit randomized benchmarking using Amazon Braket.",
    "constraints": [
        "Generate random two-qubit Clifford sequences",
        "Measure survival probability",
        "Handle two qubits"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit
from braket.devices import LocalSimulator

def run_two_qubit_rb(q0, q1, clifford_depths, shots=100):
    device = LocalSimulator()
    results = {}

    for depth in clifford_depths:
        survival_count = 0
        for _ in range(shots):
            circuit = Circuit()
            rng = np.random.default_rng()
            for _ in range(depth):
                # Random single-qubit Cliffords + entangling gate
                for q in [q0, q1]:
                    gate = rng.choice(['h', 's', 'x', 'y', 'z'])
                    getattr(circuit, gate)(q)
                if rng.random() < 0.3:
                    circuit.cnot(q0, q1)
            circuit.measure([q0, q1])
            result = device.run(circuit, shots=1).result()
            if list(result.measurements[0]) == [0, 0]:
                survival_count += 1
        results[depth] = survival_count / shots

    return results
"""
}

BRAKET_ENTRIES["designer_deutsch_jozsa_balanced"] = {
    "task": "Implement the Deutsch-Jozsa algorithm for a balanced oracle that flips the target qubit if the input has odd parity using Amazon Braket.",
    "constraints": [
        "Use n+1 qubits (n input, 1 target)",
        "Initialize input qubits to |0> and target to |1>",
        "Apply Hadamard to all qubits",
        "Apply the balanced oracle (CNOTs from inputs to target)",
        "Apply Hadamard to input qubits and measure"
    ],
    "code": """from braket.circuits import Circuit
from braket.devices import LocalSimulator

def deutsch_jozsa_balanced(n):
    input_qubits = list(range(n))
    target = n

    circuit = Circuit()

    # Initialization
    circuit.x(target)
    for q in input_qubits + [target]:
        circuit.h(q)

    # Balanced Oracle: CNOT from each input to target (parity)
    for q in input_qubits:
        circuit.cnot(q, target)

    # Interference and Measurement
    for q in input_qubits:
        circuit.h(q)
    for q in input_qubits:
        circuit.measure(q)

    return circuit

circuit = deutsch_jozsa_balanced(3)
device = LocalSimulator()
result = device.run(circuit, shots=1).result()
print(result.measurements)
"""
}

BRAKET_ENTRIES["designer_quantum_phase_estimation_t_gate"] = {
    "task": "Estimate the phase of a T gate (phase pi/4) using 3 precision qubits in Amazon Braket.",
    "constraints": [
        "Use 3 precision qubits and 1 eigenstate qubit",
        "Prepare eigenstate |1> for T gate",
        "Apply Hadamard to precision qubits",
        "Apply controlled-U operations",
        "Apply Inverse QFT on precision qubits",
        "Measure precision qubits"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit
from braket.devices import LocalSimulator

def inverse_qft(circuit, qubits):
    n = len(qubits)
    for i in range(n // 2):
        circuit.swap(qubits[i], qubits[n - 1 - i])
    for i in range(n):
        for j in range(i):
            angle = -np.pi / (2 ** (i - j))
            circuit.cphaseshift(qubits[i], qubits[j], angle)
        circuit.h(qubits[i])

precision_qubits = [0, 1, 2]
eigen_qubit = 3

circuit = Circuit()

# Prepare eigenstate |1>
circuit.x(eigen_qubit)

# Superposition
for q in precision_qubits:
    circuit.h(q)

# Controlled-U operations (T gate phases)
for i, q in enumerate(precision_qubits):
    power = 2 ** i
    angle = power * np.pi / 4  # T gate phase = pi/4
    circuit.cphaseshift(q, eigen_qubit, angle)

# Inverse QFT
inverse_qft(circuit, precision_qubits)

# Measurement
for q in precision_qubits:
    circuit.measure(q)

device = LocalSimulator()
result = device.run(circuit, shots=10).result()
print(result.measurement_counts)
"""
}

BRAKET_ENTRIES["designer_shor_classical_factor"] = {
    "task": "Implement the classical reduction part of Shor's algorithm to find a factor using an order finder.",
    "constraints": [
        "Handle even numbers and prime powers",
        "Randomly select x",
        "Use order finder",
        "Compute GCD"
    ],
    "code": """import math
import random
import sympy

def find_factor(n, order_finder, max_attempts=30):
    if sympy.isprime(n):
        return None
    if n % 2 == 0:
        return 2

    # Check prime power
    for k in range(2, math.floor(math.log2(n)) + 1):
        c = math.pow(n, 1 / k)
        if math.floor(c) ** k == n:
            return math.floor(c)
        if math.ceil(c) ** k == n:
            return math.ceil(c)

    for _ in range(max_attempts):
        x = random.randint(2, n - 1)
        c = math.gcd(x, n)
        if 1 < c < n:
            return c

        r = order_finder(x, n)
        if r is None or r % 2 != 0:
            continue

        y = x ** (r // 2) % n
        c = math.gcd(y - 1, n)
        if 1 < c < n:
            return c
    return None
"""
}

BRAKET_ENTRIES["designer_shor_modular_exp"] = {
    "task": "Implement modular exponentiation as a unitary matrix for use in Shor's algorithm with Amazon Braket.",
    "constraints": [
        "Build unitary matrix for |y> -> |y * x^e mod n>",
        "Use circuit.unitary() to apply it",
        "Handle register size validation"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit

def modular_exp_unitary(base, modulus, n_bits):
    dim = 2 ** n_bits
    matrix = np.zeros((dim, dim), dtype=complex)
    for y in range(dim):
        if y < modulus:
            result = (y * base) % modulus
            matrix[result, y] = 1.0
        else:
            matrix[y, y] = 1.0
    return matrix

def add_controlled_mod_exp(circuit, control, target_qubits, base, modulus, power):
    n_bits = len(target_qubits)
    powered_base = pow(base, power, modulus)
    unitary = modular_exp_unitary(powered_base, modulus, n_bits)
    circuit.unitary(matrix=unitary, targets=target_qubits, control=control)
"""
}

BRAKET_ENTRIES["designer_shor_order_finding_circuit"] = {
    "task": "Construct the order finding circuit using Quantum Phase Estimation and Modular Exponentiation for Shor's algorithm with Amazon Braket.",
    "constraints": [
        "Initialize target to |1>",
        "Apply Hadamard to exponent register",
        "Apply controlled modular exponentiation",
        "Apply Inverse QFT"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit

def inverse_qft(circuit, qubits):
    n = len(qubits)
    for i in range(n // 2):
        circuit.swap(qubits[i], qubits[n - 1 - i])
    for i in range(n):
        for j in range(i):
            angle = -np.pi / (2 ** (i - j))
            circuit.cphaseshift(qubits[i], qubits[j], angle)
        circuit.h(qubits[i])

def make_order_finding_circuit(x, n):
    L = n.bit_length()
    target = list(range(L))
    exponent = list(range(L, 3 * L + 3))

    circuit = Circuit()
    circuit.x(target[L - 1])

    for q in exponent:
        circuit.h(q)

    # Controlled modular exponentiation (placeholder)
    # In practice, use decomposed controlled modular multiplication
    for i, q in enumerate(exponent):
        power = 2 ** i
        # add_controlled_mod_exp(circuit, q, target, x, n, power)

    inverse_qft(circuit, exponent)

    for q in exponent:
        circuit.measure(q)

    return circuit
"""
}

BRAKET_ENTRIES["designer_shor_quantum_finder"] = {
    "task": "Implement the logic to extract the order 'r' from the QPE measurement result using continued fractions.",
    "constraints": [
        "Read eigenphase from measurement",
        "Use fractions.limit_denominator",
        "Verify order validity"
    ],
    "code": """import fractions
import math

def read_eigenphase(measurement, num_bits):
    # Convert binary measurement to integer
    value = int("".join(str(b) for b in measurement), 2)
    return float(value / 2 ** num_bits)

def quantum_order_finder(x, n, measurement, num_bits):
    if x < 2 or n <= x or math.gcd(x, n) > 1:
        raise ValueError(f'Invalid x={x} for modulus n={n}.')

    eigenphase = read_eigenphase(measurement, num_bits)
    f = fractions.Fraction.from_float(eigenphase).limit_denominator(n)
    if f.numerator == 0:
        return None
    r = f.denominator
    if x ** r % n != 1:
        return None
    return r
"""
}

BRAKET_ENTRIES["designer_simon_circuit"] = {
    "task": "Construct the quantum circuit for Simon's Algorithm using a given oracle function in Amazon Braket.",
    "constraints": [
        "Apply Hadamard to input qubits",
        "Apply Oracle",
        "Apply Hadamard to input qubits",
        "Measure input qubits"
    ],
    "code": """from braket.circuits import Circuit

def make_simon_circuit(input_qubits, output_qubits, oracle_fn):
    circuit = Circuit()

    # Initialize qubits
    for q in input_qubits:
        circuit.h(q)

    # Query oracle
    oracle_fn(circuit, input_qubits, output_qubits)

    # Measure in X basis
    for q in input_qubits:
        circuit.h(q)
    for q in input_qubits:
        circuit.measure(q)

    return circuit
"""
}

BRAKET_ENTRIES["designer_simon_oracle"] = {
    "task": "Implement the oracle for Simon's Algorithm that satisfies f(x) = f(y) iff x XOR y = s using Amazon Braket.",
    "constraints": [
        "Copy input to output",
        "XOR secret string based on significant bit",
        "Apply permutation"
    ],
    "code": """from braket.circuits import Circuit

def make_oracle(circuit, input_qubits, output_qubits, secret_string):
    # Copy contents to output qubits
    for control, target in zip(input_qubits, output_qubits):
        circuit.cnot(control, target)

    # Create mapping
    if sum(secret_string):
        significant = list(secret_string).index(1)

        for j in range(len(secret_string)):
            if secret_string[j] > 0:
                circuit.cnot(input_qubits[significant], output_qubits[j])

    # Apply a permutation
    pos = [0, len(secret_string) - 1]
    circuit.swap(output_qubits[pos[0]], output_qubits[pos[1]])
"""
}

BRAKET_ENTRIES["designer_simon_post_processing"] = {
    "task": "Implement the classical post-processing for Simon's Algorithm to solve the linear system over GF(2).",
    "constraints": [
        "Check linear independence",
        "Solve system using Null Space",
        "Return secret string s"
    ],
    "code": """import numpy as np
import scipy as sp

def post_processing(data, results):
    sing_values = sp.linalg.svdvals(results)
    tolerance = 1e-5
    if sum(sing_values < tolerance) == 0:
        flag = True
        null_space = sp.linalg.null_space(results).T[0]
        solution = np.around(null_space, 3)
        minval = abs(min(solution[np.nonzero(solution)], key=abs))
        solution = (solution / minval % 2).astype(int)
        data.append(str(solution))
        return flag
    return False
"""
}

BRAKET_ENTRIES["designer_stabilizer_correct"] = {
    "task": "Implement the correct method for a stabilizer code class to measure syndromes and apply corrections using Amazon Braket.",
    "constraints": [
        "Measure syndromes using ancillas",
        "Apply corrections based on syndrome mapping",
        "Handle X, Y, Z errors"
    ],
    "code": """from braket.circuits import Circuit

def stabilizer_correct(circuit, qubits, ancillas, M, syndromes_to_corrections, n, k):
    gate_map = {'X': 'x', 'Y': 'y', 'Z': 'z'}
    for r in range(n - k):
        for idx in range(n):
            if M[r][idx] == 'Z':
                circuit.cnot(qubits[idx], ancillas[r])
            elif M[r][idx] == 'X':
                circuit.h(qubits[idx])
                circuit.cnot(qubits[idx], ancillas[r])
                circuit.h(qubits[idx])
            elif M[r][idx] == 'Y':
                circuit.si(qubits[idx])
                circuit.h(qubits[idx])
                circuit.cnot(qubits[idx], ancillas[r])
                circuit.h(qubits[idx])
                circuit.s(qubits[idx])

    for syndrome, correction in syndromes_to_corrections.items():
        op = gate_map[correction[0]]
        target = correction[1]
        for r in range(n - k):
            if syndrome[r] == 1:
                circuit.x(ancillas[r])
        # Apply controlled correction
        if len(ancillas) == 2:
            circuit.ccnot(ancillas[0], ancillas[1], qubits[target])
        for r in range(n - k):
            if syndrome[r] == 1:
                circuit.x(ancillas[r])
    return circuit
"""
}

BRAKET_ENTRIES["designer_stabilizer_decode"] = {
    "task": "Implement the decode method for a stabilizer code to extract logical information from measurement results using Amazon Braket.",
    "constraints": [
        "Calculate expectation values of logical Z operators",
        "Return decoded bits"
    ],
    "code": """import numpy as np

def stabilizer_decode(measurements, logical_Zs, n):
    decoded = []
    for z_op in logical_Zs:
        # Calculate parity of qubits where Z appears
        z_qubits = [i for i, p in enumerate(z_op) if p in ('Z', 'Y')]
        parity_sum = 0
        for shot in measurements:
            parity = 1
            for q in z_qubits:
                parity *= (1 - 2 * shot[q])
            parity_sum += parity
        expectation = parity_sum / len(measurements)
        decoded.append(round((1 - expectation) / 2))
    return decoded
"""
}

BRAKET_ENTRIES["designer_stabilizer_encode"] = {
    "task": "Implement the encode method for a stabilizer code to map logical qubits to physical qubits using Amazon Braket.",
    "constraints": [
        "Use logical Xs to apply CNOTs",
        "Apply Hadamard and Phase gates based on stabilizer matrix M",
        "Generate encoding circuit"
    ],
    "code": """from braket.circuits import Circuit

def stabilizer_encode(circuit, additional_qubits, unencoded_qubits, logical_Xs, M, r, n, k):
    gate_map = {'X': 'x', 'Y': 'y', 'Z': 'z'}
    qubits = additional_qubits + unencoded_qubits

    for idx, x in enumerate(logical_Xs):
        for j in range(r, n - k):
            if x[j] == 'X' or x[j] == 'Y':
                circuit.cnot(unencoded_qubits[idx], additional_qubits[j])

    for row in range(r):
        circuit.h(qubits[row])
        if M[row][row] == 'Y' or M[row][row] == 'Z':
            circuit.s(qubits[row])
        for col in range(n):
            if col == row:
                continue
            if M[row][col] == 'I':
                continue
            op = gate_map[M[row][col]]
            circuit.cnot(qubits[row], qubits[col])
    return circuit
"""
}

BRAKET_ENTRIES["designer_stabilizer_init"] = {
    "task": "Implement the initialization logic for a stabilizer code, converting generators to standard form.",
    "constraints": [
        "Initialize with group_generators and correctable_errors",
        "Build boolean matrix M",
        "Convert to standard form",
        "Calculate logical operators"
    ],
    "code": """import numpy as np

def _build_by_code(mat):
    out = []
    n = mat.shape[1] // 2
    for i in range(mat.shape[0]):
        ps = ''
        for j in range(n):
            k = 2 * mat[i, j + n] + mat[i, j]
            ps += "IXZY"[k]
        out.append(ps)
    return out

def init_stabilizer_code(group_generators, correctable_errors):
    n = len(group_generators[0])
    k = n - len(group_generators)
    M = np.zeros((n - k, 2 * n), np.int8)
    for i, gen in enumerate(group_generators):
        for j, c in enumerate(gen):
            if c in ('X', 'Y'):
                M[i, j] = 1
            if c in ('Z', 'Y'):
                M[i, n + j] = 1

    stabilizer_matrix = _build_by_code(M)
    return {
        'n': n,
        'k': k,
        'M': stabilizer_matrix,
    }
"""
}

BRAKET_ENTRIES["designer_stabilizer_utils"] = {
    "task": "Implement utility functions for Stabilizer Codes: Pauli string conversion and Symplectic Gaussian Elimination.",
    "constraints": [
        "Implement _build_by_code",
        "Implement _gaussian_elimination",
        "Implement _transfer_to_standard_form"
    ],
    "code": """import numpy as np

def _build_by_code(mat):
    out = []
    n = mat.shape[1] // 2
    for i in range(mat.shape[0]):
        ps = ''
        for j in range(n):
            k = 2 * mat[i, j + n] + mat[i, j]
            ps += "IXZY"[k]
        out.append(ps)
    return out

def _gaussian_elimination(M, min_row, max_row, min_col, max_col):
    assert M.shape[1] % 2 == 0
    n = M.shape[1] // 2
    max_rank = min(max_row - min_row, max_col - min_col)
    rank = 0
    for r in range(max_rank):
        i = min_row + r
        j = min_col + r
        pivot_rows, pivot_cols = np.nonzero(M[i:max_row, j:max_col])
        if pivot_rows.size == 0:
            break
        pi = pivot_rows[0]
        pj = pivot_cols[0]
        M[[i, i + pi]] = M[[i + pi, i]]
        M[:, [(j + pj), j]] = M[:, [j, (j + pj)]]
        j_other_half = (j + n) % (2 * n)
        M[:, [(j_other_half + pj), j_other_half]] = M[:, [j_other_half, (j_other_half + pj)]]
        for k in range(i + 1, max_row):
            if M[k, j] == 1:
                M[k, :] = np.mod(M[i, :] + M[k, :], 2)
        rank += 1
    for r in reversed(range(rank)):
        i = min_row + r
        j = min_col + r
        for k in range(i - 1, min_row - 1, -1):
            if M[k, j] == 1:
                M[k, :] = np.mod(M[i, :] + M[k, :], 2)
    return rank

def _transfer_to_standard_form(M, n, k):
    r = _gaussian_elimination(M, 0, n - k, 0, n)
    _ = _gaussian_elimination(M, r, n - k, n + r, 2 * n)
    A2 = M[0:r, (n - k):n]
    C1 = M[0:r, (n + r):(2 * n - k)]
    C2 = M[0:r, (2 * n - k):(2 * n)]
    E = M[r:(n - k), (2 * n - k):(2 * n)]
    X = np.concatenate([
        np.zeros((k, r), dtype=np.int8), E.T, np.eye(k, dtype=np.int8),
        np.mod(E.T @ C1.T + C2.T, 2), np.zeros((k, n - r), np.int8)
    ], axis=1)
    Z = np.concatenate([
        np.zeros((k, n), dtype=np.int8), A2.T,
        np.zeros((k, n - k - r), dtype=np.int8), np.eye(k, dtype=np.int8)
    ], axis=1)
    return M, X, Z, r
"""
}

BRAKET_ENTRIES["designer_teleportation_circuit"] = {
    "task": "Implement the Quantum Teleportation circuit to transfer a state from 'msg' to 'bob' using Amazon Braket.",
    "constraints": [
        "Create Bell Pair (Alice-Bob)",
        "Perform Bell Measurement (Msg-Alice)",
        "Apply Classical Corrections (Bob) using measurement results"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit
from braket.devices import LocalSimulator

def make_quantum_teleportation_circuit(ranX, ranY):
    circuit = Circuit()
    msg, alice, bob = 0, 1, 2

    # 1. Entanglement: Creates Bell state between Alice and Bob
    circuit.h(alice)
    circuit.cnot(alice, bob)

    # 2. Preparation: Creates a random state for the Message
    circuit.rx(msg, ranX * np.pi)
    circuit.ry(msg, ranY * np.pi)

    # 3. Bell Measurement: Measure Message and Alice's entangled qubit
    circuit.cnot(msg, alice)
    circuit.h(msg)

    # Note: In Braket, mid-circuit measurement with classical feedback
    # is not supported on all devices. For simulation, we measure all at end.
    circuit.measure([msg, alice, bob])

    return circuit
"""
}

BRAKET_ENTRIES["designer_teleportation_simulation"] = {
    "task": "Simulate the teleportation circuit and verify the state transfer using Amazon Braket's state vector simulator.",
    "constraints": [
        "Calculate expected state",
        "Simulate circuit",
        "Compare expected vs actual results"
    ],
    "code": """import numpy as np
from braket.circuits import Circuit
from braket.devices import LocalSimulator

def simulate_teleportation(ranX, ranY):
    circuit = Circuit()
    msg, alice, bob = 0, 1, 2

    circuit.h(alice)
    circuit.cnot(alice, bob)
    circuit.rx(msg, ranX * np.pi)
    circuit.ry(msg, ranY * np.pi)
    circuit.cnot(msg, alice)
    circuit.h(msg)

    # For state vector simulation, don't add measurements
    device = LocalSimulator()
    result = device.run(circuit, shots=0).result()
    state_vector = result.result_types[0].value if result.result_types else None

    # For shot-based comparison
    meas_circuit = Circuit()
    meas_circuit.h(alice)
    meas_circuit.cnot(alice, bob)
    meas_circuit.rx(msg, ranX * np.pi)
    meas_circuit.ry(msg, ranY * np.pi)
    meas_circuit.cnot(msg, alice)
    meas_circuit.h(msg)
    meas_circuit.measure([msg, alice, bob])

    result = device.run(meas_circuit, shots=1000).result()
    return result.measurement_counts
"""
}

BRAKET_ENTRIES["designer_two_qubit_gate_tabulation"] = {
    "task": "Demonstrate compiling random 2-qubit unitaries using a base gate and analyzing the fidelity in Amazon Braket.",
    "constraints": [
        "Define a base 2-qubit unitary",
        "Generate random 2-qubit unitaries",
        "Compare using unitary fidelity",
        "Plot histogram of infidelities"
    ],
    "code": """import numpy as np
from scipy.stats import unitary_group
from braket.circuits import Circuit
from braket.devices import LocalSimulator

def unitary_fidelity(U, V):
    d = U.shape[0]
    return abs(np.trace(U.conj().T @ V)) ** 2 / d ** 2

def main(samples=100):
    device = LocalSimulator()

    # Generate random 2-qubit unitaries and test circuit fidelity
    infidelities = []
    for _ in range(samples):
        target = unitary_group.rvs(4)

        circuit = Circuit()
        circuit.unitary(matrix=target, targets=[0, 1])

        # Verify by simulating
        result_circuit = Circuit()
        result_circuit.unitary(matrix=target, targets=[0, 1])
        result_circuit.unitary(matrix=target.conj().T, targets=[0, 1])

        # Should be identity
        infidelity = 1.0 - unitary_fidelity(target, target)
        infidelities.append(infidelity)

    print(f"Mean infidelity: {np.mean(infidelities):.6f}")
    print(f"Max infidelity: {np.max(infidelities):.6f}")

if __name__ == '__main__':
    main()
"""
}

BRAKET_ENTRIES["modern_api_dont_use_classical_register"] = {
    "task": "Important: Amazon Braket does NOT have ClassicalRegister. Measurements are done directly with circuit.measure().",
    "constraints": [
        "NEVER use ClassicalRegister - it doesn't exist in Braket",
        "Use circuit.measure(qubits) instead",
        "Braket automatically handles classical bits internally"
    ],
    "code": """from braket.circuits import Circuit

# CORRECT - Amazon Braket measurement
circuit = Circuit()
circuit.h(0)
circuit.cnot(0, 1)
circuit.measure([0, 1])  # This is the correct way
"""
}

BRAKET_ENTRIES["modern_api_dont_use_cirq_optimizers"] = {
    "task": "Important: Amazon Braket does not have a built-in circuit optimizer module. Use scipy.optimize for variational algorithms, and Braket's built-in compilation happens at the device level.",
    "constraints": [
        "NEVER import cirq.optimizers or similar - they don't exist in Braket",
        "Braket handles compilation/optimization at the device level",
        "For VQE/QAOA parameter optimization, use scipy.optimize.minimize"
    ],
    "code": """from braket.circuits import Circuit
from scipy.optimize import minimize

# CORRECT - Amazon Braket circuit
circuit = Circuit()
circuit.h(0)
circuit.h(0)  # Redundant gate - device compiler may optimize this
circuit.cnot(0, 1)

# For VQE parameter optimization, use scipy
def objective(params):
    return 0.0  # Your cost function

result = minimize(objective, x0=[0.0], method='COBYLA')
"""
}

BRAKET_ENTRIES["modern_api_dont_use_cirq_contrib_qaoa"] = {
    "task": "Important: Amazon Braket does not have a contrib.qaoa module. Build QAOA circuits manually using circuit.zz() and circuit.rx().",
    "constraints": [
        "Build QAOA problem Hamiltonian with ZZ gates",
        "Build QAOA mixer with RX rotations",
        "Use proper angle conventions for ZZ gates"
    ],
    "code": """from braket.circuits import Circuit

# CORRECT - Amazon Braket QAOA (built manually)
circuit = Circuit()
gamma = 0.5
beta = 0.3

# Initial superposition
for q in range(3):
    circuit.h(q)

# Problem Hamiltonian (ZZ interactions for MaxCut)
edges = [(0, 1), (1, 2), (2, 0)]
for u, v in edges:
    circuit.zz(u, v, 2 * gamma)

# Mixer Hamiltonian (X rotations)
for q in range(3):
    circuit.rx(q, 2 * beta)

circuit.measure([0, 1, 2])
"""
}

BRAKET_ENTRIES["modern_api_grover_multi_controlled"] = {
    "task": "Implement Grover's algorithm for 3 qubits using Amazon Braket with Toffoli gates for multi-controlled operations.",
    "constraints": [
        "Use 3 qubits",
        "Use ccnot (Toffoli) for multi-controlled gates",
        "Always include measurements"
    ],
    "code": """from braket.circuits import Circuit

circuit = Circuit()

# Initialize superposition
for q in range(3):
    circuit.h(q)

# Oracle marking |101>
circuit.x(1)
circuit.h(2)
circuit.ccnot(0, 1, 2)  # CCZ via H-CCNot-H
circuit.h(2)
circuit.x(1)

# Diffuser (Grover diffusion operator)
for q in range(3):
    circuit.h(q)
for q in range(3):
    circuit.x(q)
circuit.h(2)
circuit.ccnot(0, 1, 2)
circuit.h(2)
for q in range(3):
    circuit.x(q)
for q in range(3):
    circuit.h(q)

# Measurement (REQUIRED)
circuit.measure([0, 1, 2])
"""
}

BRAKET_ENTRIES["modern_api_vqe_scipy_optimization"] = {
    "task": "Implement VQE with Amazon Braket using scipy for optimization and LocalSimulator for execution.",
    "constraints": [
        "Use scipy.optimize.minimize for parameter optimization",
        "Use LocalSimulator for circuit execution",
        "Build parametric ansatz with ry, rz gates",
        "Measure Hamiltonian terms separately"
    ],
    "code": """import numpy as np
from scipy.optimize import minimize
from braket.circuits import Circuit
from braket.devices import LocalSimulator

device = LocalSimulator()

def vqe_ansatz(theta):
    circuit = Circuit()
    circuit.ry(0, theta[0])
    circuit.ry(1, theta[1])
    circuit.cnot(0, 1)
    circuit.rz(1, theta[2])
    return circuit

def measure_energy(theta):
    circuit = vqe_ansatz(theta)
    circuit.measure(0)

    result = device.run(circuit, shots=1000).result()
    meas = np.array(result.measurements)
    exp_z = np.mean(1 - 2 * meas[:, 0])

    return exp_z

# Optimization loop
result = minimize(measure_energy, x0=[0.0, 0.0, 0.0], method='COBYLA')
print(f"Optimal energy: {result.fun}")
print(f"Optimal params: {result.x}")
"""
}


def convert_text(text):
    """Convert Cirq references to Braket references in text fields."""
    text = text.replace("Cirq", "Amazon Braket")
    text = text.replace("cirq", "braket")
    text = text.replace("cirq_google", "braket")
    text = text.replace("LineQubit", "qubit")
    text = text.replace("GridQubit", "qubit")
    text = text.replace("NamedQubit", "qubit")
    text = text.replace("Simulator()", "LocalSimulator()")
    text = text.replace("DensityMatrixSimulator", "LocalSimulator('braket_dm')")
    return text


def main():
    with open(INPUT, "r", encoding="utf-8") as f:
        lines = f.readlines()

    output_lines = []
    for line in lines:
        entry = json.loads(line.strip())
        entry_id = entry["id"]

        if entry_id in BRAKET_ENTRIES:
            braket = BRAKET_ENTRIES[entry_id]
            entry["task"] = braket["task"]
            entry["constraints"] = braket["constraints"]
            entry["code"] = braket["code"]
        else:
            # Fallback: just do text replacements
            entry["task"] = convert_text(entry["task"])
            entry["constraints"] = [convert_text(c) for c in entry["constraints"]]

        output_lines.append(json.dumps(entry, ensure_ascii=False))

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines) + "\n")

    print(f"Converted {len(output_lines)} entries to {OUTPUT}")


if __name__ == "__main__":
    main()
