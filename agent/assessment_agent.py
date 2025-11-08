"""
Assessment Agent - Mental health screening and DASS-21 guidance
"""

from typing import TypedDict, List
from langchain_groq import ChatGroq


# ============================================================================
# STATIC TEMPLATES - No LLM needed for standard assessment info
# ============================================================================

DASS21_EXPLANATION = """Hey, I'm Sunny! 😊

**About DASS-21 Assessment:**

The DASS-21 is a self-report questionnaire that helps you understand your current emotional state across three areas:

📊 **Depression** - Measures feelings of hopelessness, low mood, and lack of interest
📊 **Anxiety** - Measures worry, nervousness, and physical anxiety symptoms  
📊 **Stress** - Measures tension, irritability, and difficulty relaxing

**How it works:**
• 21 questions (7 for each area)
• Rate how much each statement applied to you over the past week
• Takes about 5-10 minutes
• Results show severity levels: Normal, Mild, Moderate, Severe, Extremely Severe

**Important to remember:** 💙
✓ This is a screening tool, not a diagnosis
✓ It gives you insight into your current emotional state
✓ Results can help you understand if professional support might be helpful
✓ A mental health professional can provide a complete assessment

Want to take the DASS-21? I'm here to support you through it! 😊"""


ASSESSMENT_GENERAL_INFO = """Hey, I'm Sunny! 😊

**Mental Health Self-Assessment:**

Self-assessment tools are like having a caring check-in with yourself. They help you:

✓ **Understand your feelings** - Put words to what you're experiencing
✓ **Track patterns** - Notice changes over time
✓ **Make informed decisions** - Know when to seek more support
✓ **Start conversations** - Share results with professionals

**Available assessments:**
📋 **DASS-21** - Comprehensive (Depression, Anxiety, Stress)
📋 **Quick Mood Check** - Fast emotional snapshot
📋 **Stress Level** - Focused on stress symptoms

**Remember:** These tools are starting points, not diagnoses. Think of them as a friendly nudge to check in with yourself - and a mental health professional can give you the complete picture and personalized care you deserve! 💙

What would you like to know more about?"""


DASS21_SCORE_TEMPLATE = """**Your DASS-21 Results:** 📊

**Depression:** {depression_score} - {depression_severity}
**Anxiety:** {anxiety_score} - {anxiety_severity}
**Stress:** {stress_score} - {stress_severity}

**What this means:**

{interpretation}

**Severity Ranges:**
• Normal: 0-9 (Depression), 0-7 (Anxiety), 0-14 (Stress)
• Mild: 10-13 (D), 8-9 (A), 15-18 (S)
• Moderate: 14-20 (D), 10-14 (A), 19-25 (S)
• Severe: 21-27 (D), 15-19 (A), 26-33 (S)
• Extremely Severe: 28+ (D), 20+ (A), 34+ (S)

**Next Steps:**

{recommendations}

Remember, I'm here as your supportive friend, but a mental health professional can give you personalized care and guidance. You're worth that investment! 💙😊"""


def get_severity_level(score: int, assessment_type: str) -> str:
    """
    Calculate severity level from DASS-21 score.
    Returns: 'Normal', 'Mild', 'Moderate', 'Severe', or 'Extremely Severe'
    """
    if assessment_type.lower() == 'depression':
        if score <= 9: return 'Normal'
        elif score <= 13: return 'Mild'
        elif score <= 20: return 'Moderate'
        elif score <= 27: return 'Severe'
        else: return 'Extremely Severe'
    
    elif assessment_type.lower() == 'anxiety':
        if score <= 7: return 'Normal'
        elif score <= 9: return 'Mild'
        elif score <= 14: return 'Moderate'
        elif score <= 19: return 'Severe'
        else: return 'Extremely Severe'
    
    elif assessment_type.lower() == 'stress':
        if score <= 14: return 'Normal'
        elif score <= 18: return 'Mild'
        elif score <= 25: return 'Moderate'
        elif score <= 33: return 'Severe'
        else: return 'Extremely Severe'
    
    return 'Unknown'


def format_dass21_results(depression: int, anxiety: int, stress: int) -> str:
    """
    Format DASS-21 results using static template (NO LLM).
    Returns fully formatted results string.
    """
    # Get severity levels
    dep_severity = get_severity_level(depression, 'depression')
    anx_severity = get_severity_level(anxiety, 'anxiety')
    stress_severity = get_severity_level(stress, 'stress')
    
    # Determine interpretation based on highest severity
    severities = [dep_severity, anx_severity, stress_severity]
    severity_order = ['Normal', 'Mild', 'Moderate', 'Severe', 'Extremely Severe']
    max_severity = max(severities, key=lambda x: severity_order.index(x) if x in severity_order else 0)
    
    # Generate interpretation
    if max_severity == 'Normal':
        interpretation = """Your scores are in the normal range! 😊 This suggests you're managing well overall. Keep up with self-care and healthy coping strategies."""
        recommendations = """• Continue your current self-care practices
• Stay connected with supportive people
• Reach out if things change"""
    
    elif max_severity == 'Mild':
        interpretation = """Your scores show mild symptoms in some areas. This is common and manageable with the right support and coping strategies."""
        recommendations = """• Try stress-reduction techniques (breathing exercises, mindfulness)
• Talk to trusted friends or family
• Consider speaking with a counselor if symptoms persist"""
    
    elif max_severity == 'Moderate':
        interpretation = """Your scores indicate moderate symptoms. This suggests you could benefit from professional support to develop coping strategies."""
        recommendations = """• Consider talking to a mental health professional
• CHAT services (for 16-30): Free counseling at 6493-6500
• Your GP can provide referrals to counseling services"""
    
    else:  # Severe or Extremely Severe
        interpretation = """Your scores indicate significant distress. Professional support is strongly recommended to help you through this difficult time."""
        recommendations = """• Please reach out to a mental health professional soon
• IMH 24/7 Helpline: 6389-2222 for immediate support
• CHAT (16-30): 6493-6500 for free counseling
• Your wellbeing matters - don't wait to seek help"""
    
    # Fill in template
    return DASS21_SCORE_TEMPLATE.format(
        depression_score=depression,
        depression_severity=dep_severity,
        anxiety_score=anxiety,
        anxiety_severity=anx_severity,
        stress_score=stress,
        stress_severity=stress_severity,
        interpretation=interpretation,
        recommendations=recommendations
    )


