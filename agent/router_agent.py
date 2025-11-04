"""
Router Agent - Intelligent query routing with RAG context
"""

from typing import TypedDict, List, Tuple
from langchain_groq import ChatGroq
import re
import logging

# Configure logger for router agent
logger = logging.getLogger(__name__)


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
    # Soft/qualifying phrases
    "a bit off": 1, "feeling a bit off": 1,
    "down in the dumps": 1, "feeling blue": 1, "melancholy": 1,
    "anxious mess": 1, "emotional wreck": 1, "emotional": 1,
    "can't focus": 1, "cant focus": 1, "distracted": 1,
    "irritable": 1, "restless": 1, "tense": 1, "uneasy": 1,
    "overthinking": 1, "ruminating": 1, "obsessing": 1,
    "self-doubting": 1, "doubting myself": 1, "insecure": 1,
    "frustrated": 1, "angry": 1, "upset": 1,
    "sad": 1, "depressed": 1, "anxious": 1,  # Common standalone emotions
    "stressed": 1, "down": 1,  # Removed duplicate "worried"
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
    distress_level: str  # 'high', 'mild', or 'none'
    last_menu_options: List[str]  # Track menu options for stateful turn tracking
    turn_count: int  # Track conversation turns


def detect_crisis(query: str) -> bool:
    """Detect crisis keywords in user query."""
    crisis_keywords = [
        "suicide", "suicidal", "kill myself", "end my life", "want to die",
        "self harm", "hurt myself", "cutting", "overdose", "no reason to live",
        "better off dead", "can't go on", "end it all"
    ]
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in crisis_keywords)


def detect_explicit_intent(query: str) -> str:
    """
    Detect if user has explicit intent for a specific agent.
    Returns agent name or empty string.
    Priority order: assessment > resource > escalation
    """
    query_lower = query.lower()
    
    # Assessment intent - highest priority for explicit requests
    assessment_keywords = ['assessment', 'test', 'evaluate', 'screen', 'dass', 'phq']
    if any(keyword in query_lower for keyword in assessment_keywords):
        return "assessment"
    
    # Resource intent - includes Singapore services and specific helplines/services
    resource_keywords = [
        'support service', 'mental health service', 'singapore service',
        'hotline', 'helpline', 'crisis line', 'call', 'phone',
        'imh', 'sos', 'samaritans', 'chat service', 'chat center',
        'therapy', 'therapist', 'counseling', 'counselor', 'psychiatrist',
        'clinic', 'hospital', 'emergency', 'urgent care',
        'where can i', 'where to', 'who can help', 'where to get help'
    ]
    if any(keyword in query_lower for keyword in resource_keywords):
        return "resource"
    
    # Human escalation - professional help requests
    escalation_keywords = ['talk to someone', 'speak to professional', 'real person', 'human counselor']
    if any(keyword in query_lower for keyword in escalation_keywords):
        return "human_escalation"
    
    return ""


def detect_menu_reply(query: str, last_menu_options: List[str]) -> bool:
    """
    Detect if user is replying to a numbered menu or selecting an option.
    """
    query_lower = query.lower().strip()
    
    # Check for numbered replies (1, 2, 3, etc.)
    if query_lower.isdigit() and len(last_menu_options) > 0:
        option_num = int(query_lower)
        return 1 <= option_num <= len(last_menu_options)
    
    # Check for text-based selections
    selection_patterns = [
        "first", "second", "third", "fourth", "fifth",
        "first one", "second one", "third one", 
        "the first", "the second", "the third",
        "option 1", "option 2", "option 3",
        "choice 1", "choice 2", "choice 3"
    ]
    
    return any(pattern in query_lower for pattern in selection_patterns)


def update_menu_context(state: AgentState, menu_options: List[str]) -> None:
    """
    Update the state with menu options for stateful turn tracking.
    Call this from agents when presenting numbered menus or options to users.
    """
    state["last_menu_options"] = menu_options


