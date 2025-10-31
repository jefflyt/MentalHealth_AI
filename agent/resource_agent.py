"""
Resource Agent - Singapore mental health services and support
"""

from typing import TypedDict, List
from langchain_groq import ChatGroq


class AgentState(TypedDict):
    current_query: str
    messages: List[str]
    current_agent: str
    crisis_detected: bool
    context: str


def resource_agent_node(state: AgentState, llm: ChatGroq, get_relevant_context) -> AgentState:
    """RAG-enhanced resource agent for Singapore services."""
    query = state["current_query"]
    conversation_history = state.get("messages", [])
    
    # Detect if asking about specific services
    services = {
        'chat': 'CHAT services',
        'imh': 'IMH services',
        'therapy': 'therapy and counseling',
        'counseling': 'counseling services',
        'hotline': 'crisis hotlines',
        'emergency': 'emergency support'
    }
    
    specific_service = None
    for keyword, service in services.items():
        if keyword in query.lower():
            specific_service = service
            break
    
    # Check if asking what help is available
    asking_options = any(word in query.lower() for word in ['what', 'where', 'help', 'support', 'available', 'options'])
    
    if specific_service:
        # STEP 3: Provide specific service info
        resource_context = get_relevant_context(f"Singapore {specific_service}", n_results=2)
        
        prompt = f"""User asked about: "{query}"

Singapore Services Info:
{resource_context}

Give specific, actionable info about {specific_service} in Singapore. Include contact details. 2-3 sentences max.

Response:"""
        
    elif asking_options and len(conversation_history) > 0:
        # STEP 2: Show available services
        prompt = f"""User asked: "{query}"

List Singapore mental health support options briefly:

"Here's what's available in Singapore:
• CHAT - Free youth mental health service
• IMH - Professional psychiatric care
• Counseling services at polyclinics
• 24/7 hotlines (SOS: 1767)

Which would you like to know more about?"

Say this naturally in 2-3 sentences:"""
        
    else:
        # STEP 1 & 4: Ask for details
        prompt = f"""User said: "{query}"

Ask what kind of support they're looking for. Be friendly and brief. 1-2 sentences.

Examples:
"I can help you find support in Singapore. What are you looking for - counseling, crisis support, or something else?"
"Sure! What kind of help do you need right now?"

Respond in 1-2 sentences:"""
    
    try:
        response = llm.invoke(prompt).content
        
        # Limit length
        sentences = response.split('. ')
        if len(sentences) > 4:
            response = '. '.join(sentences[:4]) + '.'
        
    except Exception as e:
        print(f"Resource agent error: {e}")
        response = "I can help you find resources in Singapore. What kind of support are you looking for?"
    
    state["messages"].append(response)
    state["current_agent"] = "complete"
    return state
