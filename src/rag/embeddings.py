"""
Embedding Model Module

This module implements the embedding generation for the RAG system.
It uses sentence transformers to create semantic embeddings for
text queries and code snippets.

Author: Umer Farooq, Hussain Waseem Syed, Muhammad Irtaza Khan
Email: umerfarooqcs0891@gmail.com

Purpose:
    - Generate embeddings for natural language queries
    - Generate embeddings for Cirq code snippets
    - Support batch processing for efficiency
    - Leverage PyTorch CUDA for acceleration

Input:
    - Text strings (queries, code, documentation)
    - Batch of texts for batch processing
    - Model configuration parameters

Output:
    - Vector embeddings (typically 384 or 768 dimensions)
    - Embedding metadata
    - Processing statistics

Dependencies:
    - Sentence Transformers: For embedding models
    - PyTorch: For GPU acceleration
    - NumPy: For array operations
    - Transformers (Hugging Face): For model loading

Links to other modules:
    - Used by: Retriever, VectorStore, KnowledgeBase
    - Uses: Sentence Transformers, PyTorch
    - Part of: RAG system pipeline
"""

import os
from typing import List, Union, Optional, Dict, Any
import numpy as np
from pathlib import Path

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

from ..cirq_rag_code_assistant.config import get_config
from ..cirq_rag_code_assistant.config.logging import get_logger

logger = get_logger(__name__)


class EmbeddingModel:
    """
    Generates semantic embeddings for text and code using sentence transformers.
    
    Supports GPU acceleration via PyTorch CUDA and batch processing for efficiency.
    """
    
    def __init__(
        self,
        model_name: Optional[str] = None,
        device: Optional[str] = None,
        cache_folder: Optional[str] = None,
    ):
        """
        Initialize the EmbeddingModel.
        
        Args:
            model_name: Name of the sentence transformer model.
                       Defaults to config value
            device: Device to run model on ("cpu", "cuda", "auto").
                   Defaults to config value
            cache_folder: Folder to cache model files
        """
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError(
                "sentence-transformers is required. "
                "Install it with: pip install sentence-transformers"
            )
        
        config = get_config()
        self.model_name = model_name or config.get("models.embedding.model_name", "BAAI/bge-base-en-v1.5")
        self.device = self._determine_device(device)
        self.cache_folder = cache_folder
        
        # Initialize model
        logger.info(f"Loading embedding model: {self.model_name}")
        logger.info(f"Using device: {self.device}")
        
        try:
            self.model = SentenceTransformer(
                self.model_name,
                device=self.device,
                cache_folder=self.cache_folder,
            )
            logger.info("✅ Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise
        
        # Get embedding dimension
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        logger.info(f"Embedding dimension: {self.embedding_dim}")
        
        # Statistics
        self.stats = {
            "total_embeddings": 0,
            "total_batches": 0,
            "total_texts": 0,
        }
    
    def _determine_device(self, device: Optional[str] = None) -> str:
        """Determine the device to use for embeddings."""
        if device:
            return device
        
        config = get_config()
        torch_device = config.get("pytorch.torch_device", "auto")
        
        if torch_device == "auto":
            if TORCH_AVAILABLE and torch.cuda.is_available():
                return "cuda"
            return "cpu"
        
        return torch_device
    
    def encode(
        self,
        texts: Union[str, List[str]],
        batch_size: int = 32,
        show_progress_bar: bool = False,
        normalize_embeddings: bool = True,
        convert_to_numpy: bool = True,
    ) -> np.ndarray:
        """
        Generate embeddings for input texts.
        
        Args:
            texts: Single text string or list of texts
            batch_size: Batch size for processing
            show_progress_bar: Whether to show progress bar
            normalize_embeddings: Whether to normalize embeddings to unit length
            convert_to_numpy: Whether to convert to numpy array
            
        Returns:
            Numpy array of embeddings (shape: [n_texts, embedding_dim])
        """
        # Convert single text to list
        if isinstance(texts, str):
            texts = [texts]
        
        if not texts:
            return np.array([])
        
        # Generate embeddings
        logger.debug(f"Generating embeddings for {len(texts)} texts")
        
        try:
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                show_progress_bar=show_progress_bar,
                normalize_embeddings=normalize_embeddings,
                convert_to_numpy=convert_to_numpy,
            )
            
            # Update statistics
            self.stats["total_embeddings"] += len(texts)
            self.stats["total_batches"] += 1
            self.stats["total_texts"] += len(texts)
            
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    def encode_queries(self, queries: Union[str, List[str]], **kwargs) -> np.ndarray:
        """
        Generate embeddings for queries (optimized for query encoding).
        
        Args:
            queries: Single query string or list of queries
            **kwargs: Additional arguments passed to encode()
            
        Returns:
            Numpy array of query embeddings
        """
        return self.encode(queries, **kwargs)
    
    def encode_documents(
        self,
        documents: Union[str, List[str]],
        **kwargs
    ) -> np.ndarray:
        """
        Generate embeddings for documents (optimized for document encoding).
        
        Args:
            documents: Single document string or list of documents
            **kwargs: Additional arguments passed to encode()
            
        Returns:
            Numpy array of document embeddings
        """
        return self.encode(documents, **kwargs)
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings produced by this model."""
        return self.embedding_dim
    
    def get_stats(self) -> Dict[str, Any]:
        """Get embedding generation statistics."""
        return self.stats.copy()
    
    def reset_stats(self) -> None:
        """Reset statistics counters."""
        self.stats = {
            "total_embeddings": 0,
            "total_batches": 0,
            "total_texts": 0,
        }
    
    def save_model(self, path: Union[str, Path]) -> None:
        """
        Save the model to disk.
        
        Args:
            path: Path to save the model
        """
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Saving model to {path}")
        self.model.save(str(path))
        logger.info("✅ Model saved successfully")
    
    @classmethod
    def load_model(cls, path: Union[str, Path], device: Optional[str] = None) -> "EmbeddingModel":
        """
        Load a saved model from disk.
        
        Args:
            path: Path to the saved model
            device: Device to load model on
            
        Returns:
            EmbeddingModel instance
        """
        path = Path(path)
        
        if not path.exists():
            raise FileNotFoundError(f"Model path not found: {path}")
        
        logger.info(f"Loading model from {path}")
        
        instance = cls.__new__(cls)
        instance.model = SentenceTransformer(str(path), device=device)
        instance.embedding_dim = instance.model.get_sentence_embedding_dimension()
        instance.device = device or "cpu"
        instance.model_name = str(path)
        instance.cache_folder = None
        instance.stats = {
            "total_embeddings": 0,
            "total_batches": 0,
            "total_texts": 0,
        }
        
        logger.info("✅ Model loaded successfully")
        return instance


def create_embedding_model(
    model_name: Optional[str] = None,
    device: Optional[str] = None,
) -> EmbeddingModel:
    """
    Factory function to create an EmbeddingModel instance.
    
    Args:
        model_name: Name of the embedding model
        device: Device to use
        
    Returns:
        EmbeddingModel instance
    """
    return EmbeddingModel(model_name=model_name, device=device)


# Default embedding model instance (lazy initialization)
_default_model: Optional[EmbeddingModel] = None


def get_default_embedding_model() -> EmbeddingModel:
    """Get or create the default embedding model instance."""
    global _default_model
    
    if _default_model is None:
        _default_model = create_embedding_model()
    
    return _default_model
