"""
RAG Generator Module

This module implements the generation component of the RAG system.
It combines retrieved context with LLM capabilities to generate
Cirq code from natural language descriptions.

Author: Umer Farooq, Hussain Waseem Syed, Muhammad Irtaza Khan
Email: umerfarooqcs0891@gmail.com

Purpose:
    - Generate Cirq code from natural language + retrieved context
    - Combine RAG retrieval with LLM generation
    - Apply code templates and best practices
    - Ensure syntax correctness and Cirq conventions

Input:
    - Natural language description
    - Retrieved context (code examples, documentation)
    - Algorithm type and parameters
    - Generation parameters (temperature, max_tokens, etc.)

Output:
    - Generated Cirq code
    - Code metadata (algorithm, complexity, imports)
    - Generation confidence scores
    - Explanation of code structure

Dependencies:
    - Retriever: For context retrieval
    - LLM API (OpenAI/Anthropic): For code generation
    - Code templates: For structured generation
    - Cirq: For code validation

Links to other modules:
    - Used by: DesignerAgent
    - Uses: Retriever, LLM APIs, Code templates
    - Part of: RAG system pipeline
"""

import os
import re
from typing import Dict, Optional, Any, List

import requests

from .retriever import Retriever

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from ..cirq_rag_code_assistant.config import get_config
from ..cirq_rag_code_assistant.config.logging import get_logger

logger = get_logger(__name__)


