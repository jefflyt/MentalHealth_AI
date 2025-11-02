"""
Router Agent - Intelligent query routing with RAG context
"""

from typing import TypedDict, List
from langchain_groq import ChatGroq


# Define distress keyword dictionaries as module-level constants
# High distress keywords (weight: 5) - severe emotional/physical suffering
HIGH_DISTRESS_KEYWORDS = {
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
    "isolated": 5, "abandoned": 5, "rejected": 5,
    "ruined": 5, "over": 5, "done": 5,
}

# Moderate distress keywords (weight: 3) - clear negative feelings
MODERATE_DISTRESS_KEYWORDS = {
    "feel bad": 3, "feeling down": 3, "feeling low": 3,
    "feeling sad": 3, "feeling anxious": 3, "feeling depressed": 3,
    "feeling stressed": 3, "stressed out": 3, "burnt out": 3,
    "not okay": 3, "not ok": 3, "not well": 3, "unwell": 3,
    "struggling": 3, "hard time": 3, "difficult time": 3,
    "tough time": 3, "rough time": 3, "bad day": 3,
    "exhausted": 3, "drained": 3, "tired": 3, "worn out": 3,
    "worried": 3, "scared": 3, "afraid": 3, "fearful": 3,
    "lonely": 3, "alone": 3, "isolated": 3, "disconnected": 3,
    "helpless": 3, "powerless": 3, "stuck": 3,
    "empty": 3, "numb": 3, "detached": 3,
    "down in the dumps": 3, "feeling blue": 3, "melancholy": 3,
    "anxious mess": 3, "emotional wreck": 3, "emotional": 3,
    "can't focus": 3, "cant focus": 3, "distracted": 3,
    "irritable": 3, "restless": 3, "tense": 3, "uneasy": 3,
    "overthinking": 3, "ruminating": 3, "obsessing": 3,
    "self-doubting": 3, "doubting myself": 3, "insecure": 3,
    "frustrated": 3, "angry": 3, "upset": 3,
    "tearful": 3, "crying": 3, "tears": 3,
    "burned out": 3, "overloaded": 3, "burdened": 3,
    "conflicted": 3, "torn": 3, "confused": 3,
    "sad": 3, "depressed": 3, "anxious": 3,  # Common standalone emotions
}

# Mild distress keywords (weight: 1) - vague help-seeking
MILD_DISTRESS_KEYWORDS = {
    "need help": 1, "help me": 1, "need support": 1,
    "need someone": 1, "need to talk": 1, "want to talk": 1,
    "someone to talk to": 1, "talk to someone": 1,
    "something wrong": 1, "what's wrong with me": 1, "whats wrong with me": 1,
    "confused": 1, "unsure": 1, "uncertain": 1,
    "don't know": 1, "dont know": 1, "not sure": 1,
    "a bit off": 1, "feeling off": 1, "not myself": 1,
    "need a chat": 1, "need advice": 1, "need guidance": 1,
    "curious": 1, "wondering": 1, "questioning": 1,
    "mixed emotions": 1, "mixed feelings": 1, "complicated": 1,
    "seeking advice": 1, "looking for help": 1, "seeking help": 1,
    "hesitant": 1, "uncertain": 1, "indecisive": 1,
    "pensive": 1, "reflective": 1, "thoughtful": 1,
    "lost": 1, "adrift": 1, "directionless": 1,
    "blah": 1, "meh": 1, "whatever": 1,
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
    Returns: 'high', 'moderate', 'mild', or 'none'
    
    Scoring system:
    - HIGH keywords: 5 points
    - MODERATE keywords: 3 points  
    - MILD keywords: 1 point
    
    Thresholds (adjusted for single-phrase detection):
    - 10+: HIGH distress (2+ high keywords OR 1 high + modifier)
    - 5-9: MODERATE distress (1 high keyword OR 2-3 moderate keywords)
    - 1-4: MILD distress (1-2 moderate keywords OR 1-4 mild keywords)
    - 0: NONE
    """
    query_lower = query.lower()
    
    # Calculate weighted score
    score = 0
    
    # Check high distress patterns
    for phrase, weight in HIGH_DISTRESS_KEYWORDS.items():
        if phrase in query_lower:
            score += weight
    
    # Check moderate distress patterns
    for phrase, weight in MODERATE_DISTRESS_KEYWORDS.items():
        if phrase in query_lower:
            score += weight
    
    # Check mild distress patterns
    for phrase, weight in MILD_DISTRESS_KEYWORDS.items():
        if phrase in query_lower:
            score += weight
    
    # Apply intensity modifiers
    score = apply_intensity_modifiers(query, score)
    
    # Determine distress level based on adjusted score thresholds
    if score >= 10:
        return 'high'
    elif score >= 5:
        return 'moderate'
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
    
    # Punctuation modifiers - exclamation marks
    exclamation_count = query.count('!')
    if exclamation_count >= 3:
        modified_score += 2 * (exclamation_count - 2)
    
    # ALL CAPS modifier (indicates shouting/intensity)
    words = query.split()
    caps_words = [w for w in words if w.isupper() and len(w) > 2]
    if len(caps_words) >= 2:
        modified_score += 3
    
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
        for phrase, weight in {**HIGH_DISTRESS_KEYWORDS, **MODERATE_DISTRESS_KEYWORDS, **MILD_DISTRESS_KEYWORDS}.items():
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
