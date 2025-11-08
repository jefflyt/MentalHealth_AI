"""
Agent Helpers - Integration utilities for Chains, Memory, and Tools
Provides helper functions to integrate LangChain components with agent nodes

DEPRECATED: This module uses deprecated langchain.memory.ConversationBufferMemory
which was removed in LangChain 1.0+. Currently not used by the application.
The application uses custom ConversationBufferMemory implementation in app.py instead.
"""

from typing import Dict, List, Any, Optional
# DEPRECATED IMPORT - Do not use
# from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage


def get_conversation_context(memory: Any) -> str:
    """
    DEPRECATED: Extract formatted conversation context from memory.
    
    Args:
        memory: ConversationBufferMemory instance
        
    Returns:
        Formatted conversation history string
    """
    if not memory:
        return ""
    
    history = memory.load_memory_variables({})
    messages = history.get("chat_history", [])
    
    if not messages:
        return ""
    
    formatted = []
    for msg in messages[-10:]:  # Last 10 messages for context
        if isinstance(msg, (HumanMessage, dict)):
            role = "User"
            content = msg.content if hasattr(msg, 'content') else msg.get('content', '')
        else:
            role = "AI"
            content = msg.content if hasattr(msg, 'content') else msg.get('content', '')
        formatted.append(f"{role}: {content}")
    
    return "\n".join(formatted)


def save_to_memory(
    memory: Any,
    user_message: str,
    ai_response: str
):
    """
    DEPRECATED: Save interaction to conversation memory.
    
    Args:
        memory: ConversationBufferMemory instance (deprecated)
        user_message: User's input
        ai_response: AI's response
    """
    if memory:
        memory.save_context(
            {"input": user_message},
            {"output": ai_response}
        )


def create_rag_enhanced_prompt(
    query: str,
    context: str,
    conversation_history: str = "",
    persona_guidelines: str = "",
    distress_level: str = "none"
) -> str:
    """
    Create a comprehensive RAG-enhanced prompt with all context.
    
    Args:
        query: User's current query
        context: Retrieved context from RAG
        conversation_history: Previous conversation context
        persona_guidelines: Agent persona guidelines (e.g., Sunny's personality)
        distress_level: User's distress level
        
    Returns:
        Formatted prompt string
    """
    prompt = ""
    
    if persona_guidelines:
        prompt += f"{persona_guidelines}\n\n"
    
    if distress_level != "none":
        prompt += f"⚠️ User Distress Level: {distress_level.upper()}\n"
        if distress_level == "high":
            prompt += "PRIORITY: Provide immediate empathetic support and crisis resources.\n"
        prompt += "\n"
    
    if context:
        prompt += f"Retrieved Knowledge Base Context:\n{context}\n\n"
    
    if conversation_history:
        prompt += f"Conversation History:\n{conversation_history}\n\n"
    
    prompt += f"Current User Query: {query}\n\n"
    prompt += "Provide a supportive, context-aware response:"
    
    return prompt


def should_use_tool(query: str, agent_type: str) -> Optional[Dict[str, str]]:
    """
    Determine if a tool should be invoked based on query and agent type.
    
    Args:
        query: User's query
        agent_type: Type of agent (crisis, information, resource, assessment)
        
    Returns:
        Dictionary with tool info if tool should be used, None otherwise
    """
    query_lower = query.lower()
    
    # Crisis agent tool triggers
    if agent_type == "crisis":
        if any(word in query_lower for word in ['hotline', 'emergency', 'help now', 'crisis']):
            return {
                "tool": "crisis_hotline",
                "urgency": "immediate" if 'now' in query_lower or 'emergency' in query_lower else "high"
            }
    
    # Resource agent tool triggers
    elif agent_type == "resource":
        if any(word in query_lower for word in ['find', 'service', 'therapist', 'counselor', 'support group']):
            # Determine resource type
            if 'hotline' in query_lower or 'emergency' in query_lower:
                resource_type = 'hotline'
            elif 'therapy' in query_lower or 'therapist' in query_lower or 'counselor' in query_lower:
                resource_type = 'therapy'
            elif 'support group' in query_lower or 'group' in query_lower:
                resource_type = 'support_group'
            elif 'youth' in query_lower or 'young' in query_lower:
                resource_type = 'youth'
            else:
                resource_type = 'general'
            
            return {
                "tool": "resource_finder",
                "resource_type": resource_type
            }
    
    # Assessment agent tool triggers
    elif agent_type == "assessment":
        if any(word in query_lower for word in ['assess', 'screen', 'test', 'check', 'evaluate']):
            # Determine assessment type
            if 'depress' in query_lower:
                assessment_type = 'depression'
            elif 'anxi' in query_lower or 'worry' in query_lower:
                assessment_type = 'anxiety'
            elif 'stress' in query_lower:
                assessment_type = 'stress'
            else:
                assessment_type = 'general'
            
            return {
                "tool": "assessment",
                "assessment_type": assessment_type
            }
    
    # General tool triggers (any agent)
    if any(word in query_lower for word in ['breath', 'breathing', 'relax', 'calm down']):
        # Determine breathing type
        if 'box' in query_lower:
            breath_type = 'box'
        elif '478' in query_lower or '4-7-8' in query_lower:
            breath_type = '478'
        elif 'deep' in query_lower:
            breath_type = 'deep'
        else:
            breath_type = 'calming'
        
        return {
            "tool": "breathing",
            "exercise_type": breath_type
        }
    
    if any(word in query_lower for word in ['mood', 'feeling', 'how am i', 'track']):
        if 'track' in query_lower or 'log' in query_lower:
            return {
                "tool": "mood_tracker",
                "action": "log"
            }
        elif 'pattern' in query_lower or 'analyze' in query_lower:
            return {
                "tool": "mood_tracker",
                "action": "analyze"
            }
    
    return None


def format_tool_response(tool_result: str, agent_personality: str = "") -> str:
    """
    Format tool output with agent personality.
    
    Args:
        tool_result: Raw tool output
        agent_personality: Agent's personality/voice
        
    Returns:
        Formatted response
    """
    if agent_personality:
        return f"{agent_personality}\n\n{tool_result}"
    return tool_result


def merge_contexts(rag_context: str, external_context: str) -> str:
    """
    Merge RAG context with external context (e.g., assessment results).
    
    Args:
        rag_context: Context from RAG retrieval
        external_context: External context (assessments, etc.)
        
    Returns:
        Merged context string
    """
    contexts = []
    
    if rag_context:
        contexts.append(f"Knowledge Base Context:\n{rag_context}")
    
    if external_context:
        contexts.append(f"Session Context:\n{external_context}")
    
    return "\n\n---\n\n".join(contexts)


def extract_intent(query: str, llm) -> Dict[str, Any]:
    """
    Extract user intent using LLM.
    
    Args:
        query: User's query
        llm: LLM instance
        
    Returns:
        Dictionary with intent information
    """
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    
    intent_prompt = ChatPromptTemplate.from_template("""Analyze this mental health query and extract key intent.

User Query: {query}

Identify:
1. Primary intent (information/resource/assessment/crisis/conversation)
2. Specific topic or need
3. Urgency level (low/moderate/high)

Output as: intent|topic|urgency

Example: resource|find therapist|moderate

Analysis:""")
    
    chain = intent_prompt | llm | StrOutputParser()
    result = chain.invoke({"query": query})
    
    parts = result.strip().split('|')
    
    return {
        "intent": parts[0] if len(parts) > 0 else "conversation",
        "topic": parts[1] if len(parts) > 1 else "",
        "urgency": parts[2] if len(parts) > 2 else "low"
    }
