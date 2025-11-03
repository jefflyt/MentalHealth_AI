"""
Resource Agent - Singapore mental health services and support
"""

from typing import TypedDict, List
from langchain_groq import ChatGroq

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


def resource_agent_node(state: AgentState, llm: ChatGroq, get_relevant_context) -> AgentState:
    """RAG-enhanced resource agent for Singapore services."""
    query = state["current_query"]
    conversation_history = state.get("messages", [])
    
    print("\n" + "="*60)
    print("🏥 [RESOURCE AGENT ACTIVATED]")
    print(f"📝 Query: {query}")
    print("="*60)
    
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
            print(f"🔍 Detected specific service: {specific_service}")
            break
    
    # Check if asking what help is available or general help request
    asking_options = any(word in query.lower() for word in ['what', 'where', 'help', 'support', 'available', 'options', 'need'])
    
    if asking_options:
        print("📋 User asking for available options")
    
    # If just general "help" or "need help" - show warm, complete response
    if asking_options and not specific_service:
        print("💙 Showing warm support message with resources")
        response = """Hey, I'm Sunny, and I'm here to support you. 💙 😊

**Immediate Help in Singapore:**

📞 **SOS Hotline: 1767** (24/7, free)
   - Talk to someone anytime

🏥 **IMH Helpline: 6389-2222** (24/7)
   - Institute of Mental Health

💬 **CHAT: 6493-6500** (Ages 16-30)
   - Free mental health check & support

What would you like to know more about?"""
        
        state["messages"].append(response)
        state["current_agent"] = "complete"
        return state
    
    if specific_service:
        # Provide specific service info with pre-written, warm responses
        print(f"💡 Providing specific info about: {specific_service}")
        
        # Pre-written responses for common services (warm and complete)
        service_responses = {
            'CHAT services': """**CHAT (Community Health Assessment Team)** 💙

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

            'IMH services': """**Institute of Mental Health (IMH)** 🏥

Singapore's specialist psychiatric hospital:

📞 **24/7 Helpline: 6389-2222**
🚨 **Emergency: 6389-2222**
📍 **Location: Buangkok Green Medical Park**

**Services:**
✓ Psychiatric care
✓ Counseling
✓ Crisis intervention
✓ Inpatient & outpatient care

Professional help is available anytime.""",

            'crisis hotlines': """**Crisis Hotlines in Singapore** 📞

**Always Available (24/7):**

📞 **SOS: 1767** (Free, confidential)
   - Emotional support anytime

📞 **IMH: 6389-2222**
   - Mental health emergency

🚨 **Emergency: 999 or 995**
   - Life-threatening situations

You don't have to face this alone. Please reach out."""
        }
        
        # Use pre-written response if available, otherwise generate
        if specific_service in service_responses:
            response = service_responses[specific_service]
        else:
            # Get context with optional re-ranking
            raw_context = get_relevant_context(f"Singapore {specific_service}", n_results=4)
            
            # Re-rank if available (improves relevance for Singapore services)
            if RERANKER_AVAILABLE:
                docs = [{"text": raw_context, "source": "knowledge_base"}]
                reranked_docs = rerank_documents(
                    query=f"Singapore {specific_service}",
                    documents=docs,
                    document_key="text"
                )
                resource_context = reranked_docs[0]["text"] if reranked_docs else raw_context
                print("🔄 Re-ranking applied to resource context")
            else:
                resource_context = raw_context
            
            prompt = f"""You are Sunny, a caring digital friend. User needs {specific_service} in Singapore.

{resource_context}

As Sunny, provide this resource with your warm, supportive personality:
• Service name with emoji - make it friendly
• Contact number (clean, no asterisks)  
• 1-2 key points about why it's helpful
• Encouraging closing from a caring friend

Example Sunny style: "Hey! For counseling, I'd recommend [service] 🌟 at [number]. They're really understanding and have helped lots of people. You deserve support! 😊"

Your warm response as Sunny:"""
            
            try:
                response = llm.invoke(prompt).content.strip()
            except Exception as e:
                print(f"LLM error: {e}")
                response = f"I can help you find {specific_service}. Let me know if you need specific contact information."
        
        state["messages"].append(response)
        state["current_agent"] = "complete"
        return state
        
    elif asking_options and len(conversation_history) > 0:
        # Show available services with Sunny's personality
        print("📋 Showing service list")
        response = """Hey! I'm Sunny, and I'd love to help you find the right support 😊

**Mental Health Support in Singapore:** 💙

🔹 **SOS: 1767** - 24/7 emotional support
🔹 **CHAT: 6493-6500** - Youth (16-30) 
🔹 **IMH: 6389-2222** - Professional care

Which one sounds right for you? I'm here to help! 💙"""
        
        state["messages"].append(response)
        state["current_agent"] = "complete"
        return state
        
    else:
        # Ask for details with Sunny's warm personality
        print("💬 Asking user for more details")
        response = "Hey, I'm Sunny! 😊 I can help you find support in Singapore. What kind of help are you looking for? 💙"
    
    state["messages"].append(response)
    state["current_agent"] = "complete"
    return state
