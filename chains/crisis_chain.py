"""
Crisis Detection Chain - Advanced crisis and distress detection
Analyzes messages for self-harm, suicidal ideation, and severe distress
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Dict, Tuple


def create_crisis_detection_chain(llm):
    """
    Create a crisis detection chain for immediate safety assessment.
    
    Args:
        llm: LangChain LLM instance
        
    Returns:
        Crisis detection chain
    """
    
    crisis_prompt = ChatPromptTemplate.from_template("""You are a crisis detection system for mental health support.

Analyze the user's message for signs of immediate danger or crisis.

User Message: {message}

Look for:
- Suicidal ideation (thoughts of ending life)
- Self-harm intent or behavior
- Immediate danger to self or others
- Severe emotional distress requiring urgent intervention
- Expressions of hopelessness with plans or means

Output a JSON with:
{{
    "is_crisis": true/false,
    "severity": "CRITICAL/HIGH/MODERATE/LOW",
    "indicators": ["list", "of", "crisis", "indicators"],
    "recommended_action": "immediate_crisis_intervention/supportive_monitoring/standard_support"
}}

Output ONLY valid JSON.

Analysis:""")
    
    crisis_chain = crisis_prompt | llm | StrOutputParser()
    
    return crisis_chain


def create_distress_level_chain(llm):
    """
    Create a chain to assess emotional distress level.
    
    Args:
        llm: LangChain LLM instance
        
    Returns:
        Distress level chain
    """
    
    distress_prompt = ChatPromptTemplate.from_template("""Assess the emotional distress level in this message.

User Message: {message}

Distress Levels:
- HIGH: Severe distress, crisis indicators, immediate need
- MILD: Moderate distress, struggling but stable
- NONE: Neutral, informational, low distress

Consider:
- Emotional intensity
- Urgency of need
- Presence of crisis indicators
- Coping ability

Output ONLY: HIGH, MILD, or NONE

Distress Level:""")
    
    distress_chain = distress_prompt | llm | StrOutputParser()
    
    return distress_chain


def create_safety_assessment_chain(llm):
    """
    Create a comprehensive safety assessment chain.
    
    Args:
        llm: LangChain LLM instance
        
    Returns:
        Safety assessment chain
    """
    
    safety_prompt = ChatPromptTemplate.from_template("""Conduct a safety assessment based on this message.

User Message: {message}
Context: {context}

Assessment Areas:
1. Suicidal Ideation (thoughts, plans, means, intent)
2. Self-Harm Risk (current or recent)
3. Safety Planning (protective factors, support system)
4. Immediate Danger (timeframe, urgency)

Output JSON:
{{
    "suicide_risk": "IMMEDIATE/HIGH/MODERATE/LOW/NONE",
    "self_harm_risk": "IMMEDIATE/HIGH/MODERATE/LOW/NONE",
    "protective_factors": ["list", "if", "present"],
    "risk_factors": ["list", "if", "present"],
    "requires_emergency": true/false,
    "recommended_resources": ["specific", "resources"]
}}

Output ONLY valid JSON.

Assessment:""")
    
    safety_chain = safety_prompt | llm | StrOutputParser()
    
    return safety_chain


def detect_crisis_with_context(message: str, llm, conversation_history: str = "") -> Dict:
    """
    Detect crisis with conversation context.
    
    Args:
        message: Current user message
        llm: LangChain LLM instance
        conversation_history: Previous conversation context
        
    Returns:
        Dictionary with crisis detection results
    """
    
    import json
    
    # Create enhanced prompt with context
    contextual_crisis_prompt = ChatPromptTemplate.from_template("""Analyze this message for crisis indicators with conversation context.

Conversation History:
{history}

Current Message: {message}

Provide crisis assessment as JSON:
{{
    "is_crisis": true/false,
    "severity": "CRITICAL/HIGH/MODERATE/LOW",
    "crisis_type": "suicide/self_harm/severe_distress/none",
    "indicators": ["specific", "indicators", "found"],
    "urgency": "immediate/urgent/monitor/none",
    "confidence": 0.0-1.0
}}

Output ONLY valid JSON.

Analysis:""")
    
    chain = contextual_crisis_prompt | llm | StrOutputParser()
    
    result = chain.invoke({
        "message": message,
        "history": conversation_history or "No previous conversation"
    })
    
    try:
        # Parse JSON result
        crisis_data = json.loads(result)
        return crisis_data
    except json.JSONDecodeError:
        # Fallback simple detection
        return {
            "is_crisis": False,
            "severity": "UNKNOWN",
            "crisis_type": "none",
            "indicators": [],
            "urgency": "none",
            "confidence": 0.0
        }


def assess_distress_level(message: str, llm) -> Tuple[str, float]:
    """
    Quick distress level assessment.
    
    Args:
        message: User message
        llm: LangChain LLM instance
        
    Returns:
        Tuple of (distress_level, confidence)
    """
    
    chain = create_distress_level_chain(llm)
    level = chain.invoke({"message": message}).strip().upper()
    
    # Map to standardized levels
    if "HIGH" in level or "CRISIS" in level:
        return ("HIGH", 0.9)
    elif "MILD" in level or "MODERATE" in level:
        return ("MILD", 0.8)
    else:
        return ("NONE", 0.7)
