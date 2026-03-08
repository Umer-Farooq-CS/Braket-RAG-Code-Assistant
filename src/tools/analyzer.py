"""
Circuit Analyzer Tool Module

This module implements the circuit analysis tool for analyzing
circuit structure, metrics, and optimization opportunities.

Author: Umer Farooq, Hussain Waseem Syed, Muhammad Irtaza Khan
Email: umerfarooqcs0891@gmail.com

Purpose:
    - Analyze circuit structure and metrics
    - Calculate depth, gate count, connectivity
    - Identify optimization opportunities
    - Generate analysis reports
    - Compare circuit variants

Input:
    - Braket circuit
    - Analysis parameters
    - Comparison circuits (optional)

Output:
    - Circuit metrics (depth, gate count, etc.)
    - Analysis report
    - Optimization suggestions
    - Comparison results (if applicable)

Dependencies:
    - Amazon Braket SDK: For circuit analysis
    - NetworkX: For connectivity analysis (optional)
    - NumPy: For calculations

Links to other modules:
    - Used by: OptimizerAgent, ValidatorAgent
    - Uses: Braket analysis tools
    - Part of: Tool suite
"""

from typing import Dict, Any, Optional, List
from collections import Counter

try:
    from braket.circuits import Circuit, gates
    BRAKET_AVAILABLE = True
except ImportError:
    BRAKET_AVAILABLE = False

from ..braket_rag_code_assistant.config.logging import get_logger

logger = get_logger(__name__)


class CircuitAnalyzer:
    """
    Analyzes quantum circuits for structure, metrics, and optimization opportunities.
    
    Provides comprehensive circuit analysis including depth, gate counts,
    connectivity, and optimization suggestions.
    """
    
    def __init__(self):
        """Initialize the CircuitAnalyzer."""
        if not BRAKET_AVAILABLE:
            raise ImportError("Amazon Braket SDK is required for circuit analysis")
    
    def analyze(self, circuit: Any) -> Dict[str, Any]:
        """
        Perform comprehensive circuit analysis.
        
        Args:
            circuit: Braket Circuit to analyze
            
        Returns:
            Dictionary with analysis results
        """
        if not isinstance(circuit, Circuit):
            raise ValueError("Input must be a Braket Circuit")
        
        analysis = {
            "success": True,
            "metrics": self._calculate_metrics(circuit),
            "structure": self._analyze_structure(circuit),
            "gates": self._analyze_gates(circuit),
            "connectivity": self._analyze_connectivity(circuit),
            "optimization_suggestions": self._suggest_optimizations(circuit),
        }
        
        return analysis
    
    def _calculate_metrics(self, circuit: Any) -> Dict[str, Any]:
        """Calculate basic circuit metrics."""
        instructions = circuit.instructions
        
        num_measurements = sum(
            1 for inst in instructions
            if inst.operator.name == "Measure"
        )
        
        return {
            "num_qubits": circuit.qubit_count,
            "depth": circuit.depth,
            "num_operations": len(instructions),
            "num_moments": circuit.depth,
            "num_measurements": num_measurements,
        }
    
    def _analyze_structure(self, circuit: Any) -> Dict[str, Any]:
        """Analyze circuit structure."""
        depth = circuit.depth
        num_instructions = len(circuit.instructions)
        
        avg_ops_per_layer = num_instructions / depth if depth > 0 else 0
        
        return {
            "num_moments": depth,
            "total_instructions": num_instructions,
            "avg_ops_per_layer": avg_ops_per_layer,
        }
    
    def _analyze_gates(self, circuit: Any) -> Dict[str, Any]:
        """Analyze gate usage in circuit."""
        instructions = circuit.instructions
        gate_types = [inst.operator.name for inst in instructions]
        gate_counts = Counter(gate_types)
        
        two_qubit_gates = sum(
            1 for inst in instructions
            if len(inst.target) == 2
        )
        
        return {
            "total_gates": len(instructions),
            "gate_counts": dict(gate_counts),
            "num_two_qubit_gates": two_qubit_gates,
            "num_single_qubit_gates": len(instructions) - two_qubit_gates,
            "unique_gate_types": len(gate_counts),
        }
    
    def _analyze_connectivity(self, circuit: Any) -> Dict[str, Any]:
        """Analyze qubit connectivity."""
        num_qubits = circuit.qubit_count
        instructions = circuit.instructions
        
        connections = set()
        for inst in instructions:
            if len(inst.target) == 2:
                q1, q2 = inst.target[0], inst.target[1]
                connections.add((min(q1, q2), max(q1, q2)))
        
        max_connections = num_qubits * (num_qubits - 1) / 2 if num_qubits > 1 else 1
        
        return {
            "num_qubits": num_qubits,
            "num_connections": len(connections),
            "connections": [str((q1, q2)) for q1, q2 in connections],
            "connectivity_ratio": len(connections) / max_connections if num_qubits > 1 else 0,
        }
    
    def _suggest_optimizations(self, circuit: Any) -> List[str]:
        """Suggest circuit optimizations."""
        suggestions = []
        
        metrics = self._calculate_metrics(circuit)
        gates_info = self._analyze_gates(circuit)
        
        if metrics["depth"] > 100:
            suggestions.append("Circuit depth is high. Consider circuit optimization.")
        
        if gates_info["num_two_qubit_gates"] > metrics["num_operations"] * 0.5:
            suggestions.append("High ratio of two-qubit gates. Consider gate decomposition optimization.")
        
        if metrics["num_measurements"] == 0:
            suggestions.append("No measurements found. Add measurements to observe results.")
        
        return suggestions
    
    def compare(
        self,
        circuit1: Any,
        circuit2: Any,
    ) -> Dict[str, Any]:
        """
        Compare two circuits.
        
        Args:
            circuit1: First circuit
            circuit2: Second circuit
            
        Returns:
            Comparison results
        """
        analysis1 = self.analyze(circuit1)
        analysis2 = self.analyze(circuit2)
        
        comparison = {
            "circuit1": analysis1["metrics"],
            "circuit2": analysis2["metrics"],
            "differences": {},
            "improvements": [],
        }
        
        for key in analysis1["metrics"]:
            val1 = analysis1["metrics"][key]
            val2 = analysis2["metrics"][key]
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                comparison["differences"][key] = val2 - val1
        
        if comparison["differences"].get("depth", 0) < 0:
            comparison["improvements"].append("Circuit 2 has lower depth")
        
        if comparison["differences"].get("num_two_qubit_gates", 0) < 0:
            comparison["improvements"].append("Circuit 2 has fewer two-qubit gates")
        
        return comparison
