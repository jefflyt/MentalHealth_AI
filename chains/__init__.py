"""
LangChain Chains for Mental Health AI Agent
Modular chain implementations for RAG, conversation, routing, and crisis detection
"""

from .rag_chain import create_rag_chain
# from .conversation_chain import create_conversation_chain  # Disabled - requires deprecated langchain.chains
from .router_chain import create_router_chain
from .crisis_chain import create_crisis_detection_chain

__all__ = [
    'create_rag_chain',
    # 'create_conversation_chain',  # Disabled
    'create_router_chain',
    'create_crisis_detection_chain'
]