class AgentState(TypedDict):
    current_query: str
    messages: List[str]
    current_agent: str
    crisis_detected: bool
    context: str


def assessment_agent_node(state: AgentState, llm: ChatGroq, get_relevant_context) -> AgentState:
    """
    Assessment agent with DASS-21 protocols - OPTIMIZED.
    Uses static templates instead of LLM for standard explanations.
    """
    
    print("\n" + "="*60)
    print("📊 [AGENT ACTIVATED: Assessment Agent]")
    print("="*60)
    
    query = state["current_query"]
    query_lower = query.lower()
    
    # ========================================================================
    # OPTIMIZATION 1: Check if asking for DASS-21 explanation (instant answer)
    # ========================================================================
    dass21_keywords = ['dass-21', 'dass 21', 'dass21', 'what is dass', 'tell me about dass', 'explain dass']
    if any(keyword in query_lower for keyword in dass21_keywords):
        print("⚡ DASS-21 EXPLANATION: Returning static template (no LLM)")
        state["messages"].append(DASS21_EXPLANATION)
        state["current_agent"] = "complete"
        return state
    
    # ========================================================================
    # OPTIMIZATION 2: Check if asking for general assessment info (instant answer)
    # ========================================================================
    general_keywords = ['assessment', 'screening', 'self-assessment', 'mental health test', 'evaluation']
    specific_keywords = ['dass-21', 'dass 21', 'phq', 'gad']
    
    # If asking about assessments generally (not specific DASS-21 scores)
    if any(keyword in query_lower for keyword in general_keywords) and not any('score' in query_lower or 'result' in query_lower):
        print("⚡ GENERAL ASSESSMENT INFO: Returning static template (no LLM)")
        state["messages"].append(ASSESSMENT_GENERAL_INFO)
        state["current_agent"] = "complete"
        return state
    
    # ========================================================================
    # OPTIMIZATION 3: Check if providing scores for interpretation (template-based)
    # ========================================================================
    # Pattern: "my scores are X, Y, Z" or "depression X anxiety Y stress Z"
    import re
    score_pattern = r'(\d+).*?(\d+).*?(\d+)'
    score_match = re.search(score_pattern, query)
    
    if score_match and ('score' in query_lower or 'result' in query_lower or 'depression' in query_lower):
        try:
            scores = [int(score_match.group(1)), int(score_match.group(2)), int(score_match.group(3))]
            
            # Validate scores (DASS-21 scores typically 0-42)
            if all(0 <= score <= 42 for score in scores):
                print(f"⚡ SCORE INTERPRETATION: Using template with scores {scores} (no LLM)")
                
                # Assume order: depression, anxiety, stress (most common)
                results = format_dass21_results(scores[0], scores[1], scores[2])
                state["messages"].append(results)
                state["current_agent"] = "complete"
                return state
        except (ValueError, IndexError):
            pass  # Fall through to LLM if parsing fails
    
    # ========================================================================
    # FALLBACK: Use LLM only for specific/unusual assessment questions
    # ========================================================================
    print("💬 SPECIFIC QUERY: Using LLM for nuanced response")
    
    # Get DASS-21 and assessment context
    assessment_context = get_relevant_context(f"DASS-21 mental health assessment screening {query}", n_results=3)
    
    # SIMPLIFIED PROMPT - no lengthy examples
    assessment_prompt = f"""You are Sunny, a caring friend helping with mental health assessment guidance.

Context: {assessment_context}

User Query: "{query}"

Provide warm, supportive guidance about mental health assessments. Keep it brief (2-3 sentences).
Start with "Hey, I'm Sunny! 😊" and emphasize that self-assessment tools provide insights but professional support is valuable."""
    
    try:
        # Generate deterministic seed for consistent assessment responses
        import hashlib
        query_seed = int(hashlib.md5(query.lower().strip().encode()).hexdigest()[:8], 16)
        
        response = llm.invoke(
            assessment_prompt,
            config={"configurable": {"seed": query_seed}}
        ).content
        
        response += "\n\n💙 *Remember, these tools are starting points. A mental health professional can give you the complete picture! 😊*"
        
    except Exception as e:
        print(f"Assessment agent error: {e}")
        # Fallback to general info
        response = ASSESSMENT_GENERAL_INFO
    
    state["messages"].append(response)
    state["current_agent"] = "complete"
    return state
