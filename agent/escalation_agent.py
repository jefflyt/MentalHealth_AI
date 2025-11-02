"""
Human Escalation Agent - Professional referrals and complex case support
"""

from typing import TypedDict, List
from langchain_groq import ChatGroq


class AgentState(TypedDict):
    current_query: str
    messages: List[str]
    current_agent: str
    crisis_detected: bool
    context: str


def human_escalation_node(state: AgentState, llm: ChatGroq, get_relevant_context) -> AgentState:
    """RAG-enhanced human escalation with professional referrals."""
    
    print("\n" + "="*60)
    print("🤝 [AGENT ACTIVATED: Human Escalation Agent]") 
    print("="*60)
    
    query = state["current_query"]
    external_context = state.get("context", "")  # Assessment results or other context
    
    # Get professional referral context
    referral_context = get_relevant_context(f"professional mental health referral Singapore complex cases {query}", n_results=3)
    
    # Check if this is an assessment suggestion rather than a crisis
    if external_context and "ASSESSMENT_SUGGESTION" in external_context:
        print("🎯 Including assessment suggestion context")
        assessment_suggestion = True
    else:
        assessment_suggestion = False
    
    if assessment_suggestion:
        escalation_prompt = f"""
        You are Sunny, a warm and caring digital friend. The user has been giving vague responses and would benefit from a self-assessment.
        
        User's recent responses: "{query}"
        Context: {external_context}
        
        As Sunny, respond with your caring personality:
        
        1. Gently acknowledge they seem to be going through something: "I notice you've been giving short responses..."
        2. Suggest that a quick self-assessment might help them understand their feelings better
        3. Mention specific options: DASS-21 for comprehensive screening, Quick Mood Check, or Stress Level Assessment
        4. Be warm and encouraging - this could help you get more targeted support
        
        Keep it friendly and supportive, like a caring friend suggesting something helpful.
        """
    else:
        escalation_prompt = f"""
        You are Sunny, a warm and caring digital friend who knows about mental health resources. Someone needs professional support.
        
        Context about Singapore services: {referral_context}
        User's situation: "{query}"
        
        As Sunny, respond with your caring, friend-like personality:
        
        1. Acknowledge their situation with genuine empathy - "I can really hear that..."
        2. Gently suggest professional help as their supportive friend would
        3. Recommend ONE specific service in Singapore that fits best
        4. End with warm encouragement about taking this positive step
        
        Use Sunny's style: conversational, caring, like talking to a trusted friend who wants the best for you. Avoid clinical language or lists. Keep it warm and personal.
        """
    
    try:
        response = llm.invoke(escalation_prompt).content
        

        
    except Exception as e:
        print(f"Human escalation error: {e}")
        response = """Hey, I'm Sunny, and I can really hear that you're going through something significant. I think talking to a professional could make a real difference for you, and I care about you getting the support you deserve.

        If you're between 16-30, CHAT offers free mental health support - you can just walk into their centers at Jurong Point, Woodlands, or Hougang, or call them at 6493-6500. They're really understanding people and it's completely free.

        For anyone older, IMH has great outpatient services you can access by calling 6389-2200. They'll help you figure out the best support for your specific situation.

        Taking this step isn't always easy, but you're absolutely worth the investment in getting the right kind of help. I believe in you! 🤝 😊"""
    
    state["messages"].append(response)
    state["current_agent"] = "complete"
    return state
