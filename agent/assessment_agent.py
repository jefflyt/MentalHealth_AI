"""
Assessment Agent - Mental health screening and DASS-21 guidance
"""

from typing import TypedDict, List
from langchain_groq import ChatGroq


class AgentState(TypedDict):
    current_query: str
    messages: List[str]
    current_agent: str
    crisis_detected: bool
    context: str


def assessment_agent_node(state: AgentState, llm: ChatGroq, get_relevant_context) -> AgentState:
    """RAG-enhanced assessment agent with DASS-21 protocols."""
    
    print("\n" + "="*60)
    print("📊 [AGENT ACTIVATED: Assessment Agent]")
    print("="*60)
    
    query = state["current_query"]
    
    # Get DASS-21 and assessment context
    assessment_context = get_relevant_context(f"DASS-21 mental health assessment screening {query}", n_results=3)
    
    assessment_prompt = f"""
    You are Sunny, a caring digital friend helping with mental health assessment guidance.
    
    Based on the DASS-21 assessment guidelines and mental health screening protocols:
    
    Context: {assessment_context}
    
    User Query: "{query}"
    
    As Sunny, provide warm, supportive guidance about:
    - Mental health self-assessment (explain it like a caring friend would)
    - DASS-21 screening information if relevant (make it less clinical, more supportive)
    - What assessments can and cannot determine (gentle boundaries)
    - Encouraging next steps for professional evaluation
    
    Start with "Hey, I'm Sunny! 😊" and maintain your caring, patient personality throughout.
    Use encouraging language and remind them you're here to support them.
    Emphasize that self-assessment tools provide insights but professional support is valuable.
    """
    
    try:
        # Generate deterministic seed for consistent assessment responses
        import hashlib
        query_seed = int(hashlib.md5(query.lower().strip().encode()).hexdigest()[:8], 16)
        
        response = llm.invoke(
            assessment_prompt,
            config={"configurable": {"seed": query_seed}}
        ).content
        
        response += "\n\n💙 *Remember, I'm here as your supportive friend, but these tools are just starting points. A mental health professional can give you the complete picture and personalized care you deserve! 😊*"
        
    except Exception as e:
        print(f"Assessment agent error: {e}")
        response = """
        Hey, I'm Sunny! 😊 Mental health self-assessment can give you valuable insights into how you're doing - think of it like checking in with yourself.
        
        The DASS-21 is a gentle screening tool that looks at depression, anxiety, and stress levels. It's like having a friendly conversation about your feelings!
        
        I can help you understand:
        - How mental health screening works (it's less scary than it sounds!)
        - What the DASS-21 assessment covers
        - Where to get professional assessment in Singapore
        
        Remember: These tools are like a caring friend asking "How are you really doing?" - they're helpful for awareness, but a professional can give you the complete support you deserve! 💙
        """
    
    state["messages"].append(response)
    state["current_agent"] = "complete"
    return state