class Generator:
    """
    Generates Cirq code using RAG (Retrieval-Augmented Generation).
    
    Combines retrieved context from the knowledge base with LLM capabilities
    to generate accurate, executable Cirq code.
    """
    
    # Code generation prompt template (with RAG context)
    PROMPT_TEMPLATE = """You are an expert quantum computing programmer specializing in Google's Cirq framework.

Your task is to generate syntactically correct, executable Cirq code based on the user's request and the provided examples.

Context from knowledge base:
{context}

User request: {query}

Instructions:
1. Generate complete, executable Cirq code that fulfills the user's request
2. Follow Cirq best practices and conventions
3. Include necessary imports
4. Add comments explaining key steps
5. Ensure the code is syntactically correct and can be executed

Generated code:"""

    # Direct prompt template (without RAG context)
    DIRECT_PROMPT_TEMPLATE = """You are an expert quantum computing programmer specializing in Google's Cirq framework.

Your task is to generate syntactically correct, executable Cirq code based on the user's request.

User request: {query}

Instructions:
1. Generate complete, executable Cirq code that fulfills the user's request
2. Follow Cirq best practices and conventions
3. Include necessary imports
4. Add comments explaining key steps
5. Ensure the code is syntactically correct and can be executed

Generated code:"""

    def __init__(
        self,
        retriever: Optional[Retriever] = None,
        model: Optional[str] = None,
        provider: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ):
        """
        Initialize the Generator.
        
        Args:
            retriever: Retriever instance for context retrieval (optional if only using direct generation)
            model: LLM model name (defaults to config.agents.designer.model.model)
            provider: LLM provider ("openai", "anthropic", or "ollama"; defaults to config.agents.designer.model.provider)
            temperature: Generation temperature (defaults to config.agents.designer.model.temperature or 0.2)
            max_tokens: Maximum tokens to generate (defaults to config.agents.designer.model.max_tokens or 2000)
        """
        self.retriever = retriever

        # Load defaults from configuration if not explicitly provided
        cfg = get_config()
        designer_cfg = cfg.get("agents", {}).get("designer", {}).get("model", {})
        model = model or designer_cfg.get("model", "gpt-4")
        provider = (provider or designer_cfg.get("provider", "openai")).lower()
        if temperature is None:
            temperature = designer_cfg.get("temperature", 0.2)
        if max_tokens is None:
            max_tokens = designer_cfg.get("max_tokens", 2000)

        self.model = model
        self.provider = provider
        self.temperature = float(temperature)
        self.max_tokens = int(max_tokens)
        
        # Initialize LLM client
        if self.provider == "ollama":
            # Ollama uses a local HTTP API; no SDK client object is required.
            # The base URL can be overridden with the OLLAMA_HOST environment variable.
            self.ollama_base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
            self.client = None
        elif self.provider == "openai":
            if not OPENAI_AVAILABLE:
                raise ImportError(
                    "OpenAI library is required. "
                    "Install it with: pip install openai"
                )
            # OpenAI client will use OPENAI_API_KEY env var automatically
            self.client = OpenAI()
        elif self.provider == "anthropic":
            if not ANTHROPIC_AVAILABLE:
                raise ImportError(
                    "Anthropic library is required. "
                    "Install it with: pip install anthropic"
                )
            # Anthropic client will use ANTHROPIC_API_KEY env var automatically
            self.client = anthropic.Anthropic()
        else:
            raise ValueError(f"Unsupported provider: {provider}. Use 'ollama', 'openai', or 'anthropic'.")
        
        logger.info(f"Initialized Generator with {provider}/{model}")
    
    def generate(
        self,
        query: str,
        algorithm: Optional[str] = None,
        top_k: int = 3,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate Cirq code from a natural language query.
        
        Args:
            query: Natural language description of desired code
            algorithm: Optional algorithm type (e.g., "vqe", "qaoa")
            top_k: Number of examples to retrieve for context
            **kwargs: Additional generation parameters
            
        Returns:
            Dictionary with generated code, metadata, and confidence
        """
        # Retrieve relevant context
        if self.retriever:
            logger.info(f"Retrieving context for query: {query[:50]}...")
            context_results = self.retriever.retrieve(
                query=query,
                top_k=top_k,
                algorithm=algorithm,
            )
            
            # Format context
            context = self.retriever.retrieve_context(
                query=query,
                top_k=top_k,
                algorithm=algorithm,
            )
        else:
            logger.info("No retriever provided, skipping context retrieval")
            context_results = []
            context = ""
        
        # Build prompt with algorithm-specific constraints
        algorithm_constraints = ""
        if algorithm and algorithm.lower() == "qaoa":
            algorithm_constraints = """

CRITICAL CONSTRAINTS FOR QAOA:
- NEVER import or use cirq.contrib.qaoa - this module does NOT exist in modern Cirq
- Build QAOA circuits manually using cirq.ZZ gates for the problem Hamiltonian
- Use cirq.rx rotations for the mixer Hamiltonian
- Use np.pi in ZZ exponents for correct phase: cirq.ZZ(qubits[u], qubits[v]) ** (-2 * gamma / np.pi)
- Always create a circuit variable that can be executed and measured
"""
        
        # Build prompt
        prompt = self.PROMPT_TEMPLATE.format(
            context=context if context else "No relevant examples found.",
            query=query,
        )
        
        # Add algorithm-specific constraints if any
        if algorithm_constraints:
            prompt = prompt + algorithm_constraints
        
        # Generate code using LLM
        logger.info(f"Generating code using {self.provider}/{self.model}")
        
        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert Cirq quantum computing programmer."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    **kwargs
                )
                generated_text = response.choices[0].message.content
            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    **kwargs
                )
                generated_text = response.content[0].text
            else:  # ollama - uses Modelfile's SYSTEM prompt
                url = f"{self.ollama_base_url.rstrip('/')}/api/generate"
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",  # Request JSON output
                }
                resp = requests.post(url, json=payload, timeout=kwargs.get("timeout", 300))
                resp.raise_for_status()
                data = resp.json()
                generated_text = data.get("response", "")
            
            # Extract code from response (handles both JSON and raw formats)
            code, description = self._extract_code_from_response(generated_text)
            
            # Extract metadata
            metadata = self._extract_metadata(code, algorithm)
            metadata["description"] = description
            
            result = {
                "code": code,
                "description": description,
                "raw_response": generated_text,
                "metadata": metadata,
                "context_used": len(context_results),
                "algorithm": algorithm,
            }
            
            logger.info("✅ Code generation completed")
            return result
            
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            raise
    
    def _extract_code_from_response(self, text: str) -> tuple:
        """
        Extract code and description from LLM response.
        
        Handles JSON format from Modelfile: {"code": "...", "description": "..."}
        Falls back to legacy extraction if JSON parsing fails.
        
        Args:
            text: LLM response text
            
        Returns:
            Tuple of (code, description)
        """
        import json
        
        # Try to parse as JSON first (from Modelfile format)
        try:
            # Handle potential JSON wrapped in markdown code blocks
            clean_text = text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.startswith("```"):
                clean_text = clean_text[3:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            clean_text = clean_text.strip()
            
            data = json.loads(clean_text)
            code = data.get("code", "")
            description = data.get("description", "")
            
            if code:
                logger.debug("Successfully extracted code from JSON response")
                return code, description
        except json.JSONDecodeError:
            logger.debug("Response is not JSON, falling back to code extraction")
        
        # Fallback to legacy extraction
        code = self._extract_code(text)
        return code, ""
    
    def _extract_code(self, text: str) -> str:
        """
        Extract code block from LLM response (legacy method).
        
        Args:
            text: LLM response text
            
        Returns:
            Extracted code string
        """
        # Try to find code blocks
        code_block_pattern = r"```(?:python)?\n?(.*?)```"
        matches = re.findall(code_block_pattern, text, re.DOTALL)
        
        if matches:
            # Return the first code block
            return matches[0].strip()
        
        # If no code block, try to find import statements and code
        lines = text.split('\n')
        code_lines = []
        in_code = False
        
        for line in lines:
            # Start collecting when we see an import
            if 'import' in line and ('cirq' in line.lower() or 'numpy' in line.lower()):
                in_code = True
            
            if in_code:
                code_lines.append(line)
        
        if code_lines:
            return '\n'.join(code_lines).strip()
        
        # Fallback: return the entire text
        return text.strip()
    
    def _extract_metadata(self, code: str, algorithm: Optional[str]) -> Dict[str, Any]:
        """
        Extract metadata from generated code.
        
        Args:
            code: Generated code
            algorithm: Algorithm type if known
            
        Returns:
            Metadata dictionary
        """
        metadata = {
            "code_length": len(code),
            "num_lines": len(code.split('\n')),
            "has_imports": "import" in code,
            "has_cirq": "cirq" in code.lower(),
        }
        
        # Extract imports
        import_pattern = r"(?:^|\n)(?:import|from)\s+([^\s]+)"
        imports = re.findall(import_pattern, code, re.MULTILINE)
        if imports:
            metadata["imports"] = imports
        
        # Detect algorithm if not provided
        if not algorithm:
            algorithm_patterns = {
                "vqe": r"vqe|variational|eigensolver",
                "qaoa": r"qaoa|max.?cut",
                "grover": r"grover|amplitude",
                "qft": r"qft|fourier",
                "teleportation": r"teleport|bell",
            }
            
            code_lower = code.lower()
            for algo, pattern in algorithm_patterns.items():
                if re.search(pattern, code_lower):
                    metadata["detected_algorithm"] = algo
                    break
        
        return metadata

    def build_prompt(
        self,
        query: str,
        algorithm: Optional[str] = None,
        top_k: int = 3,
    ) -> Dict[str, Any]:
        """
        Build the full RAG prompt and return it along with the context.
        
        This method is useful for inspecting what the RAG system sends to the LLM.
        
        Args:
            query: Natural language description of desired code
            algorithm: Optional algorithm type (e.g., "vqe", "qaoa")
            top_k: Number of examples to retrieve for context
            
        Returns:
            Dictionary with full_prompt, context, and context_results
        """
        if self.retriever:
            # Retrieve relevant context
            context_results = self.retriever.retrieve(
                query=query,
                top_k=top_k,
                algorithm=algorithm,
            )
            
            # Format context
            context = self.retriever.retrieve_context(
                query=query,
                top_k=top_k,
                algorithm=algorithm,
            )
        else:
            context_results = []
            context = ""
        
        # Build prompt
        full_prompt = self.PROMPT_TEMPLATE.format(
            context=context if context else "No relevant examples found.",
            query=query,
        )
        
        return {
            "full_prompt": full_prompt,
            "context": context,
            "context_results": context_results,
            "num_examples": len(context_results),
        }

    def build_direct_prompt(self, query: str) -> str:
        """
        Build the direct LLM prompt (without RAG context).
        
        Args:
            query: Natural language description of desired code
            
        Returns:
            The formatted direct prompt string
        """
        return self.DIRECT_PROMPT_TEMPLATE.format(query=query)

    def generate_direct(
        self,
        query: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate Cirq code directly from the LLM without RAG context.
        
        This method is useful for comparing RAG-augmented generation with
        direct LLM generation.
        
        Args:
            query: Natural language description of desired code
            **kwargs: Additional generation parameters
            
        Returns:
            Dictionary with generated code and metadata
        """
        # Build direct prompt (no RAG context)
        prompt = self.DIRECT_PROMPT_TEMPLATE.format(query=query)
        
        logger.info(f"Generating code directly (no RAG) using {self.provider}/{self.model}")
        
        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert Cirq quantum computing programmer."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    **kwargs
                )
                generated_text = response.choices[0].message.content
            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    **kwargs
                )
                generated_text = response.content[0].text
            else:  # ollama
                url = f"{self.ollama_base_url.rstrip('/')}/api/chat"
                payload = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are an expert Cirq quantum computing programmer."},
                        {"role": "user", "content": prompt},
                    ],
                    "stream": False,
                    "options": {
                        "temperature": self.temperature,
                        "num_predict": self.max_tokens,
                    },
                }
                resp = requests.post(url, json=payload, timeout=kwargs.get("timeout", 300))
                resp.raise_for_status()
                data = resp.json()
                generated_text = data.get("message", {}).get("content", "")
            
            # Extract code from response (handles both JSON and raw formats)
            code, description = self._extract_code_from_response(generated_text)
            
            # Extract metadata
            metadata = self._extract_metadata(code, None)
            
            result = {
                "code": code,
                "description": description,
                "raw_response": generated_text,
                "metadata": metadata,
                "context_used": 0,  # No RAG context used
                "method": "direct_llm",
            }
            
            logger.info("✅ Direct code generation completed")
            return result
            
        except Exception as e:
            logger.error(f"Error generating code directly: {e}")
            raise

