"""
Information Agent - Mental health education with evidence-based knowledge
"""

from typing import TypedDict, List
import os
from langchain_groq import ChatGroq
from .sunny_persona import get_sunny_persona, get_distress_responses, build_sunny_prompt

# Optional re-ranker import (can be disabled via env)
try:
    from .reranker import rerank_documents
    RERANKER_AVAILABLE = True
except ImportError:
    RERANKER_AVAILABLE = False
    def rerank_documents(query, documents, **kwargs):
        """Fallback when re-ranker not available"""
        return documents

# Final toggle: only use if both available AND explicitly enabled
USE_RERANKER = (
    os.getenv("RERANKER_ENABLED", "false").lower() == "true"
) and RERANKER_AVAILABLE


# ============================================================================
# CACHED ANSWERS - Instant responses for common queries (no LLM needed)
# ============================================================================
COMMON_QUERIES = {
    'what is anxiety': {
        'answer': """Anxiety is your body's natural response to stress - it's that worried or nervous feeling. 💙

Common signs:
• Racing thoughts
• Restlessness
• Physical tension

It's very common, and there are ways to manage it! Want to know more about coping strategies?""",
        'keywords': ['what is anxiety', 'define anxiety', 'anxiety definition', 'what does anxiety mean']
    },
    'what is depression': {
        'answer': """Depression is more than just feeling sad - it's a persistent low mood that affects daily life. 💙

Common signs:
• Feeling down most days
• Loss of interest in activities
• Changes in sleep or appetite
• Fatigue

You're not alone in this. Want to explore some support options?""",
        'keywords': ['what is depression', 'define depression', 'depression definition', 'what does depression mean']
    },
    'what is stress': {
        'answer': """Stress is your body and mind's reaction to challenges or demands. 💙

It can show up as:
• Feeling overwhelmed
• Difficulty concentrating
• Physical tension
• Sleep issues

Some stress is normal, but I can help you learn ways to manage it better! Want some tips?""",
        'keywords': ['what is stress', 'define stress', 'stress definition', 'what does stress mean']
    },
    'breathing exercise': {
        'answer': """Here's a simple breathing exercise you can try right now: 🌬️

**Box Breathing (4-4-4-4):**
1. Breathe in for 4 counts
2. Hold for 4 counts
3. Breathe out for 4 counts
4. Hold for 4 counts
5. Repeat 3-4 times

This really helps calm your nervous system. Give it a try! 😊""",
        'keywords': ['breathing exercise', 'how to breathe', 'breathing technique', 'deep breathing']
    }
}


# ============================================================================
# OFF-TOPIC DETECTION - Pre-LLM filter (saves LLM calls)
# ============================================================================
def is_off_topic(query: str) -> bool:
    """
    Check if query is off-topic BEFORE LLM call.
    Returns True if query is clearly not about mental health.
    """
    query_lower = query.lower().strip()
    
    # Mental health keywords - if any present, likely on-topic
    mental_health_keywords = [
        'feel', 'feeling', 'emotion', 'anxiety', 'stress', 'depress', 'sad', 'worry',
        'mental', 'health', 'wellbeing', 'cope', 'help', 'support', 'lonely', 'tired',
        'overwhelm', 'difficult', 'hard', 'struggle', 'hurt', 'pain', 'upset', 'angry',
        'scared', 'afraid', 'nervous', 'panic', 'mood', 'sleep', 'therapy', 'counseling'
    ]
    
    if any(keyword in query_lower for keyword in mental_health_keywords):
        return False  # On-topic
    
    # Off-topic indicators (general knowledge, unrelated topics)
    off_topic_patterns = [
        'weather', 'temperature', 'forecast', 'rain', 'sunny',
        'recipe', 'cook', 'food', 'restaurant', 'eat',
        'movie', 'film', 'tv show', 'actor', 'actress',
        'sports', 'football', 'soccer', 'basketball',
        'news', 'politics', 'election', 'president',
        'stock', 'market', 'investment', 'money',
        'math', 'calculate', 'equation', 'solve',
        'history', 'geography', 'science',
        'translate', 'language',
        'joke', 'funny', 'entertainment'
    ]
    
    # If query is very short (1-2 words) and has off-topic pattern, likely off-topic
    words = query_lower.split()
    if len(words) <= 3 and any(pattern in query_lower for pattern in off_topic_patterns):
        return True
    
    return False