def extract_menu_selection(query: str, menu_options: List[str]) -> str:
    """
    Extract the selected menu option from user query.
    Returns the selected option text or empty string if no valid selection.
    """
    query_lower = query.lower().strip()
    
    # Handle numbered selection (1, 2, 3, etc.)
    if query_lower.isdigit():
        option_num = int(query_lower)
        if 1 <= option_num <= len(menu_options):
            return menu_options[option_num - 1]
    
    # Handle text-based selections
    selection_map = {
        "first": 0, "second": 1, "third": 2, "fourth": 3, "fifth": 4,
        "first one": 0, "second one": 1, "third one": 2,
        "the first": 0, "the second": 1, "the third": 2,
        "option 1": 0, "option 2": 1, "option 3": 2,
        "choice 1": 0, "choice 2": 1, "choice 3": 2
    }
    
    for pattern, index in selection_map.items():
        if pattern in query_lower and index < len(menu_options):
            return menu_options[index]
    
    return ""


def _matches_with_word_boundary(phrase: str, text: str) -> bool:
    """
    Check if phrase exists in text with word boundaries.
    Prevents partial matches (e.g., "over" won't match inside "overwhelmed").
    """
    # Escape special regex characters in the phrase
    escaped_phrase = re.escape(phrase)
    # Create pattern with word boundaries
    pattern = r'\b' + escaped_phrase + r'\b'
    return bool(re.search(pattern, text, re.IGNORECASE))


def _is_negated(phrase: str, text: str, phrase_position: int) -> bool:
    """
    Enhanced negation detection that handles various negation patterns.
    
    Handles:
    - Simple negation: "not sad", "never happy"
    - Compound negation: "not at all sad", "not really worried"
    - No/none patterns: "no hope", "not any good"
    """
    # Negation patterns with varying intensities
    negation_patterns = [
        # Strong negation (completely negates)
        r'\b(not|never|no|neither)\s+(at\s+all|really|actually|truly|very|particularly)\s+',
        # Medium negation (with modifiers)
        r'\b(not|never|no)\s+(that|so|too|very)\s+',
        # Simple negation
        r'\b(not|never|no|neither|don\'t|dont|doesn\'t|doesnt|didn\'t|didnt|won\'t|wont|isn\'t|isnt|wasn\'t|wasnt)\s+',
        r'\b(hardly|barely|scarcely)\s+',
    ]
    
    # Look in the 30 characters before the phrase
    start_pos = max(0, phrase_position - 30)
    preceding_text = text[start_pos:phrase_position]
    
    # Check each negation pattern
    for pattern in negation_patterns:
        if re.search(pattern, preceding_text, re.IGNORECASE):
            return True
    
    return False


