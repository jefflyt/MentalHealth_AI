"""
Human Escalation Agent - Professional referrals and complex case support
"""

from typing import TypedDict, List
from langchain_groq import ChatGroq
from .sunny_persona import build_sunny_prompt
import logging

# Configure logger
logger = logging.getLogger(__name__)


# ============================================================================
# RULE-BASED REFERRAL LOGIC - No LLM decision-making needed
# ============================================================================

def decide_referral_service(query: str, distress_level: str = 'none') -> dict:
    """
    Rule-based referral decision (NO LLM).
    Returns: dict with 'service', 'reason', 'priority'
    
    Rules:
    1. High severity/crisis keywords → IMH (24/7 immediate care)
    2. Youth (16-30) indicators → CHAT (free, youth-focused)
    3. Moderate distress → CHAT or IMH based on age
    4. General professional help → CHAT (accessible, free)
    """
    query_lower = query.lower()
    
    # Rule 1: High severity keywords → IMH
    high_severity_keywords = [
        'severe', 'crisis', 'emergency', 'urgent', 'serious',
        'hospitalization', 'hospital', 'psychiatrist', 'psychiatric',
        'medication', 'diagnosis', 'diagnosed', 'treatment',
        'can\'t cope', 'cant cope', 'overwhelming', 'too much'
    ]
    
    if any(keyword in query_lower for keyword in high_severity_keywords):
        return {
            'service': 'IMH',
            'reason': 'high_severity',
            'priority': 'high',
            'number': '6389-2222',
            'availability': '24/7'
        }
    
    # Rule 2: Youth indicators → CHAT
    youth_keywords = [
        'young', 'youth', 'teen', 'teenager', 'student', 'school', 'university',
        '16', '17', '18', '19', '20', 'twenties', 'college'
    ]
    
    if any(keyword in query_lower for keyword in youth_keywords):
        return {
            'service': 'CHAT',
            'reason': 'youth_focused',
            'priority': 'medium',
            'number': '6493-6500',
            'availability': 'Mon-Fri 1-9 PM, Sat 10 AM-4 PM'
        }
    
    # Rule 3: Moderate distress with high distress_level → IMH
    if distress_level == 'high':
        return {
            'service': 'IMH',
            'reason': 'high_distress',
            'priority': 'high',
            'number': '6389-2222',
            'availability': '24/7'
        }
    
    # Rule 4: Default → CHAT (most accessible, free)
    return {
        'service': 'CHAT',
        'reason': 'accessible_default',
        'priority': 'medium',
        'number': '6493-6500',
        'availability': 'Mon-Fri 1-9 PM, Sat 10 AM-4 PM'
    }


# ============================================================================
# PRE-CRAFTED SUNNY TEMPLATES - No LLM generation needed
# ============================================================================

