"""
Information Agent - Mental health education with evidence-based knowledge
"""

from typing import TypedDict, List
from langchain_groq import ChatGroq
from .sunny_persona import get_sunny_persona, get_distress_responses, build_sunny_prompt

# Optional re-ranker import (gracefully handles if not installed)
try:
    from .reranker import rerank_documents
    RERANKER_AVAILABLE = True
except ImportError:
    RERANKER_AVAILABLE = False
    def rerank_documents(query, documents, **kwargs):
        """Fallback when re-ranker not available"""
        return documents


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
    external_context = state.get("context", "")  # Assessment results or other context
    
    # Load Sunny's persona components
    sunny = get_sunny_persona()
    distress_responses = get_distress_responses()
    
    print("\n" + "="*60)
    print("📚 [SUNNY - INFORMATION AGENT ACTIVATED]")
    print("="*60)
    
    # Use distress level from router (SIMPLIFIED 2-LEVEL SYSTEM)
    sounds_unstable = distress_level in ['high', 'mild']
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
    # BUT ONLY if they're not in distress - distress responses take priority!
    selected_service = None
    
    # Check for number selection (always works)
    if query.strip() in ['1', '2', '3', '4']:
        selected_service = agent_services[query.strip()]
        print(f"✅ User selected option {query.strip()}: {selected_service['name']}")
    elif not sounds_unstable:
        # Only check keyword matches if user is NOT in distress
        query_lower = query.lower()
        for service_num, service in agent_services.items():
            if any(keyword in query_lower for keyword in service['keywords']):
                selected_service = service
                print(f"✅ Keyword match detected → Option {service_num}: {selected_service['name']}")
                break
    else:
        print("🚨 User in distress - skipping keyword matching, prioritizing distress response")
    
    # Flow logic - DISTRESS TAKES PRIORITY
    if sounds_unstable:
        # User is distressed - show response based on distress level (SIMPLIFIED 2-LEVEL SYSTEM)
        print(f"📋 PRIORITY: Showing Sunny's {distress_level} distress response")
        
        distress_response = distress_responses[distress_level]
        
        if distress_level == 'high':
            # HIGH distress - immediate empathy + structured support menu
            response = f"""{distress_response['opening']}

{distress_response['context']}

I can support you with:

1️⃣ Understanding what you're feeling
2️⃣ Coping strategies that can help right now  
3️⃣ Connecting you to professional support in Singapore
4️⃣ Just being here to listen - whatever you need

Type a number (1-4), or just tell me more about what's happening. I'm not going anywhere. 😊"""

        else:  # mild distress
            # MILD distress - friendly, casual, bullet-point style
            response = f"""{distress_response['opening']}

{distress_response['context']}

What would you like help with?
• Understanding emotions
• Coping strategies  
• Support services in Singapore
• Or just talk - I'm a good listener!

What's on your mind today?"""
        
        state["messages"].append(response)
        state["current_agent"] = "complete"
        return state
        
    elif selected_service:
        # User selected a service - provide relevant info
        print(f"💡 Providing info about: {selected_service['topic']}")
        
        # Get context with optional re-ranking
        raw_context = get_relevant_context(selected_service['topic'], n_results=4)
        
        # Re-rank if available (improves relevance)
        if RERANKER_AVAILABLE:
            # Convert context string to document list for re-ranking
            docs = [{"text": raw_context, "source": "knowledge_base"}]
            reranked_docs = rerank_documents(
                query=selected_service['topic'],
                documents=docs,
                document_key="text"
            )
            info_context = reranked_docs[0]["text"] if reranked_docs else raw_context
            print("🔄 Re-ranking applied to context")
        else:
            info_context = raw_context
        
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
        
    else:
        # Normal conversation - be friendly and supportive (VERY brief)
        print("💬 Sunny's casual conversation mode")
        
        # Build context including external context (assessment suggestions)
        context_parts = [f'User said: "{query}"']
        if external_context:
            context_parts.append(external_context)
            print("🎯 Including external context (assessment suggestion)")
        
        full_context = '\n\n'.join(context_parts)
        
        # Check if we're suggesting an assessment OR have assessment results to discuss
        is_assessment_suggestion = external_context and "ASSESSMENT_SUGGESTION" in external_context
        has_assessment_results = external_context and "assessment" in external_context.lower() and "findings:" in external_context
        
        if has_assessment_results and not is_assessment_suggestion:
            # User has assessment results - provide overview and suggestions
            prompt = build_sunny_prompt(
                agent_type='information',
                context=full_context,
                specific_instructions=f"""The user has recently completed an assessment and is now chatting with you. Based on their results, provide:

1. A warm greeting acknowledging they completed the assessment
2. A simple, empathetic overview of their results (be gentle, not clinical)
3. 2-3 practical suggestions based on their results
4. Reassurance and offer to talk more about specific areas

Assessment context: {external_context}

Guidelines:
- Be warm and supportive, not clinical
- Don't repeat exact scores unless relevant
- Focus on what they can do to feel better
- Acknowledge their courage in taking the assessment
- Keep it conversational and caring

Your supportive response as Sunny:"""
            )
        elif is_assessment_suggestion:
            prompt = build_sunny_prompt(
                agent_type='information',
                context=full_context,
                specific_instructions=f"""The user has given several vague responses and might benefit from a self-assessment. Respond warmly as Sunny and suggest they try the self-assessment tool to better understand their mental health.

{external_context}

Be supportive and explain how the assessment could help them. End with encouraging them to click the Assessment tab or take the DASS-21 assessment.

Your supportive response as Sunny:"""
            )
        else:
            prompt = build_sunny_prompt(
                agent_type='information',
                context=full_context,
                specific_instructions=f"""If this is about mental health, wellbeing, or emotions: Respond as Sunny with warmth and support in 1-2 SHORT sentences using phrases like: {', '.join(sunny['validation_phrases'][:2])}

If this is NOT about mental health: Use Sunny's redirect: "{sunny['redirect_template']}"

Your warm response as Sunny:"""
            )
    
        try:
            response = llm.invoke(prompt).content.strip()
            
            # Only apply hard limit for normal responses, not assessment responses or suggestions
            if not is_assessment_suggestion and not has_assessment_results:
                # VERY hard limit - max 2 sentences for casual conversation
                sentences = [s.strip() for s in response.split('.') if s.strip()]
                response = '. '.join(sentences[:2]) + '.' if sentences else "I'm here for you. What's on your mind?"
            
        except Exception as e:
            print(f"Information agent error: {e}")
            response = f"{sunny['validation_phrases'][0]}. What's on your mind? 💙"
        
        state["messages"].append(response)
        state["current_agent"] = "complete"
        return state