def detect_distress_level(query: str) -> Tuple[str, float]:
    """
    Detect level of distress in user query using weighted scoring.
    Returns: Tuple of (distress_level, raw_score)
    
    SIMPLIFIED 2-LEVEL SYSTEM:
    - HIGH keywords: 5 points (severe crisis, immediate empathy needed)
    - MILD keywords: 1 point (general support, friendly approach)
    
    Thresholds:
    - 5+: HIGH distress (any high keyword OR 5+ mild keywords with modifiers)
    - 1-4: MILD distress (1-4 mild keywords)
    - 0: NONE
    
    Includes enhanced word-boundary matching and negation handling.
    """
    query_lower = query.lower()
    
    # Calculate weighted score
    score = 0
    
    # Check high distress patterns with word-boundary and negation handling
    for phrase, weight in HIGH_DISTRESS_KEYWORDS.items():
        # Use word-boundary matching to prevent partial matches
        if _matches_with_word_boundary(phrase, query_lower):
            phrase_index = query_lower.find(phrase.lower())
            
            # Enhanced negation detection
            if not _is_negated(phrase, query_lower, phrase_index):
                score += weight
    
    # Check mild distress patterns with word-boundary and negation handling
    for phrase, weight in MILD_DISTRESS_KEYWORDS.items():
        # Use word-boundary matching to prevent partial matches
        if _matches_with_word_boundary(phrase, query_lower):
            phrase_index = query_lower.find(phrase.lower())
            
            # Enhanced negation detection
            if not _is_negated(phrase, query_lower, phrase_index):
                score += weight
    
    # Apply intensity modifiers
    score = apply_intensity_modifiers(query, score)
    
    # Determine distress level - SIMPLIFIED 2-LEVEL SYSTEM
    if score >= 5:
        level = 'high'
    elif score >= 1:
        level = 'mild'
    else:
        level = 'none'
    
    return (level, score)


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
    """Enhanced router with RAG context and prioritized explicit intent detection."""
    query = state["current_query"]
    
    logger.info("="*60)
    logger.info("🧭 [ROUTER AGENT ACTIVATED]")
    logger.info(f"📝 Query: {query}")
    logger.info("="*60)
    
    # Initialize state management fields if not present
    if "last_menu_options" not in state:
        state["last_menu_options"] = []
    if "turn_count" not in state:
        state["turn_count"] = 0
    
    state["turn_count"] += 1
    
    # Priority 1: Crisis detection (highest priority - always override)
    # Check BEFORE expensive context fetch
    if detect_crisis(query):
        state["crisis_detected"] = True
        state["current_agent"] = "crisis_intervention"
        state["messages"].append("🚨 I'm here with you right now - getting you immediate support")
        logger.warning("🚨 PRIORITY 1: Crisis detected → Crisis Agent")
        return state
    
    # Priority 2: Menu replies and contextual references (handle stateful interactions)
    if detect_menu_reply(query, state["last_menu_options"]):
        # User is responding to a menu - check if it's a resource selection
        selected_option = extract_menu_selection(query, state["last_menu_options"])
        
        if selected_option:
            logger.info(f"📋 PRIORITY 2: Menu selection detected → '{selected_option}'")
            
            # Check if this looks like a resource selection (Singapore services, hotlines, etc.)
            resource_keywords = ['hotline', 'helpline', 'chat', 'imh', 'sos', 'samaritans', 'service', 'therapy', 'counseling']
            if any(keyword in selected_option.lower() for keyword in resource_keywords):
                state["current_agent"] = "resource"
                state["context"] = f"User selected: {selected_option}"
                logger.info(f"🏥 Menu selection is a resource → Resource Agent")
                return state
        
        # Default to information agent for other menu replies
        state["current_agent"] = "information"
        logger.info("📋 PRIORITY 2: Menu reply detected → Information Agent (with menu context)")
        return state
    
    # Priority 3: Explicit intent detection (prioritize specific requests)
    explicit_intent = detect_explicit_intent(query)
    if explicit_intent:
        state["current_agent"] = explicit_intent
        logger.info(f"🎯 PRIORITY 3: Explicit intent detected → {explicit_intent.upper()} Agent")
        return state
    
    # Priority 4: Distress detection (only if no explicit intent found)
    # Check BEFORE expensive context fetch
    distress_level, distress_score = detect_distress_level(query)
    
    if distress_level != 'none':
        state["current_agent"] = "information"
        state["distress_level"] = distress_level  # Pass distress level to information agent
        logger.info(f"😔 PRIORITY 4: {distress_level.upper()} distress detected (score: {distress_score:.1f}) → Information Agent")
        return state
    
    # Priority 5: Fallback LLM routing for general queries
    # Only fetch expensive context if we reach this point
    logger.info("🎯 PRIORITY 5: Using LLM routing for general query...")
    
    # Get initial context for routing decisions, but preserve any existing context (like assessment suggestions)
    existing_context = state.get("context", "")
    routing_context = get_relevant_context(f"route classify {query}", n_results=2)
    
    # If we have existing context (e.g., assessment suggestions), keep it and add routing context
    if existing_context:
        state["context"] = existing_context + "\n\n" + routing_context
        logger.debug("🎯 Preserving existing context and adding routing context")
    else:
        state["context"] = routing_context
    
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
        # Generate deterministic seed from query for consistent routing
        import hashlib
        query_seed = int(hashlib.md5(query.lower().strip().encode()).hexdigest()[:8], 16)
        
        routing_response = llm.invoke(
            routing_prompt,
            config={"configurable": {"seed": query_seed}}
        ).content.strip().lower()
        
        # Validate and set agent
        valid_agents = ["information", "resource", "assessment", "human_escalation"]
        if routing_response in valid_agents:
            state["current_agent"] = routing_response
            logger.info(f"✅ LLM routed to: {routing_response.upper()} Agent")
        else:
            # Default to information agent if unclear
            state["current_agent"] = "information"
            logger.warning(f"⚠️  Invalid routing ({routing_response}), defaulting to: INFORMATION Agent")
        
        # Don't add routing message - let the agent respond directly
        
    except Exception as e:
        logger.error(f"❌ Routing error: {e}", exc_info=True)
        logger.warning("⚠️  Defaulting to: INFORMATION Agent")
        state["current_agent"] = "information"  # Safe default
    
    return state
