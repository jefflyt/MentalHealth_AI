"""
Router Agent - Intelligent query routing with RAG context
"""

from typing import TypedDict, List
from langchain_groq import ChatGroq


class AgentState(TypedDict):
    current_query: str
    messages: List[str]
    current_agent: str
    crisis_detected: bool
    context: str


def detect_crisis(query: str) -> bool:
    """Detect crisis keywords in user query."""
    crisis_keywords = [
        "suicide", "suicidal", "kill myself", "end my life", "want to die",
        "self harm", "hurt myself", "cutting", "overdose", "no reason to live",
        "better off dead", "can't go on", "end it all"
    ]
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in crisis_keywords)


def router_node(state: AgentState, llm: ChatGroq, get_relevant_context) -> AgentState:
    """Enhanced router with RAG context."""
    query = state["current_query"]
    
    # Get initial context for routing decisions
    routing_context = get_relevant_context(f"route classify {query}", n_results=2)
    state["context"] = routing_context
    
    # Crisis detection (highest priority)
    if detect_crisis(query):
        state["crisis_detected"] = True
        state["current_agent"] = "crisis_intervention"
        state["messages"].append("🚨 Crisis situation detected - routing to immediate support")
        return state
    
    # Use LLM with context for intelligent routing
    routing_prompt = f"""
    Based on the following context and user query, determine the most appropriate agent:
    
    Context: {routing_context}
    
    User Query: "{query}"
    
    Available Agents:
    - information: General mental health information and education
    - resource: Singapore mental health services and resources 
    - assessment: DASS-21 mental health screening
    - human_escalation: Complex cases requiring human support
    
    Respond with only the agent name that best matches the query.
    """
    
    try:
        routing_response = llm.invoke(routing_prompt).content.strip().lower()
        
        # Validate and set agent
        valid_agents = ["information", "resource", "assessment", "human_escalation"]
        if routing_response in valid_agents:
            state["current_agent"] = routing_response
        else:
            # Default to information agent if unclear
            state["current_agent"] = "information"
        
        # Don't add routing message - let the agent respond directly
        
    except Exception as e:
        print(f"Routing error: {e}")
        state["current_agent"] = "information"  # Safe default
    
    return state