def get_cached_answer(query: str) -> str:
    """
    Check if query matches a cached common answer.
    Returns cached answer or empty string if no match.
    """
    query_lower = query.lower().strip()
    
    for topic, data in COMMON_QUERIES.items():
        if any(keyword in query_lower for keyword in data['keywords']):
            return data['answer']
    
    return ""


class AgentState(TypedDict):
    current_query: str
    messages: List[str]
    current_agent: str
    crisis_detected: bool
    context: str
    distress_level: str  # 'high', 'moderate', 'mild', or 'none'


def information_agent_node(state: AgentState, llm: ChatGroq, get_relevant_context) -> AgentState:
    """RAG-enhanced information agent with Sunny's personality - OPTIMIZED."""
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
    
    # ========================================================================
    # OPTIMIZATION 1: Check cached answers first (instant response, no LLM)
    # ========================================================================
    cached_answer = get_cached_answer(query)
    if cached_answer and distress_level == 'none':
        print("⚡ CACHED ANSWER: Returning instant response (no LLM call)")
        state["messages"].append(cached_answer)
        state["current_agent"] = "complete"
        return state
    
    # ========================================================================
    # OPTIMIZATION 2: Off-topic detection (skip LLM for unrelated queries)
    # ========================================================================
    if is_off_topic(query) and distress_level == 'none':
        print("🚫 OFF-TOPIC DETECTED: Returning redirect (no LLM call)")
        state["messages"].append(sunny['redirect_template'])
        state["current_agent"] = "complete"
        return state
    
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
        
        # Re-rank if enabled
        if USE_RERANKER:
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
        
        # SIMPLIFIED PROMPT - removed examples and lengthy instructions
        prompt = build_sunny_prompt(
            agent_type='information',
            context=f"Topic: {selected_service['name']}\n\nKnowledge: {info_context}",
            specific_instructions="Provide ONE actionable tip (1-2 sentences). Be warm and supportive."
        )
        
        try:
            # Generate deterministic seed for consistent responses
            import hashlib
            query_seed = int(hashlib.md5(query.lower().strip().encode()).hexdigest()[:8], 16)
            
            response = llm.invoke(
                prompt,
                config={"configurable": {"seed": query_seed}}
            ).content.strip()
            
            # Hard limit - only first 2 sentences
            sentences = [s.strip() for s in response.split('.') if s.strip()]
            if len(sentences) > 2:
                response = '. '.join(sentences[:2]) + '.'
            
            # Add formatting for readability
            response = f"{response}\n\n💬 *Want to know more? Just ask!*"
            
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
        
        # Check if we're suggesting an assessment
        is_assessment_suggestion = external_context and "ASSESSMENT_SUGGESTION" in external_context
        
        if is_assessment_suggestion:
            # SIMPLIFIED PROMPT - removed example responses
            prompt = build_sunny_prompt(
                agent_type='information',
                context=full_context,
                specific_instructions="Suggest the DASS-21 assessment warmly. Explain how it could help them understand their mental health."
            )
        else:
            # SIMPLIFIED PROMPT - removed lengthy instructions
            prompt = build_sunny_prompt(
                agent_type='information',
                context=full_context,
                specific_instructions="Respond warmly in 1-2 SHORT sentences."
            )
    
        try:
            # Generate deterministic seed for consistent responses
            import hashlib
            query_seed = int(hashlib.md5(query.lower().strip().encode()).hexdigest()[:8], 16)
            
            response = llm.invoke(
                prompt,
                config={"configurable": {"seed": query_seed}}
            ).content.strip()
            
            # Only apply hard limit for normal responses, not assessment suggestions
            if not is_assessment_suggestion:
                # VERY hard limit - max 2 sentences
                sentences = [s.strip() for s in response.split('.') if s.strip()]
                response = '. '.join(sentences[:2]) + '.' if sentences else "I'm here for you. What's on your mind?"
            
        except Exception as e:
            print(f"Information agent error: {e}")
            response = f"{sunny['validation_phrases'][0]}. What's on your mind? 💙"
        
        state["messages"].append(response)
        state["current_agent"] = "complete"
        return state