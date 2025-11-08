"""
RAG Chain - Retrieval-Augmented Generation Chain
Combines retriever with LLM to provide context-grounded responses
"""

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


def format_docs(docs):
    """Format retrieved documents for context."""
    if not docs:
        return "No relevant information found."
    
    context_pieces = []
    for doc in docs:
        source = doc.metadata.get('source', 'Knowledge Base')
        context_pieces.append(f"[Source: {source}]\n{doc.page_content}")
    
    return "\n\n---\n\n".join(context_pieces)


def create_rag_chain(retriever, llm):
    """
    Create a RAG chain that retrieves context and generates responses.
    
    Args:
        retriever: LangChain retriever instance
        llm: LangChain LLM instance
        
    Returns:
        Runnable RAG chain
    """
    
    # RAG prompt template
    rag_prompt = ChatPromptTemplate.from_template("""You are a compassionate mental health support assistant.

Use the following context from the knowledge base to inform your response:

{context}

User Question: {question}

Provide a supportive, evidence-based response. If the context doesn't contain relevant information, acknowledge this and provide general supportive guidance.

Response:""")
    
    # Create RAG chain: retrieve → format → prompt → LLM → parse
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | rag_prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain


def create_rag_chain_with_sources(retriever, llm):
    """
    Create a RAG chain that returns both answer and source documents.
    
    Args:
        retriever: LangChain retriever instance
        llm: LangChain LLM instance
        
    Returns:
        Runnable RAG chain with sources
    """
    
    from langchain_core.runnables import RunnableParallel
    
    # RAG prompt template
    rag_prompt = ChatPromptTemplate.from_template("""You are a compassionate mental health support assistant.

Use the following context from the knowledge base to inform your response:

{context}

User Question: {question}

Provide a supportive, evidence-based response.

Response:""")
    
    # Chain with sources
    rag_chain_with_sources = RunnableParallel(
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
    ).assign(
        answer=rag_prompt | llm | StrOutputParser()
    ).assign(
        sources=lambda x: retriever.invoke(x["question"])
    )
    
    return rag_chain_with_sources
