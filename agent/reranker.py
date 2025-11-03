"""
Re-ranker module for improving RAG retrieval relevance.

This module provides cross-encoder based re-ranking to improve the relevance
of retrieved documents. It's designed to be modular and can be easily disabled
via configuration without affecting the core system.

Features:
- Cross-encoder re-ranking for better relevance
- Configurable enable/disable via environment variable
- Graceful fallback if model fails to load
- Batch processing for efficiency
- Threshold-based filtering

Author: Mental Health AI Team
Version: 1.0.0
"""

from typing import List, Dict, Any, Optional, Tuple
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Conditional import for sentence_transformers
try:
    from sentence_transformers import CrossEncoder
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    logger.warning("sentence_transformers not available - re-ranker will be disabled")
    CrossEncoder = None
    SENTENCE_TRANSFORMERS_AVAILABLE = False


class ReRanker:
    """
    Cross-encoder based re-ranker for improving retrieval relevance.
    
    This class wraps a cross-encoder model to re-rank retrieved documents
    based on their relevance to the query. It's designed to be optional
    and fail gracefully if disabled or if the model can't be loaded.
    """
    
    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-TinyBERT-L-2-v2",
        enabled: bool = True,
        relevance_threshold: float = 0.0,
        top_k: int = None
    ):
        """
        Initialize the re-ranker.
        
        Args:
            model_name: HuggingFace model name for cross-encoder
            enabled: Whether re-ranking is enabled
            relevance_threshold: Minimum relevance score (filters out low scores)
            top_k: Maximum number of documents to return after re-ranking
        """
        self.model_name = model_name
        self.enabled = enabled
        self.relevance_threshold = relevance_threshold
        self.top_k = top_k
        self.model = None
        
        # Try to load model if enabled
        if self.enabled:
            self._load_model()
    
    def _load_model(self) -> None:
        """Load the cross-encoder model."""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            logger.warning("sentence_transformers not available - re-ranking disabled")
            self.enabled = False
            return
            
        try:
            logger.info(f"Loading re-ranker model: {self.model_name}")
            self.model = CrossEncoder(self.model_name)
            logger.info("Re-ranker model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load re-ranker model: {e}")
            logger.warning("Re-ranking will be disabled - falling back to original retrieval")
            self.enabled = False
            self.model = None
    
    def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        document_key: str = "text"
    ) -> List[Dict[str, Any]]:
        """
        Re-rank documents based on relevance to query.
        
        Args:
            query: The search query
            documents: List of document dictionaries
            document_key: Key in document dict containing the text
        
        Returns:
            Re-ranked list of documents (or original if disabled)
        """
        # If disabled or no model, return original documents
        if not self.enabled or self.model is None:
            logger.debug("Re-ranking disabled, returning original documents")
            return documents
        
        # If no documents, return empty list
        if not documents:
            return documents
        
        try:
            # Extract document texts
            doc_texts = [doc.get(document_key, "") for doc in documents]
            
            # Create query-document pairs
            pairs = [[query, doc_text] for doc_text in doc_texts]
            
            # Get relevance scores
            scores = self.model.predict(pairs)
            
            # Combine documents with scores
            scored_docs = [
                {**doc, "rerank_score": float(score)}
                for doc, score in zip(documents, scores)
            ]
            
            # Filter by threshold
            if self.relevance_threshold > 0:
                scored_docs = [
                    doc for doc in scored_docs
                    if doc["rerank_score"] >= self.relevance_threshold
                ]
            
            # Sort by score (descending)
            scored_docs.sort(key=lambda x: x["rerank_score"], reverse=True)
            
            # Apply top_k limit
            if self.top_k is not None and self.top_k > 0:
                scored_docs = scored_docs[:self.top_k]
            
            logger.info(
                f"Re-ranked {len(documents)} documents → {len(scored_docs)} "
                f"(threshold: {self.relevance_threshold})"
            )
            
            return scored_docs
            
        except Exception as e:
            logger.error(f"Re-ranking failed: {e}")
            logger.warning("Falling back to original document order")
            return documents
    
    def is_enabled(self) -> bool:
        """Check if re-ranking is enabled and model is loaded."""
        return self.enabled and self.model is not None
    
    def get_config(self) -> Dict[str, Any]:
        """Get current re-ranker configuration."""
        return {
            "enabled": self.enabled,
            "model_loaded": self.model is not None,
            "model_name": self.model_name,
            "relevance_threshold": self.relevance_threshold,
            "top_k": self.top_k
        }


# Global re-ranker instance (lazy initialization)
_reranker_instance: Optional[ReRanker] = None


def get_reranker(
    enabled: Optional[bool] = None,
    relevance_threshold: Optional[float] = None,
    top_k: Optional[int] = None
) -> ReRanker:
    """
    Get or create the global re-ranker instance.
    
    This function implements lazy initialization and configuration via
    environment variables. The re-ranker can be easily disabled by setting
    RERANKER_ENABLED=false in the environment.
    
    Args:
        enabled: Override environment variable for enabled status
        relevance_threshold: Override environment variable for threshold
        top_k: Override environment variable for top_k
    
    Returns:
        ReRanker instance (may be disabled)
    """
    global _reranker_instance
    
    if _reranker_instance is None:
        # Get configuration from environment with defaults
        env_enabled = os.getenv("RERANKER_ENABLED", "true").lower() == "true"
        env_threshold = float(os.getenv("RERANKER_THRESHOLD", "0.0"))
        env_top_k_str = os.getenv("RERANKER_TOP_K", "")
        env_top_k = int(env_top_k_str) if env_top_k_str else None
        env_model = os.getenv("RERANKER_MODEL", "cross-encoder/ms-marco-TinyBERT-L-2-v2")
        
        # Apply overrides
        final_enabled = enabled if enabled is not None else env_enabled
        final_threshold = relevance_threshold if relevance_threshold is not None else env_threshold
        final_top_k = top_k if top_k is not None else env_top_k
        
        # Create instance
        _reranker_instance = ReRanker(
            model_name=env_model,
            enabled=final_enabled,
            relevance_threshold=final_threshold,
            top_k=final_top_k
        )
    
    return _reranker_instance


def reset_reranker() -> None:
    """Reset the global re-ranker instance (useful for testing)."""
    global _reranker_instance
    _reranker_instance = None


# Convenience function for easy integration
def rerank_documents(
    query: str,
    documents: List[Dict[str, Any]],
    document_key: str = "text",
    enabled: bool = True
) -> List[Dict[str, Any]]:
    """
    Re-rank documents using the global re-ranker instance.
    
    This is a convenience function that makes it easy to integrate
    re-ranking into existing code with minimal changes.
    
    Args:
        query: The search query
        documents: List of document dictionaries
        document_key: Key in document dict containing the text
        enabled: Whether to use re-ranking (can disable locally)
    
    Returns:
        Re-ranked list of documents
    """
    if not enabled:
        return documents
    
    reranker = get_reranker()
    return reranker.rerank(query, documents, document_key)
