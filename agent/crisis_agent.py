"""
Crisis Intervention Agent - Immediate support with emergency protocols
"""

from typing import TypedDict, List
from langchain_groq import ChatGroq


class AgentState(TypedDict):
    current_query: str
    messages: List[str]
    current_agent: str
    crisis_detected: bool
    context: str


def crisis_intervention_node(state: AgentState, llm: ChatGroq, get_relevant_context) -> AgentState:
    """RAG-enhanced crisis intervention with relevant protocols."""
    query = state["current_query"]
    
    # Get crisis intervention context
    crisis_context = get_relevant_context(f"crisis intervention emergency protocols {query}", n_results=3)
    
    crisis_prompt = f"""
    CRISIS INTERVENTION MODE - Provide immediate support based on this context:
    
    Context: {crisis_context}
    
    User Query: "{query}"
    
    Provide:
    1. Immediate reassurance and validation
    2. Safety planning and coping strategies
    3. Emergency contacts specific to Singapore
    4. Encouragement to seek immediate professional help
    
    Be empathetic, direct, and actionable.
    """
    
    try:
        response = llm.invoke(crisis_prompt).content
    except Exception as e:
        # Fallback crisis response
        response = """
        🆘 I'm here to help you right now. You're not alone in this.
        
        IMMEDIATE SUPPORT:
        • SOS Hotline: 1767 (24/7, free)
        • IMH Emergency: 6389-2222
        • CHAT Youth Support: 6493-6500
        
        Please reach out to one of these services immediately. Your life matters.
        """
    
    state["messages"].append(response)
    state["current_agent"] = "complete"
    return state
