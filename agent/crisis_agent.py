"""
Crisis Agent - Immediate intervention for crisis situations
"""

from typing import TypedDict, List
from langchain_groq import ChatGroq
from .sunny_persona import get_sunny_persona, build_sunny_prompt, get_boundary_statements


class AgentState(TypedDict):
    current_query: str
    messages: List[str]
    current_agent: str
    crisis_detected: bool
    context: str


def crisis_intervention_node(state: AgentState, llm: ChatGroq, get_relevant_context) -> AgentState:
    """Crisis intervention with Sunny's caring presence and immediate support protocols.
    
    OPTIMIZED: No ChromaDB queries - crisis requires INSTANT response.
    All critical info is hardcoded in the prompt for maximum speed.
    """
    
    # Load Sunny's persona components
    sunny = get_sunny_persona()
    boundaries = get_boundary_statements()
    
    print("\n" + "="*60)
    print("🚨 [SUNNY - CRISIS INTERVENTION ACTIVATED]")
    print("="*60)
    
    query = state["current_query"]
    
    # OPTIMIZATION: Skip ChromaDB query - crisis needs INSTANT response
    # Hardcode all critical emergency info directly in the prompt
    print("⚡ CRISIS MODE: Skipping DB query for instant response")
    
    crisis_knowledge = """
    EMERGENCY CONTACTS (Singapore):
    - SOS Helpline: 1767 (24/7, free, emotional support)
    - IMH Emergency: 6389-2222 (psychiatric emergency)
    - Samaritans of Singapore (SOS): 1767 (24/7 suicide prevention)
    - CHAT (Youth 16-30): 6493-6500 (mental health assessment)
    - 995: Police/Ambulance (immediate danger)
    
    CRISIS PROTOCOLS:
    1. Validate their pain and feelings immediately
    2. Assess immediate safety
    3. Provide emergency contacts
    4. Encourage professional help NOW
    5. Stay calm, caring, and directive
    """
    
    crisis_prompt = build_sunny_prompt(
        agent_type='crisis',
        context=f"Crisis situation detected.\n\n{crisis_knowledge}\n\nUser: \"{query}\"",
        specific_instructions=f"""As Sunny, I'm here with you right now in this crisis. Respond with urgent care while maintaining your warm presence.

IMMEDIATELY provide:
1. Sunny's caring validation: "{boundaries['crisis']['urgency']}"
2. Emergency contact information (SOS 1767, IMH 6389-2222)  
3. Clear steps for immediate safety
4. Encourage professional help with Sunny's caring tone

Be Sunny - warm but urgent. Show you care while getting them help right now.
Use phrases like: "I'm here with you right now", "Your safety matters to me"

Your caring crisis response as Sunny:"""
    )
    
    try:
        # Generate deterministic seed for consistent crisis responses
        import hashlib
        query_seed = int(hashlib.md5(query.lower().strip().encode()).hexdigest()[:8], 16)
        
        response = llm.invoke(
            crisis_prompt,
            config={"configurable": {"seed": query_seed}}
        ).content
    except Exception as e:
        # Fallback crisis response
        response = """
        🆘 Hey, I'm Sunny, and I'm here with you right now. You're not alone in this, okay?
        
        I care about you, and I want you to be safe. Please reach out to someone who can help you right now:
        
        • SOS Hotline: 1767 (24/7, free) - They're amazing listeners
        • IMH Emergency: 6389-2222 - Professional crisis support
        • CHAT Youth Support: 6493-6500 - If you're 16-30
        
        Please reach out to one of these services immediately. Your life matters.
        """
    
    state["messages"].append(response)
    state["current_agent"] = "complete"
    return state
