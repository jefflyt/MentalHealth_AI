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
    query = state["current_query"]
    
    # Get DASS-21 and assessment context
    assessment_context = get_relevant_context(f"DASS-21 mental health assessment screening {query}", n_results=3)
    
    assessment_prompt = f"""
    Based on the DASS-21 assessment guidelines and mental health screening protocols:
    
    Context: {assessment_context}
    
    User Query: "{query}"
    
    Provide:
    - Information about mental health self-assessment
    - Guidance on DASS-21 screening if appropriate
    - Explanation of what assessments can and cannot determine
    - Clear next steps for professional evaluation
    
    Emphasize that self-assessment tools are not diagnostic and professional evaluation is important.
    """
    
    try:
        response = llm.invoke(assessment_prompt).content
        
        response += "\n\n⚠️ *Self-assessment tools provide insights but cannot replace professional diagnosis. Consider speaking with a mental health professional for comprehensive evaluation.*"
        
    except Exception as e:
        print(f"Assessment agent error: {e}")
        response = """
        Mental health self-assessment can provide valuable insights into your wellbeing. The DASS-21 is a validated screening tool that measures depression, anxiety, and stress levels.
        
        Would you like information about:
        - How mental health screening works
        - What the DASS-21 assessment covers
        - Where to get professional assessment in Singapore
        
        Remember: Self-assessment tools are helpful for awareness but cannot replace professional evaluation.
        """
    
    state["messages"].append(response)
    state["current_agent"] = "complete"
    return state
