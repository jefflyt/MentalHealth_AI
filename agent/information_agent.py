"""
Information Agent - Mental health education with evidence-based knowledge
"""

from typing import TypedDict, List
from langchain_groq import ChatGroq


class AgentState(TypedDict):
    current_query: str
    messages: List[str]
    current_agent: str
    crisis_detected: bool
    context: str


def information_agent_node(state: AgentState, llm: ChatGroq, get_relevant_context) -> AgentState:
    """RAG-enhanced information agent with knowledge base."""
    query = state["current_query"]
    conversation_history = state.get("messages", [])
    
    # Use LLM to detect emotional distress (more flexible than keywords)
    distress_check_prompt = f"""Analyze this message for emotional distress or mental health concerns.

User message: "{query}"

Does this message indicate the person is:
- Feeling unwell emotionally/mentally
- Struggling or having a hard time
- Expressing negative emotions (sad, anxious, scared, overwhelmed, etc.)
- Asking for help or support

Respond with ONLY "YES" or "NO"."""

    try:
        distress_response = llm.invoke(distress_check_prompt).content.strip().upper()
        sounds_unstable = "YES" in distress_response
    except:
        # Fallback to basic keyword detection if LLM fails
        distress_keywords = ['not feel', 'feel bad', 'struggling', 'help', 'hard time', 'difficult']
        sounds_unstable = any(keyword in query.lower() for keyword in distress_keywords)
    
    # Define agent services with keywords/numbers
    agent_services = {
        '1': {
            'name': 'Understanding feelings',
            'keywords': ['anxiety', 'stress', 'depression', 'feeling', 'emotion', 'mood', 'sad', 'worried'],
            'topic': 'understanding emotions and mental health'
        },
        '2': {
            'name': 'Coping strategies',
            'keywords': ['cope', 'coping', 'manage', 'deal', 'handle', 'breathe', 'relax', 'calm', 'technique'],
            'topic': 'coping strategies and relaxation techniques'
        },
        '3': {
            'name': 'Support services in Singapore',
            'keywords': ['support', 'service', 'help', 'singapore', 'chat', 'imh', 'therapy', 'counseling', 'hotline'],
            'topic': 'Singapore mental health support services'
        },
        '4': {
            'name': 'Just talk',
            'keywords': ['talk', 'listen', 'chat', 'vent', 'share', 'tell'],
            'topic': 'conversation and listening support'
        }
    }
    
    # Check if user selected a number or mentioned keywords
    selected_service = None
    
    # Check for number selection
    if query.strip() in ['1', '2', '3', '4']:
        selected_service = agent_services[query.strip()]
    else:
        # Check for keyword matches
        query_lower = query.lower()
        for service_num, service in agent_services.items():
            if any(keyword in query_lower for keyword in service['keywords']):
                selected_service = service
                break
    
    # Flow logic
    if selected_service:
        # User selected a service - provide relevant info
        info_context = get_relevant_context(selected_service['topic'], n_results=2)
        
        prompt = f"""User wants help with: {selected_service['name']}

Context:
{info_context}

Provide brief, helpful information (2-3 sentences) about {selected_service['topic']}. Be warm and practical.

Response:"""
        
        try:
            response = llm.invoke(prompt).content
            
            # Limit length
            sentences = response.split('. ')
            if len(sentences) > 4:
                response = '. '.join(sentences[:4]) + '.'
            
            response += "\n\n📚 *Based on evidence-based resources*"
            
        except Exception as e:
            print(f"Service response error: {e}")
            response = f"I can help you with {selected_service['name'].lower()}. What specifically would you like to know?"
        
        state["messages"].append(response)
        state["current_agent"] = "complete"
        return state
        
    elif sounds_unstable:
        # User is distressed - show numbered agent options
        response = """I'm here for you. I can help with:

1. Understanding feelings (anxiety, stress, depression)
2. Coping strategies and techniques
3. Finding support services in Singapore
4. Or just listen and talk

Just type the number or tell me what you need."""
        
        state["messages"].append(response)
        state["current_agent"] = "complete"
        return state
        
    else:
        # Normal conversation - just be friendly and supportive
        prompt = f"""You're Alex, a caring friend. User said: "{query}"

Continue the conversation naturally. Be warm, brief (1-2 sentences), and show interest.

Examples:
"Hey, how's it going?"
"I'm listening. What's on your mind?"
"That makes sense. How are you feeling about it?"

Respond warmly in 1-2 sentences:"""
    
        try:
            response = llm.invoke(prompt).content
            
            # Hard limit on length
            sentences = response.split('. ')
            if len(sentences) > 4:
                response = '. '.join(sentences[:4]) + '.'
            
        except Exception as e:
            print(f"Information agent error: {e}")
            response = "I'm here for you. What's on your mind?"
        
        state["messages"].append(response)
        state["current_agent"] = "complete"
        return state
