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
# DEFAULT: DISABLED for performance on Render free tier
USE_RERANKER = (
    os.getenv("RERANKER_ENABLED", "false").lower() == "true"
) and RERANKER_AVAILABLE

print(f"🔧 Reranker status: {'ENABLED' if USE_RERANKER else 'DISABLED'}")


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


def _invoke_llm_with_timeout(llm, prompt: str, seed: int, max_tokens: int = 256, timeout: int = 40) -> str:
    """Invoke LLM with timeout protection for Render free tier.
    
    Args:
        llm: ChatGroq LLM instance
        prompt: Prompt to send to LLM
        seed: Deterministic seed
        max_tokens: Maximum tokens to generate (default 256 for speed)
        timeout: Timeout in seconds (default 40s)
    
    Returns:
        Generated response text
        
    Raises:
        TimeoutError: If LLM call exceeds timeout
    """
    import signal
    
    def timeout_handler(signum, frame):
        raise TimeoutError(f"LLM call exceeded {timeout}s timeout")
    
    # Set up timeout (Unix-only, won't work on Windows)
    try:
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)
        
        try:
            response = llm.invoke(
                prompt,
                config={
                    "configurable": {"seed": seed},
                    "max_tokens": max_tokens  # Cap tokens for speed
                }
            ).content.strip()
            
            return response
        finally:
            # Cancel timeout
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
            
    except AttributeError:
        # signal.SIGALRM not available (Windows) - just call without timeout
        response = llm.invoke(
            prompt,
            config={
                "configurable": {"seed": seed},
                "max_tokens": max_tokens
            }
        ).content.strip()
        return response


