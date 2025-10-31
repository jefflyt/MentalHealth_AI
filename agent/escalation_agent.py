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
    query = state["current_query"]
    
    # Get professional referral context
    referral_context = get_relevant_context(f"professional mental health referral Singapore complex cases {query}", n_results=3)
    
    escalation_prompt = f"""
    Based on professional referral guidelines and Singapore mental health services:
    
    Context: {referral_context}
    
    User Query: "{query}"
    
    This case requires human professional support. Provide:
    - Validation of the complexity/importance of their concerns
    - Specific professional services in Singapore that can help
    - How to access professional mental health support
    - What to expect from professional consultation
    
    Be supportive and emphasize that seeking professional help is a positive step.
    """
    
    try:
        response = llm.invoke(escalation_prompt).content
        
        response += "\n\n🤝 *Connecting with a mental health professional shows strength and self-care. You deserve comprehensive support for your mental health journey.*"
        
    except Exception as e:
        print(f"Human escalation error: {e}")
        response = """
        Your concerns are important and would benefit from personalized professional support. 
        
        🤝 **Professional Support Options in Singapore:**
        
        **CHAT (Free, Ages 16-30):**
        • Walk-in service at Jurong Point, Woodlands, Hougang
        • Call 6493-6500
        
        **IMH Outpatient Services:**
        • Call 6389-2200 for appointments
        • Comprehensive mental health services
        
        **Private Practice:**
        • Singapore Psychological Society: Online directory
        • Various locations and specialties available
        
        Taking this step shows strength and self-awareness. Professional support can provide personalized strategies for your specific situation.
        """
    
    state["messages"].append(response)
    state["current_agent"] = "complete"
    return state
