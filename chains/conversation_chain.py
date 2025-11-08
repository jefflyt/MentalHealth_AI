"""
Conversation Chain - Memory-enhanced conversational chain
Maintains conversation context and generates contextual responses

DEPRECATED: This module uses deprecated langchain.chains.ConversationChain
and langchain.memory.ConversationBufferMemory which were removed in LangChain 1.0+.
Currently disabled in chains/__init__.py - not used by the application.
"""

# DEPRECATED IMPORTS - Do not use
# from langchain.chains import ConversationChain
# from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate


def create_conversation_chain(llm, memory=None, persona_name="Sunny"):
    """
    DEPRECATED: Create a conversation chain with memory.
    
    This function is deprecated and disabled. The application uses
    custom ConversationBufferMemory implementation in app.py instead.
    
    Args:
        llm: LangChain LLM instance
        memory: Optional ConversationBufferMemory instance
        persona_name: Name of the AI persona
        
    Returns:
        ConversationChain instance
"""
    raise NotImplementedError(
        "ConversationChain is deprecated in LangChain 1.0+. "
        "Use custom memory implementation in app.py instead."
    )
    
    # Create memory if not provided
    if memory is None:
        memory = ConversationBufferMemory(
            memory_key="history",
            return_messages=False
        )
    
    # Conversation prompt with Sunny persona
    conversation_prompt = PromptTemplate(
        input_variables=["history", "input"],
        template="""You are {persona_name}, a warm and empathetic mental health support companion.

You provide evidence-based mental health support with a gentle, encouraging tone. You're knowledgeable about mental health conditions, coping strategies, and resources in Singapore.

Key Guidelines:
- Be warm, supportive, and non-judgmental
- Validate emotions and experiences
- Provide practical, actionable guidance
- Recognize crisis situations and escalate when needed
- Use simple, accessible language
- Offer hope while being realistic

Conversation History:
{history}

Current Message: {input}

{persona_name}:"""
    )
    
    # Bind persona name
    prompt_with_persona = conversation_prompt.partial(persona_name=persona_name)
    
    # Create conversation chain
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt_with_persona,
        verbose=False
    )
    
    return conversation


def create_rag_conversation_chain(llm, retriever, memory=None):
    """
    Create a conversation chain that combines RAG with conversational memory.
    
    Args:
        llm: LangChain LLM instance
        retriever: LangChain retriever instance
        memory: Optional ConversationBufferMemory instance
        
    Returns:
        Conversation chain with RAG integration
    """
    
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnablePassthrough, RunnableParallel
    from langchain_core.output_parsers import StrOutputParser
    from .rag_chain import format_docs
    
    # DEPRECATED: This function uses removed ConversationBufferMemory
    raise NotImplementedError(
        "create_rag_conversation_chain is deprecated. "
        "ConversationBufferMemory was removed in LangChain 1.0+. "
        "Use custom memory implementation in app.py instead."
    )
    
    # Create memory if not provided
    # if memory is None:
    #     memory = ConversationBufferMemory(
    #         memory_key="chat_history",
    #         return_messages=True,
    #         output_key="answer"
    #     )
    
    # RAG + Conversation prompt
    rag_conversation_prompt = ChatPromptTemplate.from_template("""You are Sunny, a compassionate mental health support companion.

Retrieved Context:
{context}

Conversation History:
{chat_history}

Current Question: {question}

Provide a supportive response that:
1. Considers the conversation history
2. Uses retrieved context when relevant
3. Maintains warmth and empathy
4. Offers practical guidance

Sunny:""")
    
    # Create chain components
    def get_history(inputs):
        """Get conversation history from memory."""
        return memory.load_memory_variables({}).get("chat_history", "")
    
    # Build RAG + Conversation chain
    chain = (
        RunnableParallel(
            {
                "context": lambda x: retriever.invoke(x["question"]) | format_docs,
                "question": lambda x: x["question"],
                "chat_history": get_history
            }
        )
        | rag_conversation_prompt
        | llm
        | StrOutputParser()
    )
    
    # Wrap with memory saving
    def chain_with_memory(inputs):
        """Execute chain and save to memory."""
        question = inputs["question"]
        answer = chain.invoke(inputs)
        
        # Save to memory
        memory.save_context(
            {"input": question},
            {"answer": answer}
        )
        
        return answer
    
    return chain_with_memory
