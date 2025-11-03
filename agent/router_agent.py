"""
Router Agent - Intelligent query routing with RAG context
"""

from typing import TypedDict, List
from langchain_groq import ChatGroq


# Define distress keyword dictionaries - SIMPLIFIED 2-LEVEL SYSTEM
# High distress keywords (weight: 5) - severe emotional crisis, immediate empathy needed
HIGH_DISTRESS_KEYWORDS = {
    # Crisis-level emotional states
    "don't feel good": 5, "dont feel good": 5, "not feel good": 5,
    "feel terrible": 5, "feel awful": 5, "feel horrible": 5,
    "can't take it": 5, "cant take it": 5, "can't take this": 5,
    "breaking down": 5, "falling apart": 5, "falling to pieces": 5,
    "overwhelmed": 5, "can't cope": 5, "cant cope": 5,
    "losing it": 5, "giving up": 5, "lost control": 5,
    "can't breathe": 5, "cant breathe": 5, "suffocating": 5,
    "drowning": 5, "sinking": 5, "spiraling": 5,
    "can't handle": 5, "cant handle": 5, "too much": 5,
    "breaking": 5, "broken": 5, "shattered": 5,
    "devastated": 5, "destroyed": 5, "crushed": 5,
    "unbearable": 5, "agonizing": 5, "tormented": 5,
    "desperate": 5, "hopeless": 5, "no hope": 5,
    "worthless": 5, "useless": 5, "failure": 5,
    "empty inside": 5, "hollow": 5, "void": 5,
    "paralyzed": 5, "frozen": 5, "trapped": 5,
    "ruined": 5, "over": 5, "done": 5,
    # Severe emotional expressions  
    "hate myself": 5, "hate my life": 5, "want to disappear": 5,
    "nothing matters": 5, "why bother": 5, "what's the point": 5,
}

