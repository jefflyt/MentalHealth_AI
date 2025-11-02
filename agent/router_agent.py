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
    distress_level: str  # 'high', 'moderate', 'mild', or 'none'


def detect_crisis(query: str) -> bool:
    """Detect crisis keywords in user query."""
    crisis_keywords = [
        "suicide", "suicidal", "kill myself", "end my life", "want to die",
        "self harm", "hurt myself", "cutting", "overdose", "no reason to live",
        "better off dead", "can't go on", "end it all"
    ]
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in crisis_keywords)


def detect_distress_level(query: str) -> str:
    """
    Detect level of distress in user query.
    Returns: 'high', 'moderate', 'mild', or 'none'
    """
    query_lower = query.lower()
    
    # High distress - clear emotional/physical suffering
    high_distress = [
        "don't feel good", "dont feel good", "not feel good", "feel terrible", "feel awful",
        "feel horrible", "can't take it", "cant take it", "breaking down", "falling apart",
        "overwhelmed", "can't cope", "cant cope", "losing it", "giving up"
    ]
    
    # Moderate distress - clear negative feelings/emotions
    moderate_distress = [
        "feel bad", "feeling down", "feeling sad", "feeling anxious", "feeling depressed",
        "feeling stressed", "not okay", "not ok", "not well", "struggling", "hard time",
        "difficult time", "tough time", "exhausted", "drained", "worried", "scared",
        "afraid", "lonely", "alone", "hopeless", "helpless", "worthless", "empty", "numb"
    ]
    
    # Mild distress - vague help-seeking or general concerns
    mild_distress = [
        "need help", "help me", "need someone", "need to talk",
        "something wrong", "what's wrong with me", "whats wrong with me",
        "confused", "unsure", "don't know", "dont know"
    ]
    
    # Check levels in order of severity
    if any(pattern in query_lower for pattern in high_distress):
        return 'high'
    elif any(pattern in query_lower for pattern in moderate_distress):
        return 'moderate'
    elif any(pattern in query_lower for pattern in mild_distress):
        return 'mild'
    else:
        return 'none'


def router_node(state: AgentState, llm: ChatGroq, get_relevant_context) -> AgentState:
    """Enhanced router with RAG context."""
    query = state["current_query"]
    
    print("\n" + "="*60)
    print("🧭 [ROUTER AGENT ACTIVATED]")
    print(f"📝 Query: {query}")
    print("="*60)
    
    # Get initial context for routing decisions
    routing_context = get_relevant_context(f"route classify {query}", n_results=2)
    state["context"] = routing_context
    
    # Priority 1: Crisis detection (highest priority)
    if detect_crisis(query):
        state["crisis_detected"] = True
        state["current_agent"] = "crisis_intervention"
        state["messages"].append("🚨 Crisis situation detected - routing to immediate support")
        print("🚨 PRIORITY 1: Crisis detected → Crisis Agent")
        return state
    
    # Priority 2: Distress detection with different levels
    distress_level = detect_distress_level(query)
    
    if distress_level != 'none':
        state["current_agent"] = "information"
        state["distress_level"] = distress_level  # Pass distress level to information agent
        print(f"😔 PRIORITY 2: {distress_level.upper()} distress detected → Information Agent")
        return state
    
    # Priority 3: Specific requests - use LLM routing
    print("🎯 PRIORITY 3: Using LLM routing...")
    routing_prompt = f"""
    Based on the following context and user query, determine the most appropriate agent:
    
    Context: {routing_context}
    
    User Query: "{query}"
    
    Available Agents:
    - information: General mental health information and education
    - resource: Singapore mental health services and resources (only if specifically asking about services/resources)
    - assessment: DASS-21 mental health screening (only if asking about testing/assessment)
    - human_escalation: Complex cases requiring human support
    
    Respond with only the agent name that best matches the query.
    """
    
    try:
        routing_response = llm.invoke(routing_prompt).content.strip().lower()
        
        # Validate and set agent
        valid_agents = ["information", "resource", "assessment", "human_escalation"]
        if routing_response in valid_agents:
            state["current_agent"] = routing_response
            print(f"✅ LLM routed to: {routing_response.upper()} Agent")
        else:
            # Default to information agent if unclear
            state["current_agent"] = "information"
            print(f"⚠️  Invalid routing ({routing_response}), defaulting to: INFORMATION Agent")
        
        # Don't add routing message - let the agent respond directly
        
    except Exception as e:
        print(f"❌ Routing error: {e}")
        print("⚠️  Defaulting to: INFORMATION Agent")
        state["current_agent"] = "information"  # Safe default
    
    return state
