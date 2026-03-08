"""
Optimizer Agent Module

This module implements the Optimizer Agent, responsible for optimizing
quantum circuits for performance, efficiency, and hardware constraints.

Now includes RAG-based optimization guidance that retrieves reference
optimization patterns from the knowledge base.

Author: Umer Farooq, Hussain Waseem Syed, Muhammad Irtaza Khan
Email: umerfarooqcs0891@gmail.com
"""

from typing import Dict, Any, Optional, List
import cirq
from .base_agent import BaseAgent
from ..tools.analyzer import CircuitAnalyzer
from ..tools.compiler import CirqCompiler
from ..rag.generator import Generator
from ..rag.retriever import Retriever
from ..cirq_rag_code_assistant.config import get_config
from ..cirq_rag_code_assistant.config.logging import get_logger

logger = get_logger(__name__)


class OptimizerAgent(BaseAgent):
    """
    Optimizes quantum circuits with RAG-enhanced optimization guidance.
    
    Uses RAG to retrieve reference optimization patterns and apply
    appropriate Cirq optimizations based on circuit characteristics.
    """
    
    def __init__(
        self,
        retriever: Optional[Retriever] = None,
        analyzer: Optional[CircuitAnalyzer] = None,
        compiler: Optional[CirqCompiler] = None,
        generator: Optional[Generator] = None,
    ):
        """
        Initialize the OptimizerAgent.
        
        Args:
            retriever: Retriever instance for RAG-based optimization guidance (required)
            analyzer: CircuitAnalyzer instance
            compiler: CirqCompiler instance
            generator: Generator instance for LLM optimization
        """
        super().__init__(name="OptimizerAgent")
        self.retriever = retriever
        if not retriever:
            logger.warning("OptimizerAgent initialized without retriever - RAG guidance disabled")
        
        self.analyzer = analyzer or CircuitAnalyzer()
        self.compiler = compiler or CirqCompiler()
        
        # Initialize generator with optimizer config
        if generator:
            self.generator = generator
        else:
            config = get_config()
            opt_config = config.get("agents", {}).get("optimizer", {}).get("model", {})
            
            self.generator = Generator(
                retriever=retriever,  # Now uses the shared retriever
                model=opt_config.get("model", "qwen2.5-coder:14b-instruct-q4_K_M"),
                provider=opt_config.get("provider", "ollama"),
                temperature=opt_config.get("temperature", 0.2),
                max_tokens=opt_config.get("max_tokens", 2000),
            )
        
        logger.info(f"OptimizerAgent initialized (RAG: {'enabled' if retriever else 'disabled'})")
    
    def _circuit_to_code(self, circuit: cirq.Circuit) -> str:
        """
        Convert a Cirq circuit object to executable Python code.
        
        CRITICAL: str(circuit) returns ASCII diagram, NOT Python code!
        This method generates actual executable Python code from a circuit.
        """
        qubits = sorted(circuit.all_qubits(), key=str)
        
        lines = ["import cirq", ""]
        
        # Generate qubit declarations
        if qubits:
            if all(isinstance(q, cirq.LineQubit) for q in qubits):
                n_qubits = max(q.x for q in qubits) + 1
                lines.append(f"qubits = cirq.LineQubit.range({n_qubits})")
            elif all(isinstance(q, cirq.GridQubit) for q in qubits):
                for i, q in enumerate(qubits):
                    lines.append(f"q{i} = cirq.GridQubit({q.row}, {q.col})")
                lines.append(f"qubits = [{', '.join(f'q{i}' for i in range(len(qubits)))}]")
            else:
                for i, q in enumerate(qubits):
                    lines.append(f"q{i} = cirq.NamedQubit('{q}')")
                lines.append(f"qubits = [{', '.join(f'q{i}' for i in range(len(qubits)))}]")
        
        lines.append("")
        lines.append("circuit = cirq.Circuit()")
        
        qubit_to_name = {q: f"qubits[{i}]" for i, q in enumerate(qubits)}
        
        for moment in circuit.moments:
            for op in moment.operations:
                gate = op.gate
                op_qubits = [qubit_to_name[q] for q in op.qubits]
                
                if isinstance(gate, cirq.MeasurementGate):
                    key = gate.key if hasattr(gate, 'key') else 'result'
                    lines.append(f"circuit.append(cirq.measure({', '.join(op_qubits)}, key='{key}'))")
                elif isinstance(gate, cirq.HPowGate) and gate.exponent == 1:
                    lines.append(f"circuit.append(cirq.H({', '.join(op_qubits)}))")
                elif isinstance(gate, cirq.XPowGate) and gate.exponent == 1:
                    lines.append(f"circuit.append(cirq.X({', '.join(op_qubits)}))")
                elif isinstance(gate, cirq.YPowGate) and gate.exponent == 1:
                    lines.append(f"circuit.append(cirq.Y({', '.join(op_qubits)}))")
                elif isinstance(gate, cirq.ZPowGate) and gate.exponent == 1:
                    lines.append(f"circuit.append(cirq.Z({', '.join(op_qubits)}))")
                elif isinstance(gate, cirq.CNotPowGate) and gate.exponent == 1:
                    lines.append(f"circuit.append(cirq.CNOT({', '.join(op_qubits)}))")
                elif isinstance(gate, cirq.CZPowGate) and gate.exponent == 1:
                    lines.append(f"circuit.append(cirq.CZ({', '.join(op_qubits)}))")
                elif isinstance(gate, cirq.SwapPowGate) and gate.exponent == 1:
                    lines.append(f"circuit.append(cirq.SWAP({', '.join(op_qubits)}))")
                elif isinstance(gate, cirq.PhasedXZGate):
                    a = getattr(gate, 'axis_phase_exponent', 0)
                    x = getattr(gate, 'x_exponent', 0)
                    z = getattr(gate, 'z_exponent', 0)
                    lines.append(f"circuit.append(cirq.PhasedXZGate(axis_phase_exponent={a}, x_exponent={x}, z_exponent={z}).on({', '.join(op_qubits)}))")
                elif hasattr(gate, '__class__') and hasattr(gate.__class__, '__name__'):
                    gate_name = gate.__class__.__name__
                    if len(op_qubits) == 1:
                        lines.append(f"circuit.append(cirq.{gate_name}().on({op_qubits[0]}))")
                    else:
                        lines.append(f"circuit.append(cirq.{gate_name}().on({', '.join(op_qubits)}))")
                else:
                    gate_str = repr(gate)
                    if len(op_qubits) == 1:
                        lines.append(f"circuit.append({gate_str}.on({op_qubits[0]}))")
                    else:
                        lines.append(f"circuit.append({gate_str}.on({', '.join(op_qubits)}))")
        
        lines.append("")
        lines.append("print(circuit)")
        
        return "\n".join(lines)
    
    def _retrieve_optimization_references(
        self,
        code: str,
        algorithm: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve optimization references from knowledge base.
        
        Args:
            code: The code to optimize
            algorithm: Algorithm type if known
            
        Returns:
            List of optimization reference entries
        """
        if not self.retriever:
            return []
        
        # Build query for optimization patterns
        query_parts = ["optimize", "circuit", "reduce", "depth", "gates"]
        if algorithm:
            query_parts.insert(1, algorithm)
        query = " ".join(query_parts)
        
        try:
            results = self.retriever.retrieve(query=query, top_k=3)
            return results
        except Exception as e:
            logger.warning(f"Failed to retrieve optimization references: {e}")
            return []
    
    def _select_optimizations(
        self,
        circuit: cirq.Circuit,
        references: List[Dict[str, Any]],
        level: str,
    ) -> List[str]:
        """
        Select which Cirq optimizations to apply based on references and circuit analysis.
        
        Returns list of optimization function names to apply.
        """
        optimizations = []
        
        # Always do single-qubit merge (it's safe and usually beneficial)
        optimizations.append("merge_single_qubit_gates_to_phxz")
        
        # Check references for suggestions
        for ref in references:
            entry = ref.get("entry", {})
            cirq_opt = entry.get("cirq_optimization", "")
            
            if "drop_negligible" in cirq_opt:
                if "drop_negligible_operations" not in optimizations:
                    optimizations.append("drop_negligible_operations")
            if "eject_z" in cirq_opt:
                if "eject_z" not in optimizations:
                    optimizations.append("eject_z")
            if "eject_phased_paulis" in cirq_opt:
                if "eject_phased_paulis" not in optimizations:
                    optimizations.append("eject_phased_paulis")
        
        # Add optimizations based on level
        if level in ["balanced", "aggressive"]:
            if "drop_negligible_operations" not in optimizations:
                optimizations.append("drop_negligible_operations")
        
        if level == "aggressive":
            if "eject_z" not in optimizations:
                optimizations.append("eject_z")
            if "eject_phased_paulis" not in optimizations:
                optimizations.append("eject_phased_paulis")
        
        return optimizations
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize a quantum circuit with RAG guidance.
        
        Args:
            task: Task dictionary with:
                - code: The Cirq code to optimize
                - circuit: Or a circuit object directly
                - algorithm: Algorithm type for RAG lookup
                - optimization_level: "minimal", "balanced", or "aggressive"
                - use_rl: Whether to use RL optimization
                - use_llm: Whether to use LLM optimization
                - use_heuristics: Whether to use Cirq heuristics (default True)
            
        Returns:
            Result dictionary with optimized code and metrics
        """
        code = task.get("code")
        circuit = task.get("circuit")
        algorithm = task.get("algorithm")
        optimization_level = task.get("optimization_level", "balanced")
        
        if not code and not circuit:
            return {
                "success": False,
                "error": "Either 'code' or 'circuit' is required",
            }
        
        try:
            # Get circuit object
            if code:
                compiled = self.compiler.compile(code, execute=True)
                if not compiled["success"] or not compiled.get("circuit"):
                    # Try to fix compilation errors using LLM
                    logger.warning(f"Initial compilation failed: {compiled.get('errors')}")
                    logger.info("Attempting to fix code with LLM...")
                    
                    # Build error description
                    error_messages = []
                    for err in compiled.get("errors", []):
                        if isinstance(err, dict):
                            error_messages.append(err.get("message", str(err)))
                        else:
                            error_messages.append(str(err))
                    error_desc = "\n".join(error_messages)
                    
                    # Use LLM to fix the code
                    fix_prompt = f"""Fix the following Cirq code that has compilation/execution errors.

Original Code:
{code}

Errors:
{error_desc}

Instructions:
1. Fix all compilation and execution errors
2. Ensure the code creates a circuit variable that can be executed
3. For QAOA: NEVER use cirq.contrib.qaoa - build manually with cirq.ZZ and cirq.rx
4. For VQE: Ensure the circuit is created and assigned to a variable (not just returned from a function)
5. Return ONLY the fixed, executable Cirq code

Fixed code:"""
                    
                    try:
                        fix_result = self.generator.generate_direct(query=fix_prompt)
                        fixed_code = fix_result.get("code", "")
                        
                        if fixed_code:
                            # Try compiling the fixed code
                            fixed_compiled = self.compiler.compile(fixed_code, execute=True)
                            if fixed_compiled["success"] and fixed_compiled.get("circuit"):
                                logger.info("✅ LLM successfully fixed compilation errors")
                                code = fixed_code  # Use the fixed code
                                compiled = fixed_compiled
                            else:
                                logger.warning(f"LLM fix still has errors: {fixed_compiled.get('errors')}")
                    except Exception as e:
                        logger.warning(f"LLM fix attempt failed: {e}")
                    
                    # If still no circuit, return error
                    if not compiled["success"] or not compiled.get("circuit"):
                        return {
                            "success": False,
                            "error": f"Failed to compile code: {compiled.get('errors')}",
                        }
                
                circuit = compiled["circuit"]
            
            if not isinstance(circuit, cirq.Circuit):
                return {
                    "success": False,
                    "error": "Invalid circuit object",
                }
            
            # Analyze original circuit
            original_analysis = self.analyzer.analyze(circuit)
            
            # Track original code for comparison
            original_code = code if code else self._circuit_to_code(circuit)
            
            # Retrieve optimization references from RAG
            references = self._retrieve_optimization_references(code or "", algorithm)
            if references:
                logger.info(f"Retrieved {len(references)} optimization references from RAG")
            
            # Initialize optimized versions
            optimized_circuit = circuit
            optimized_code = original_code
            
            # 1. LLM Optimization (if requested)
            if task.get("use_llm", False):
                logger.info("Running LLM optimization")
                llm_result = self._optimize_with_llm(optimized_code, references)
                if llm_result.get("success"):
                    optimized_code = llm_result["code"]
                    compiled = self.compiler.compile(optimized_code, execute=True)
                    if compiled["success"]:
                        optimized_circuit = compiled["circuit"]
                    else:
                        logger.warning(f"LLM optimization produced invalid code: {compiled.get('errors')}")
                else:
                    logger.warning(f"LLM optimization failed: {llm_result.get('error')}")

            # 2. Heuristic Optimization (default)
            if task.get("use_heuristics", True):
                # Select optimizations based on RAG references
                optimizations = self._select_optimizations(optimized_circuit, references, optimization_level)
                logger.debug(f"Selected optimizations: {optimizations}")
                
                optimized_circuit = self._optimize_circuit(optimized_circuit, optimizations)
                optimized_code = self._circuit_to_code(optimized_circuit)
            
            # 3. RL Optimization
            if task.get("use_rl", False):
                optimized_circuit = self._optimize_with_rl(optimized_circuit)
                optimized_code = self._circuit_to_code(optimized_circuit)
                
            # Final Analysis
            optimized_analysis = self.analyzer.analyze(optimized_circuit)
            
            # Compare results
            comparison = self.analyzer.compare(circuit, optimized_circuit)
            
            return {
                "success": True,
                "original_code": original_code,
                "optimized_code": optimized_code,
                "original_metrics": original_analysis["metrics"],
                "optimized_metrics": optimized_analysis["metrics"],
                "improvements": comparison.get("improvements", []),
                "differences": comparison.get("differences", {}),
                "optimizations_applied": self._select_optimizations(circuit, references, optimization_level),
                "rag_references_used": len(references),
            }
        
        except Exception as e:
            logger.error(f"OptimizerAgent error: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    def _optimize_with_llm(
        self,
        code: str,
        references: List[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Optimize circuit code using LLM with RAG context.
        """
        # Build context from references
        context = ""
        if references:
            context_parts = []
            for ref in references[:2]:  # Use top 2 references
                entry = ref.get("entry", {})
                if entry.get("optimized_code"):
                    context_parts.append(f"Example optimization:\n{entry.get('optimized_code')}")
            context = "\n\n".join(context_parts)
        
        prompt = f"""Optimize the following Cirq code to reduce circuit depth and gate count while maintaining the same quantum logic.

Original Code:
{code}

{f"Reference optimizations from knowledge base:{chr(10)}{context}" if context else ""}

Instructions:
1. Analyze the circuit for redundant gates and inefficient patterns.
2. Apply circuit identities and optimizations to reduce depth and gate count.
3. CRITICAL: PRESERVE the original qubit initialization method and variable names.
4. Return ONLY the full, executable Cirq code for the optimized circuit.
5. Do not include explanations, just the code.
"""
        
        try:
            result = self.generator.generate_direct(query=prompt)
            return {
                "success": True,
                "code": result["code"],
                "explanation": result.get("description", "")
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _optimize_circuit(self, circuit: cirq.Circuit, optimizations: List[str]) -> cirq.Circuit:
        """Apply selected Cirq optimizations to circuit."""
        optimized = circuit.copy()
        
        for opt_name in optimizations:
            try:
                if opt_name == "merge_single_qubit_gates_to_phxz":
                    optimized = cirq.merge_single_qubit_gates_to_phxz(optimized)
                elif opt_name == "drop_negligible_operations":
                    optimized = cirq.drop_negligible_operations(optimized)
                elif opt_name == "eject_z":
                    optimized = cirq.eject_z(optimized)
                elif opt_name == "eject_phased_paulis":
                    optimized = cirq.eject_phased_paulis(optimized)
                elif opt_name == "expand_composite":
                    optimized = cirq.expand_composite(optimized)
                elif opt_name == "defer_measurements":
                    optimized = cirq.defer_measurements(optimized)
            except Exception as e:
                logger.warning(f"Optimization {opt_name} failed: {e}")
        
        return optimized

    def _optimize_with_rl(self, circuit: cirq.Circuit) -> cirq.Circuit:
        """Apply Reinforcement Learning based optimization."""
        from ..cirq_rag_code_assistant.config import get_config
        config = get_config()
        rl_config = config.get("agents", {}).get("optimizer", {})
        weights = rl_config.get("rl_reward_weights", {})
        iterations = rl_config.get("rl_iterations", 10)
        
        current_circuit = circuit.copy()
        current_metrics = self.analyzer.analyze(current_circuit)["metrics"]
        current_reward = self._calculate_reward(current_metrics, weights)
        
        logger.info(f"Starting RL optimization (iterations={iterations})")
        
        transformations = [
            cirq.merge_single_qubit_gates_to_phxz,
            cirq.drop_negligible_operations,
            cirq.eject_z,
            cirq.eject_phased_paulis,
            cirq.expand_composite,
            cirq.defer_measurements,
        ]
        
        for i in range(iterations):
            best_next_circuit = current_circuit
            best_next_reward = current_reward
            improved = False
            
            for transform in transformations:
                try:
                    candidate = transform(current_circuit)
                    metrics = self.analyzer.analyze(candidate)["metrics"]
                    reward = self._calculate_reward(metrics, weights)
                    
                    if reward > best_next_reward:
                        best_next_circuit = candidate
                        best_next_reward = reward
                        improved = True
                except Exception:
                    continue
            
            if improved:
                current_circuit = best_next_circuit
                current_reward = best_next_reward
                logger.debug(f"RL Iteration {i+1}: Improved reward to {current_reward:.4f}")
            else:
                logger.debug(f"RL Iteration {i+1}: No improvement")
                break
                
        return current_circuit

    def _calculate_reward(self, metrics: Dict[str, Any], weights: Dict[str, float]) -> float:
        """Calculate reward based on circuit metrics and weights."""
        reward = 0.0
        
        if "depth" in metrics:
            reward += weights.get("circuit_depth", -0.1) * metrics["depth"]
        if "num_operations" in metrics:
            reward += weights.get("total_gate_count", -0.1) * metrics["num_operations"]
        if "2_qubit_gate_count" in metrics:
            reward += weights.get("two_qubit_gates", -0.5) * metrics["2_qubit_gate_count"]
            
        return reward