# Mild distress keywords (weight: 1) - general support needed, friendly approach
MILD_DISTRESS_KEYWORDS = {
    # General emotional states
    "feel bad": 1, "feeling down": 1, "feeling low": 1,
    "feeling sad": 1, "feeling anxious": 1, "feeling depressed": 1,
    "feeling stressed": 1, "stressed out": 1, "burnt out": 1,
    "not okay": 1, "not ok": 1, "not well": 1, "unwell": 1,
    "struggling": 1, "hard time": 1, "difficult time": 1,
    "tough time": 1, "rough time": 1, "bad day": 1,
    "exhausted": 1, "drained": 1, "tired": 1, "worn out": 1,
    "worried": 1, "scared": 1, "afraid": 1, "fearful": 1,
    "lonely": 1, "alone": 1, "isolated": 1, "disconnected": 1,
    "helpless": 1, "powerless": 1, "stuck": 1,
    "empty": 1, "numb": 1, "detached": 1,
    "down in the dumps": 1, "feeling blue": 1, "melancholy": 1,
    "anxious mess": 1, "emotional wreck": 1, "emotional": 1,
    "can't focus": 1, "cant focus": 1, "distracted": 1,
    "irritable": 1, "restless": 1, "tense": 1, "uneasy": 1,
    "overthinking": 1, "ruminating": 1, "obsessing": 1,
    "self-doubting": 1, "doubting myself": 1, "insecure": 1,
    "frustrated": 1, "angry": 1, "upset": 1,
    "sad": 1, "depressed": 1, "anxious": 1,  # Common standalone emotions
    "stressed": 1, "worried": 1, "down": 1,
    "unhappy": 1, "hurt": 1, "bothered": 1,
    # Help-seeking expressions
    "need help": 1, "i need help": 1, "confused": 1,
    "not sure": 1, "don't know": 1, "dont know": 1,
    "need someone": 1, "need to talk": 1, "someone to talk to": 1,
}




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
    Detect level of distress in user query using weighted scoring.
    Returns: 'high', 'mild', or 'none'
    
    SIMPLIFIED 2-LEVEL SYSTEM:
    - HIGH keywords: 5 points (severe crisis, immediate empathy needed)
    - MILD keywords: 1 point (general support, friendly approach)
    
    Thresholds:
    - 5+: HIGH distress (any high keyword OR 5+ mild keywords with modifiers)
    - 1-4: MILD distress (1-4 mild keywords)
    - 0: NONE
    """
    query_lower = query.lower()
    
    # Calculate weighted score
    score = 0
    
    # Check high distress patterns
    for phrase, weight in HIGH_DISTRESS_KEYWORDS.items():
        if phrase in query_lower:
            score += weight
    
    # Check mild distress patterns
    for phrase, weight in MILD_DISTRESS_KEYWORDS.items():
        if phrase in query_lower:
            score += weight
    
    # Apply intensity modifiers
    score = apply_intensity_modifiers(query, score)
    
    # Determine distress level - SIMPLIFIED 2-LEVEL SYSTEM
    if score >= 5:
        return 'high'
    elif score >= 1:
        return 'mild'
    else:
        return 'none'


def apply_intensity_modifiers(query: str, base_score: float) -> float:
    """
    Apply intensity modifiers based on adverbs and punctuation.
    
    Modifiers:
    - Intensity adverbs (very, really, so, extremely): 1.5x multiplier
    - Multiple exclamation marks (3+): +2 points per extra mark
    - ALL CAPS words (2+): +3 points
    """
    query_lower = query.lower()
    modified_score = base_score
    
    # Adverb multipliers
    intensity_adverbs = ["very", "really", "so", "extremely", "incredibly", "totally", 
                         "completely", "absolutely", "utterly", "quite"]
    
    if any(adverb in query_lower for adverb in intensity_adverbs):
        modified_score *= 1.5
    
    # Punctuation modifiers - exclamation marks (more sensitive)
    exclamation_count = query.count('!')
    if exclamation_count >= 1:
        modified_score += 2 * exclamation_count  # Any exclamation adds intensity
    
    # ALL CAPS modifier (indicates shouting/intensity) - more sensitive
    words = query.split()
    caps_words = [w for w in words if w.isupper() and len(w) >= 2]  # Reduced from >2 to >=2
    if len(caps_words) >= 1:  # Even one caps word adds intensity
        modified_score += 3 * len(caps_words)
    
    return modified_score


def router_node(state: AgentState, llm: ChatGroq, get_relevant_context) -> AgentState:
    """Enhanced router with RAG context."""
    query = state["current_query"]
    
    print("\n" + "="*60)
    print("🧭 [ROUTER AGENT ACTIVATED]")
    print(f"📝 Query: {query}")
    print("="*60)
    
    # Get initial context for routing decisions, but preserve any existing context (like assessment suggestions)
    existing_context = state.get("context", "")
    routing_context = get_relevant_context(f"route classify {query}", n_results=2)
    
    # If we have existing context (e.g., assessment suggestions), keep it and add routing context
    if existing_context:
        state["context"] = existing_context + "\n\n" + routing_context
        print("🎯 Preserving existing context and adding routing context")
    else:
        state["context"] = routing_context
    
    # Priority 1: Crisis detection (highest priority)
    if detect_crisis(query):
        state["crisis_detected"] = True
        state["current_agent"] = "crisis_intervention"
        state["messages"].append("🚨 I'm here with you right now - getting you immediate support")
        print("🚨 PRIORITY 1: Crisis detected → Crisis Agent")
        return state
    
    # Priority 2: Distress detection with different levels
    distress_level = detect_distress_level(query)
    
    if distress_level != 'none':
        state["current_agent"] = "information"
        state["distress_level"] = distress_level  # Pass distress level to information agent
        
        # Calculate score for debugging
        query_lower = query.lower()
        score = 0
        for phrase, weight in {**HIGH_DISTRESS_KEYWORDS, **MILD_DISTRESS_KEYWORDS}.items():
            if phrase in query_lower:
                score += weight
        score = apply_intensity_modifiers(query, score)
        
        print(f"😔 PRIORITY 2: {distress_level.upper()} distress detected (score: {score:.1f}) → Information Agent")
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