REFERRAL_TEMPLATES = {
    'CHAT_general': """Hey, I can really hear that you're going through something, and I'm glad you reached out. 💙

I think talking to a professional could make a real difference for you. Since you're between 16-30, **CHAT** is a wonderful free resource:

📞 **Call: 6493-6500**
📍 **Walk-in: *SCAPE (Orchard), Jurong Point, Woodlands, Hougang**
🕐 **Hours: Mon-Fri 1-9 PM, Sat 10 AM-4 PM**

**What they offer:**
✓ Free mental health screening
✓ Counseling support
✓ Referrals if needed

They're really understanding people, and it's completely confidential. Taking this step takes courage, but you're absolutely worth the investment in getting the right kind of help. 😊

I believe in you! 🤝""",
    
    'CHAT_youth': """Hey, I'm Sunny, and I can hear that things are tough right now. 💙

For young people like you (16-30), **CHAT** is an amazing free resource:

📞 **Call: 6493-6500** anytime during their hours
📍 **Walk-in centers:**
   - *SCAPE (Orchard Link)
   - Jurong Point
   - Woodlands Civic Centre
   - Hougang Mall

🕐 **Hours:**
   - Mon-Fri: 1 PM - 9 PM
   - Sat: 10 AM - 4 PM

**It's completely free** and they specialize in supporting young adults. They'll listen without judgment and help you figure out the best next steps.

You don't have to face this alone - reaching out is actually really brave. I'm here cheering you on! 😊💙""",
    
    'IMH_high_severity': """Hey, I can really hear how difficult things are for you right now, and I'm glad you're reaching out. 💙

Given what you're experiencing, I think professional support from **IMH (Institute of Mental Health)** would be really helpful:

📞 **24/7 Helpline: 6389-2222**
🚨 **Available anytime, day or night**
📍 **Buangkok Green Medical Park**

**They can help with:**
✓ Immediate mental health support
✓ Assessment and treatment
✓ Crisis intervention
✓ Ongoing psychiatric care

Please don't wait to reach out - your wellbeing matters, and they're there specifically to help people in situations like yours. Taking this step is brave and important.

I care about what happens to you. 🤝😊""",
    
    'IMH_general': """Hey, I can really hear that you're going through something significant. I think talking to a professional could make a real difference for you. 💙

**IMH (Institute of Mental Health)** has excellent services:

📞 **24/7 Helpline: 6389-2222**
📍 **Outpatient appointments: 6389-2200**
🏥 **Buangkok Green Medical Park**

**Services available:**
✓ Psychiatric assessment
✓ Counseling and therapy
✓ Medication management if needed
✓ Specialized treatment programs

They're professionals who deal with these situations every day, and they'll help you figure out the best support for your specific needs.

Taking this step isn't always easy, but you're absolutely worth the investment in getting the right kind of help. I believe in you! 😊🤝""",
    
    'assessment_suggestion': """Hey, I notice you've been giving short responses, and I want to make sure I'm giving you the best support I can. 😊

Sometimes it helps to take a quick self-assessment to understand what you're feeling - it's like having a structured conversation about your emotions.

**Options:**
📋 **DASS-21** - Comprehensive screening (Depression, Anxiety, Stress)
📋 **Quick Mood Check** - Fast emotional snapshot
📋 **Stress Level Assessment** - Focused on stress

These tools can help you:
✓ Put words to what you're experiencing
✓ Understand if you might benefit from professional support
✓ Give professionals helpful information if you do reach out

Would you like to try one? I'm here to support you through it! 💙"""
}


def get_referral_message(service_info: dict, context: str = '') -> str:
    """
    Get pre-crafted Sunny referral message (NO LLM).
    Fills in appropriate template based on service and context.
    """
    service = service_info['service']
    reason = service_info['reason']
    
    # Select appropriate template
    if service == 'CHAT':
        if reason == 'youth_focused':
            return REFERRAL_TEMPLATES['CHAT_youth']
        else:
            return REFERRAL_TEMPLATES['CHAT_general']
    
    elif service == 'IMH':
        if reason == 'high_severity' or reason == 'high_distress':
            return REFERRAL_TEMPLATES['IMH_high_severity']
        else:
            return REFERRAL_TEMPLATES['IMH_general']
    
    # Fallback
    return REFERRAL_TEMPLATES['IMH_general']


class AgentState(TypedDict):
    current_query: str
    messages: List[str]
    current_agent: str
    crisis_detected: bool
    context: str


def human_escalation_node(state: AgentState, llm: ChatGroq, get_relevant_context) -> AgentState:
    """
    Human escalation with professional referrals - OPTIMIZED.
    Uses rule-based logic and pre-crafted templates instead of LLM.
    """
    
    logger.info("="*60)
    logger.info("🤝 [AGENT ACTIVATED: Human Escalation Agent]") 
    logger.info("="*60)
    
    query = state["current_query"]
    external_context = state.get("context", "")
    distress_level = state.get("distress_level", "none")
    
    # ========================================================================
    # OPTIMIZATION 1: Check if this is an assessment suggestion
    # ========================================================================
    if external_context and "ASSESSMENT_SUGGESTION" in external_context:
        logger.info("⚡ ASSESSMENT SUGGESTION: Using pre-crafted template (no LLM)")
        response = REFERRAL_TEMPLATES['assessment_suggestion']
        state["messages"].append(response)
        state["current_agent"] = "complete"
        return state
    
    # ========================================================================
    # OPTIMIZATION 2: Use rule-based logic to decide referral service
    # ========================================================================
    logger.info("🔍 RULE-BASED ROUTING: Determining best service...")
    service_info = decide_referral_service(query, distress_level)
    
    logger.info(f"✅ SELECTED: {service_info['service']} (reason: {service_info['reason']}, priority: {service_info['priority']})")
    
    # ========================================================================
    # OPTIMIZATION 3: Use pre-crafted template for referral message
    # ========================================================================
    logger.info("⚡ PRE-CRAFTED MESSAGE: Using Sunny template (no LLM)")
    response = get_referral_message(service_info, external_context)
    
    state["messages"].append(response)
    state["current_agent"] = "complete"
    return state
