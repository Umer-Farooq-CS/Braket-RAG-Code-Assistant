from braket.circuits import Circuit
circuit = Circuit()
circuit.h(0)
circuit.cnot(0, 1)
print(circuit)
