"""
Information Agent - Mental health education with evidence-based knowledge
"""

from typing import TypedDict, List
from langchain_groq import ChatGroq
from .sunny_persona import get_sunny_persona, get_distress_responses, build_sunny_prompt


class AgentState(TypedDict):
    current_query: str
    messages: List[str]
    current_agent: str
    crisis_detected: bool
    context: str
    distress_level: str  # 'high', 'moderate', 'mild', or 'none'


def information_agent_node(state: AgentState, llm: ChatGroq, get_relevant_context) -> AgentState:
    """RAG-enhanced information agent with Sunny's personality."""
    query = state["current_query"]
    conversation_history = state.get("messages", [])
    distress_level = state.get("distress_level", "none")
    
    # Load Sunny's persona components
    sunny = get_sunny_persona()
    distress_responses = get_distress_responses()
    
    print("\n" + "="*60)
    print("📚 [SUNNY - INFORMATION AGENT ACTIVATED]")
    print("="*60)
    
    # Use distress level from router (more accurate than re-detecting)
    sounds_unstable = distress_level in ['high', 'moderate']
    print(f"🔍 Distress level: {distress_level.upper()}")
    
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
        print(f"✅ User selected option {query.strip()}: {selected_service['name']}")
    else:
        # Check for keyword matches
        query_lower = query.lower()
        for service_num, service in agent_services.items():
            if any(keyword in query_lower for keyword in service['keywords']):
                selected_service = service
                print(f"✅ Keyword match detected → Option {service_num}: {service['name']}")
                break
    
    # Flow logic
    if selected_service:
        # User selected a service - provide relevant info
        print(f"💡 Providing info about: {selected_service['topic']}")
        info_context = get_relevant_context(selected_service['topic'], n_results=1)
        
        prompt = build_sunny_prompt(
            agent_type='information',
            context=f"User wants: {selected_service['name']}\n\nKnowledge context: {info_context}",
            specific_instructions=f"""Provide ONE clear, actionable tip (1-2 sentences max). Use your validation phrases like: {', '.join(sunny['validation_phrases'][:3])}

Example response style:
"Try taking three slow, deep breaths - it really can help calm your mind when things feel overwhelming. You've got this! 😊"

Your warm, helpful tip:"""
        )
        
        try:
            response = llm.invoke(prompt).content.strip()
            
            # Hard limit - only first 2 sentences
            sentences = [s.strip() for s in response.split('.') if s.strip()]
            if len(sentences) > 2:
                response = '. '.join(sentences[:2]) + '.'
            
            # Add formatting for readability
            response = f"{response}\n\n� *Want to know more? Just ask!*"
            
        except Exception as e:
            print(f"Service response error: {e}")
            response = f"I can help with {selected_service['name'].lower()}. What would you like to know?"
        
        state["messages"].append(response)
        state["current_agent"] = "complete"
        return state
        
    elif sounds_unstable:
        # User is distressed - show response based on distress level
        print(f"📋 Showing Sunny's {distress_level} distress response")
        
        distress_response = distress_responses[distress_level]
        
        if distress_level == 'high':
            # High distress - immediate empathy + menu
            response = f"""{distress_response['opening']}

{distress_response['context']}

I can support you with:

1️⃣ Understanding what you're feeling
2️⃣ Coping strategies that can help right now  
3️⃣ Connecting you to professional support in Singapore
4️⃣ Just being here to listen - whatever you need

Type a number (1-4), or just tell me more about what's happening. I'm not going anywhere. 😊"""

        elif distress_level == 'moderate':
            # Moderate distress - warm acknowledgment + menu
            response = f"""{distress_response['opening']}

I can help with:

1️⃣ Understanding your feelings
2️⃣ Coping strategies and techniques  
3️⃣ Finding support services in Singapore
4️⃣ Just someone to talk to - I'm a good listener!

Type a number (1-4), or just tell me what's on your mind. 😊"""

        else:  # mild distress
            # Mild distress - brief, welcoming, open-ended
            response = f"""{distress_response['opening']}

What would you like help with?
• Understanding emotions
• Coping strategies  
• Support services in Singapore
• Or just talk - I'm a good listener!

What's on your mind today?"""
        
        state["messages"].append(response)
        state["current_agent"] = "complete"
        return state
        
    else:
        # Normal conversation - be friendly and supportive (VERY brief)
        print("💬 Sunny's casual conversation mode")
        prompt = build_sunny_prompt(
            agent_type='information',
            context=f'User said: "{query}"',
            specific_instructions=f"""If this is about mental health, wellbeing, or emotions: Respond as Sunny with warmth and support in 1-2 SHORT sentences using phrases like: {', '.join(sunny['validation_phrases'][:2])}

If this is NOT about mental health: Use Sunny's redirect: "{sunny['redirect_template']}"

Your warm response as Sunny:"""
        )
    
        try:
            response = llm.invoke(prompt).content.strip()
            
            # VERY hard limit - max 2 sentences
            sentences = [s.strip() for s in response.split('.') if s.strip()]
            response = '. '.join(sentences[:2]) + '.' if sentences else "I'm here for you. What's on your mind?"
            
        except Exception as e:
            print(f"Information agent error: {e}")
            response = f"{sunny['validation_phrases'][0]}. What's on your mind? 💙"
        
        state["messages"].append(response)
        state["current_agent"] = "complete"
        return state