def information_agent_node(state: AgentState, llm: ChatGroq, get_relevant_context) -> AgentState:
    """RAG-enhanced information agent with Sunny's personality - RENDER OPTIMIZED.
    
    Performance optimizations for Render free tier:
    - Detailed timing logs with [INFO_AGENT] prefix
    - Truncate long messages before processing (512 chars max)
    - Cap LLM max_tokens to 256
    - Timeout wrapper around LLM calls (40s max)
    - Retriever k=3 for speed
    """
    import time
    import logging
    
    # Get logger (use app.logger if available, otherwise use print)
    try:
        from flask import current_app
        logger = current_app.logger
    except:
        logger = logging.getLogger(__name__)
    
    agent_start = time.time()
    logger.info("[INFO_AGENT] 🚀 Information agent started")
    
    query = state["current_query"]
    conversation_history = state.get("messages", [])
    distress_level = state.get("distress_level", "none")
    external_context = state.get("context", "")
    
    # OPTIMIZATION: Truncate long queries to avoid expensive embeddings
    original_query_len = len(query)
    if len(query) > 512:
        query = query[:512]
        logger.info(f"[INFO_AGENT] ✂️  Truncated query from {original_query_len} to 512 chars")
    
    # Load Sunny's persona components
    sunny = get_sunny_persona()
    distress_responses = get_distress_responses()
    
    logger.info(f"[INFO_AGENT] 📝 Query: '{query[:50]}...' | Distress: {distress_level}")
    
    # ========================================================================
    # OPTIMIZATION 1: Check cached answers first (instant response, no LLM/DB)
    # ========================================================================
    cached_answer = get_cached_answer(query)
    if cached_answer and distress_level == 'none':
        elapsed = time.time() - agent_start
        logger.info(f"[INFO_AGENT] ⚡ CACHED response returned in {elapsed:.3f}s")
        state["messages"].append(cached_answer)
        state["current_agent"] = "complete"
        return state
    
    # ========================================================================
    # OPTIMIZATION 2: Off-topic detection (skip LLM/DB for unrelated queries)
    # ========================================================================
    if is_off_topic(query) and distress_level == 'none':
        elapsed = time.time() - agent_start
        logger.info(f"[INFO_AGENT] 🚫 OFF-TOPIC detected, redirect in {elapsed:.3f}s")
        state["messages"].append(sunny['redirect_template'])
        state["current_agent"] = "complete"
        return state
    
    # Use distress level from router (SIMPLIFIED 2-LEVEL SYSTEM)
    sounds_unstable = distress_level in ['high', 'mild']
    
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
    
    if query.strip() in ['1', '2', '3', '4']:
        selected_service = agent_services[query.strip()]
        logger.info(f"[INFO_AGENT] ✅ Menu selection: {selected_service['name']}")
    elif not sounds_unstable:
        query_lower = query.lower()
        for service_num, service in agent_services.items():
            if any(keyword in query_lower for keyword in service['keywords']):
                selected_service = service
                logger.info(f"[INFO_AGENT] 🔍 Keyword match: {selected_service['name']}")
                break
    
    # Flow logic - DISTRESS TAKES PRIORITY
    if sounds_unstable:
        # User is distressed - show response based on distress level
        logger.info(f"[INFO_AGENT] 😔 Distress response: {distress_level}")
        
        distress_response = distress_responses[distress_level]
        
        if distress_level == 'high':
            response = f"""{distress_response['opening']}

{distress_response['context']}

I can support you with:

1️⃣ Understanding what you're feeling
2️⃣ Coping strategies that can help right now  
3️⃣ Connecting you to professional support in Singapore
4️⃣ Just being here to listen - whatever you need

Type a number (1-4), or just tell me more about what's happening. I'm not going anywhere. 😊"""
        else:  # mild distress
            response = f"""{distress_response['opening']}

{distress_response['context']}

What would you like help with?
• Understanding emotions
• Coping strategies  
• Support services in Singapore
• Or just talk - I'm a good listener!

What's on your mind today?"""
        
        elapsed = time.time() - agent_start
        logger.info(f"[INFO_AGENT] ✅ Distress menu returned in {elapsed:.3f}s")
        state["messages"].append(response)
        state["current_agent"] = "complete"
        return state
        
    elif selected_service:
        # User selected a service - provide relevant info with RAG
        logger.info(f"[INFO_AGENT] 💡 Selected service: {selected_service['topic']}")
        
        # TIMING: RAG retrieval
        rag_start = time.time()
        logger.info(f"[INFO_AGENT] 🔍 Starting RAG retrieval (k=3)")
        
        # Get context with k=3 for speed on Render
        raw_context = get_relevant_context(selected_service['topic'], n_results=3)
        
        rag_duration = time.time() - rag_start
        logger.info(f"[INFO_AGENT] ✅ RAG retrieval completed in {rag_duration:.3f}s")
        
        # Re-rank if enabled (usually disabled on Render)
        if USE_RERANKER:
            rerank_start = time.time()
            docs = [{"text": raw_context, "source": "knowledge_base"}]
            reranked_docs = rerank_documents(
                query=selected_service['topic'],
                documents=docs,
                document_key="text"
            )
            info_context = reranked_docs[0]["text"] if reranked_docs else raw_context
            rerank_duration = time.time() - rerank_start
            logger.info(f"[INFO_AGENT] 🔄 Re-ranking completed in {rerank_duration:.3f}s")
        else:
            info_context = raw_context
        
        # Build prompt
        prompt = build_sunny_prompt(
            agent_type='information',
            context=f"Topic: {selected_service['name']}\n\nKnowledge: {info_context}",
            specific_instructions="Provide ONE actionable tip (1-2 sentences). Be warm and supportive."
        )
        
        # TIMING: LLM generation with timeout
        llm_start = time.time()
        logger.info("[INFO_AGENT] 🤖 Starting LLM generation (max_tokens=256, timeout=40s)")
        
        try:
            # Generate deterministic seed
            import hashlib
            query_seed = int(hashlib.md5(query.lower().strip().encode()).hexdigest()[:8], 16)
            
            # Call LLM with timeout wrapper
            response = _invoke_llm_with_timeout(
                llm=llm,
                prompt=prompt,
                seed=query_seed,
                max_tokens=256,
                timeout=40
            )
            
            llm_duration = time.time() - llm_start
            logger.info(f"[INFO_AGENT] ✅ LLM generation completed in {llm_duration:.3f}s ({len(response)} chars)")
            
            # Hard limit - only first 2 sentences
            sentences = [s.strip() for s in response.split('.') if s.strip()]
            if len(sentences) > 2:
                response = '. '.join(sentences[:2]) + '.'
            
            response = f"{response}\n\n💬 *Want to know more? Just ask!*"
            
        except TimeoutError:
            logger.error(f"[INFO_AGENT] ⏰ LLM timeout after 40s - using fallback")
            response = f"I can help with {selected_service['name'].lower()}. What would you like to know?"
        except Exception as e:
            logger.error(f"[INFO_AGENT] ❌ LLM error: {e}")
            response = f"I can help with {selected_service['name'].lower()}. What would you like to know?"
        
        elapsed = time.time() - agent_start
        logger.info(f"[INFO_AGENT] ✅ Service response completed in {elapsed:.3f}s")
        state["messages"].append(response)
        state["current_agent"] = "complete"
        return state
        
    else:
        # Normal conversation - be friendly and supportive
        logger.info("[INFO_AGENT] 💬 Casual conversation mode")
        
        # Build context including conversation history and external context
        context_parts = [f'User said: "{query}"']
        
        # Include recent conversation history for context (last 3 exchanges)
        if len(conversation_history) >= 2:
            recent_history = "\n".join(conversation_history[-3:])
            context_parts.append(f"Recent conversation:\n{recent_history}")
        
        if external_context:
            context_parts.append(external_context)
            logger.info("[INFO_AGENT] 🎯 Including external context")
        
        full_context = '\n\n'.join(context_parts)
        
        # Check if we're suggesting an assessment
        is_assessment_suggestion = external_context and "ASSESSMENT_SUGGESTION" in external_context
        
        if is_assessment_suggestion:
            prompt = build_sunny_prompt(
                agent_type='information',
                context=full_context,
                specific_instructions="Suggest the DASS-21 assessment warmly. Explain how it could help them understand their mental health."
            )
        else:
            prompt = build_sunny_prompt(
                agent_type='information',
                context=full_context,
                specific_instructions="Respond naturally based on the conversation context. If user affirmed/agreed to something you offered, provide that help. Keep responses warm and concise (2-3 sentences max)."
            )
    
        # TIMING: LLM generation with timeout
        llm_start = time.time()
        logger.info("[INFO_AGENT] 🤖 Starting LLM generation (max_tokens=256, timeout=40s)")
        
        try:
            import hashlib
            query_seed = int(hashlib.md5(query.lower().strip().encode()).hexdigest()[:8], 16)
            
            # Call LLM with timeout wrapper
            response = _invoke_llm_with_timeout(
                llm=llm,
                prompt=prompt,
                seed=query_seed,
                max_tokens=256,
                timeout=40
            )
            
            llm_duration = time.time() - llm_start
            logger.info(f"[INFO_AGENT] ✅ LLM generation completed in {llm_duration:.3f}s ({len(response)} chars)")
            
            # Apply hard limit for normal responses only
            if not is_assessment_suggestion:
                sentences = [s.strip() for s in response.split('.') if s.strip()]
                response = '. '.join(sentences[:2]) + '.' if sentences else "I'm here for you. What's on your mind?"
            
        except TimeoutError:
            logger.error(f"[INFO_AGENT] ⏰ LLM timeout after 40s - using fallback")
            response = f"{sunny['validation_phrases'][0]}. What's on your mind? 💙"
        except Exception as e:
            logger.error(f"[INFO_AGENT] ❌ LLM error: {e}")
            response = f"{sunny['validation_phrases'][0]}. What's on your mind? 💙"
        
        elapsed = time.time() - agent_start
        logger.info(f"[INFO_AGENT] ✅ Conversation response completed in {elapsed:.3f}s")
        state["messages"].append(response)
        state["current_agent"] = "complete"
        return state