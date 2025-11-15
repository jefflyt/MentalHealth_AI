"""
Resource Agent - Singapore mental health services and support
"""

from typing import TypedDict, List
from langchain_groq import ChatGroq
from .sunny_persona import build_sunny_prompt
import logging
import os

# Configure logger
logger = logging.getLogger(__name__)

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
# INSTANT ANSWERS - Pre-filled vetted responses (no LLM needed)
# ============================================================================
KNOWN_SERVICES = {
    'imh': {
        'response': """**Institute of Mental Health (IMH)** 🏥

Singapore's specialist psychiatric hospital:

📞 **24/7 Helpline: 6389-2222**
🚨 **Emergency: 6389-2222**
📍 **Location: Buangkok Green Medical Park**

**Services:**
✓ Psychiatric care
✓ Counseling
✓ Crisis intervention
✓ Inpatient & outpatient care

Professional help is available anytime. 💙""",
        'keywords': ['imh', 'institute of mental health', 'buangkok', 'psychiatric hospital']
    },
    'sos': {
        'response': """**SOS (Samaritans of Singapore)** 📞

**24/7 Hotline: 1767**

✓ Free, confidential emotional support
✓ Talk to trained volunteers anytime
✓ No judgment, just listening

You're not alone. Call anytime you need to talk. 💙""",
        'keywords': ['sos', 'samaritans', '1767', 'sos hotline', 'samaritans of singapore']
    },
    'chat': {
        'response': """**CHAT (Community Health Assessment Team)** 💙

For young people ages 16-30 in Singapore:

📞 **Call: 6493-6500**
📍 **Walk-in: *SCAPE, Orchard Link**
🕐 **Hours:**
   - Mon-Fri: 1 PM - 9 PM
   - Sat: 10 AM - 4 PM

**Free Services:**
✓ Mental health screening
✓ Brief counseling
✓ Referrals to specialists

You're not alone. They're here to help.""",
        'keywords': ['chat', 'chat services', 'community health assessment', 'scape', '6493-6500']
    },
    'hotline': {
        'response': """**Crisis Hotlines in Singapore** 📞

**Always Available (24/7):**

📞 **SOS: 1767** (Free, confidential)
   - Emotional support anytime

📞 **IMH: 6389-2222**
   - Mental health emergency

🚨 **Emergency: 999 or 995**
   - Life-threatening situations

You don't have to face this alone. Please reach out. 💙""",
        'keywords': ['hotline', 'helpline', 'crisis line', 'emergency number', 'call']
    },
    'therapy': {
        'response': """**Therapy & Counseling in Singapore** 🌟

**Affordable Options:**

💙 **CHAT (16-30): 6493-6500**
   - Free counseling for youth

🏥 **Polyclinics**
   - Subsidized counseling referrals
   - Call your nearest polyclinic

💚 **Family Service Centres**
   - Community-based support
   - Sliding scale fees

Need help finding a therapist? Let me know! 😊""",
        'keywords': ['therapy', 'therapist', 'counseling', 'counselor', 'psychologist']
    },
    'general': {
        'response': """**Mental Health Support in Singapore** 💙

**Immediate Help (24/7):**
📞 **SOS: 1767** - Emotional support
📞 **IMH: 6389-2222** - Mental health care

**Youth Support (16-30):**
📞 **CHAT: 6493-6500** - Free screening & counseling

**Professional Care:**
🏥 **IMH** - Specialist psychiatric hospital
💚 **Polyclinics** - Affordable counseling

What kind of support are you looking for? 😊"""
    }
}


def get_instant_answer(query: str) -> str:
    """
    Check if query matches a known service for instant response.
    Returns pre-filled answer or empty string if no match.
    """
    query_lower = query.lower().strip()
    
    for service_id, service_data in KNOWN_SERVICES.items():
        if service_id == 'general':
            continue  # Skip general, use as fallback
        
        keywords = service_data.get('keywords', [])
        if any(keyword in query_lower for keyword in keywords):
            logger.info(f"⚡ INSTANT ANSWER: Matched '{service_id}' (no LLM call)")
            return service_data['response']
    
    return ""


class AgentState(TypedDict):
    current_query: str
    messages: List[str]
    current_agent: str
    crisis_detected: bool
    context: str


def resource_agent_node(state: AgentState, llm: ChatGroq, get_relevant_context) -> AgentState:
    """RAG-enhanced resource agent for Singapore services - OPTIMIZED."""
    query = state["current_query"]
    conversation_history = state.get("messages", [])
    
    logger.info("="*60)
    logger.info("🏥 [RESOURCE AGENT ACTIVATED]")
    logger.info(f"📝 Query: {query}")
    logger.info("="*60)
    
    # ========================================================================
    # OPTIMIZATION 1: Check for instant answers first (no LLM needed)
    # ========================================================================
    instant_answer = get_instant_answer(query)
    if instant_answer:
        logger.info("⚡ INSTANT ANSWER: Returning pre-filled response (no LLM call)")
        state["messages"].append(instant_answer)
        state["current_agent"] = "complete"
        return state
    
    # ========================================================================
    # OPTIMIZATION 2: Check if asking for general options
    # ========================================================================
    asking_options = any(word in query.lower() for word in ['what', 'where', 'help', 'support', 'available', 'options', 'need'])
    
    if asking_options:
        logger.info("📋 General help request - showing overview")
        response = KNOWN_SERVICES['general']['response']
        state["messages"].append(response)
        state["current_agent"] = "complete"
        return state
    
    # ========================================================================
    # OPTIMIZATION 3: For unknown resources, use template approach
    # ========================================================================
    logger.info("🔍 Unknown resource - using template + minimal LLM")
    
    # Step 1: Retrieve context
    raw_context = get_relevant_context(f"Singapore mental health {query}", n_results=3)
    
    # Step 2: Re-rank if enabled
    if USE_RERANKER:
        docs = [{"text": raw_context, "source": "knowledge_base"}]
        reranked_docs = rerank_documents(
            query=f"Singapore {query}",
            documents=docs,
            document_key="text"
        )
        resource_context = reranked_docs[0]["text"] if reranked_docs else raw_context
        logger.debug("🔄 Re-ranking applied")
    else:
        resource_context = raw_context
    
    # Step 3: Use LLM only to fill in template (MINIMAL PROMPT)
    # Remove example responses, just ask for structured output
    prompt = build_sunny_prompt(
        agent_type="resource",
        context=resource_context,
        specific_instructions=f"""Fill in this template with Singapore resource info:

**[Service Name]** [emoji]

📞 **Contact: [number]**
📍 **Location: [address if available]**

**Key info:**
✓ [1-2 key points only]

Format exactly as shown. Be concise."""
    )
    
    try:
        import hashlib
        query_seed = int(hashlib.md5(query.lower().strip().encode()).hexdigest()[:8], 16)
        
        response = llm.invoke(
            prompt,
            config={"configurable": {"seed": query_seed}}
        ).content.strip()
        
    except Exception as e:
        logger.error(f"LLM error: {e}", exc_info=True)
        # Fallback to general info
        response = KNOWN_SERVICES['general']['response']
    
    state["messages"].append(response)
    state["current_agent"] = "complete"
    return state
