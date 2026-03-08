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
    - Cirq circuit
    - Analysis parameters
    - Comparison circuits (optional)

Output:
    - Circuit metrics (depth, gate count, etc.)
    - Analysis report
    - Optimization suggestions
    - Comparison results (if applicable)

Dependencies:
    - Cirq: For circuit analysis
    - NetworkX: For connectivity analysis (optional)
    - NumPy: For calculations

Links to other modules:
    - Used by: OptimizerAgent, ValidatorAgent
    - Uses: Cirq analysis tools
    - Part of: Tool suite
"""

from typing import Dict, Any, Optional, List
from collections import Counter

try:
    import cirq
    CIRQ_AVAILABLE = True
except ImportError:
    CIRQ_AVAILABLE = False

from ..cirq_rag_code_assistant.config.logging import get_logger

logger = get_logger(__name__)


class CircuitAnalyzer:
    """
    Analyzes quantum circuits for structure, metrics, and optimization opportunities.
    
    Provides comprehensive circuit analysis including depth, gate counts,
    connectivity, and optimization suggestions.
    """
    
    def __init__(self):
        """Initialize the CircuitAnalyzer."""
        if not CIRQ_AVAILABLE:
            raise ImportError("Cirq is required for circuit analysis")
    
    def analyze(self, circuit: Any) -> Dict[str, Any]:
        """
        Perform comprehensive circuit analysis.
        
        Args:
            circuit: Cirq circuit to analyze
            
        Returns:
            Dictionary with analysis results
        """
        if not isinstance(circuit, cirq.Circuit):
            raise ValueError("Input must be a Cirq Circuit")
        
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
        qubits = list(circuit.all_qubits())
        operations = list(circuit.all_operations())
        
        return {
            "num_qubits": len(qubits),
            "depth": len(circuit),
            "num_operations": len(operations),
            "num_moments": len(circuit),
            "num_measurements": sum(1 for op in operations if isinstance(op.gate, cirq.MeasurementGate)),
        }
    
    def _analyze_structure(self, circuit: Any) -> Dict[str, Any]:
        """Analyze circuit structure."""
        moments = list(circuit.moments)
        
        return {
            "num_moments": len(moments),
            "moment_sizes": [len(moment) for moment in moments],
            "max_moment_size": max(len(moment) for moment in moments) if moments else 0,
            "avg_moment_size": sum(len(moment) for moment in moments) / len(moments) if moments else 0,
        }
    
    def _analyze_gates(self, circuit: Any) -> Dict[str, Any]:
        """Analyze gate usage in circuit."""
        operations = list(circuit.all_operations())
        gate_types = [type(op.gate).__name__ for op in operations if op.gate]
        gate_counts = Counter(gate_types)
        
        # Count two-qubit gates
        two_qubit_gates = sum(
            1 for op in operations
            if len(op.qubits) == 2
        )
        
        return {
            "total_gates": len(operations),
            "gate_counts": dict(gate_counts),
            "num_two_qubit_gates": two_qubit_gates,
            "num_single_qubit_gates": len(operations) - two_qubit_gates,
            "unique_gate_types": len(gate_counts),
        }
    
    def _analyze_connectivity(self, circuit: Any) -> Dict[str, Any]:
        """Analyze qubit connectivity."""
        qubits = list(circuit.all_qubits())
        operations = list(circuit.all_operations())
        
        # Count connections
        connections = set()
        for op in operations:
            if len(op.qubits) == 2:
                q1, q2 = op.qubits
                connections.add((min(q1, q2, key=str), max(q1, q2, key=str)))
        
        return {
            "num_qubits": len(qubits),
            "num_connections": len(connections),
            "connections": [str((q1, q2)) for q1, q2 in connections],
            "connectivity_ratio": len(connections) / (len(qubits) * (len(qubits) - 1) / 2) if len(qubits) > 1 else 0,
        }
    
    def _suggest_optimizations(self, circuit: Any) -> List[str]:
        """Suggest circuit optimizations."""
        suggestions = []
        
        metrics = self._calculate_metrics(circuit)
        gates = self._analyze_gates(circuit)
        
        # Check for high depth
        if metrics["depth"] > 100:
            suggestions.append("Circuit depth is high. Consider circuit optimization.")
        
        # Check for many two-qubit gates
        if gates["num_two_qubit_gates"] > metrics["num_operations"] * 0.5:
            suggestions.append("High ratio of two-qubit gates. Consider gate decomposition optimization.")
        
        # Check for measurement placement
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
        
        # Calculate differences
        for key in analysis1["metrics"]:
            val1 = analysis1["metrics"][key]
            val2 = analysis2["metrics"][key]
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                comparison["differences"][key] = val2 - val1
        
        # Identify improvements
        if comparison["differences"].get("depth", 0) < 0:
            comparison["improvements"].append("Circuit 2 has lower depth")
        
        if comparison["differences"].get("num_two_qubit_gates", 0) < 0:
            comparison["improvements"].append("Circuit 2 has fewer two-qubit gates")
        
        return comparison
