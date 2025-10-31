"""
AI Mental Health Agent - Simplified LangGraph Multi-Agent Application
Main application implementing LangGraph workflow with specialized mental health agents.
This version works without sentence-transformers for Python 3.13 compatibility.
"""

import os
from typing import TypedDict, Annotated, Sequence, Literal
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
import chromadb

# Load environment
load_dotenv()

# Crisis keywords for immediate intervention
CRISIS_KEYWORDS = [
    "kill myself", "want to die", "end it all", "commit suicide",
    "hurt myself", "cut myself", "self harm", "not worth living",
    "better off dead", "end my life", "take my own life",
    "no reason to live", "can't go on", "suicide", "suicidal"
]

class AgentState(TypedDict):
    """State for the mental health support agent workflow."""
    messages: Annotated[Sequence[dict], add_messages]
    user_query: str
    next_node: str
    crisis_detected: bool
    assessment_step: int
    assessment_data: dict
    routing_confidence: float
    retrieved_context: str

def initialize_system():
    """Initialize LLM and ChromaDB components."""
    print("Initializing AI Mental Health Support Agent with ChromaDB...")
    
    # Initialize LLM
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables. Please check your .env file.")
    
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
    print("✅ LLM initialized (Groq with Llama 3.3 70B)")
    
    # Initialize ChromaDB
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    print("✅ ChromaDB client initialized")
    
    # Load or create collections
    vectorstores = load_chroma_collections(chroma_client)
    
    return llm, vectorstores

def load_chroma_collections(chroma_client):
    """Load or create ChromaDB collections for each knowledge category."""
    collections = {}
    categories = [
        "mental_health_info",
        "singapore_resources", 
        "coping_strategies",
        "dass21_guidelines",
        "crisis_protocols"
    ]
    
    for category in categories:
        try:
            # Try to get existing collection
            collection = chroma_client.get_collection(name=category)
            collections[category] = collection
            print(f"✅ Loaded existing collection: {category}")
        except:
            # Create new collection if it doesn't exist
            collection = chroma_client.create_collection(name=category)
            collections[category] = collection
            print(f"🔄 Created new collection: {category}")
            
            # Populate with basic data
            populate_collection(collection, category)
    
    return collections

def populate_collection(collection, category):
    """Populate ChromaDB collection with knowledge base content."""
    data_path = f"./data/{category}"
    
    if not os.path.exists(data_path):
        print(f"⚠️ Data directory not found: {data_path}")
        return
    
    documents = []
    metadatas = []
    ids = []
    
    for filename in os.listdir(data_path):
        if filename.endswith('.txt'):
            filepath = os.path.join(data_path, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    
                    # Split content into chunks
                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=200
                    )
                    chunks = text_splitter.split_text(content)
                    
                    # Add chunks to collection data
                    for i, chunk in enumerate(chunks):
                        documents.append(chunk)
                        metadatas.append({
                            "source": filename,
                            "category": category,
                            "chunk_id": i
                        })
                        ids.append(f"{category}_{filename}_{i}")
                        
            except Exception as e:
                print(f"⚠️ Error reading {filepath}: {e}")
    
    if documents:
        try:
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✅ Added {len(documents)} documents to {category}")
        except Exception as e:
            print(f"⚠️ Error adding documents to {category}: {e}")

def query_chroma_collection(collections, category, query, n_results=3):
    """Query ChromaDB collection for relevant documents."""
    if category not in collections:
        return "No relevant information found."
    
    try:
        results = collections[category].query(
            query_texts=[query],
            n_results=n_results
        )
        
        if results['documents'] and results['documents'][0]:
            # Combine the retrieved documents
            context = "\n\n".join(results['documents'][0])
            return context
        else:
            return "No relevant information found."
            
    except Exception as e:
        print(f"⚠️ Error querying {category}: {e}")
        return "No relevant information found."

def detect_crisis(query: str) -> bool:
    """Detect crisis situations in user query."""
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in CRISIS_KEYWORDS)

def get_crisis_resources() -> str:
    """Return immediate crisis resources."""
    return """
🚨 IMMEDIATE HELP AVAILABLE 🚨

If you're in immediate danger, please contact:
• Emergency Services: 995 (Singapore)
• Samaritans of Singapore: 1767 (24/7)
• Institute of Mental Health Emergency: 6389-2222

You are not alone. Help is available right now.

Online Support:
• SOS (Samaritans): Call 1767 or visit sos.org.sg
• IMH CHAT (16-30 years): 6493-6500/6501
• Silver Ribbon Suicide Prevention: suicideprevention.sg

Remember: This crisis will pass. You matter. There are people who want to help you.
"""

def router_agent(state: AgentState) -> dict:
    """Route user queries to appropriate agents."""
    query = state["user_query"]
    
    # Check for crisis first
    if detect_crisis(query):
        return {
            "next_node": "crisis_agent",
            "crisis_detected": True,
            "routing_confidence": 1.0
        }
    
    # Simple keyword-based routing (without embeddings)
    query_lower = query.lower()
    
    if any(word in query_lower for word in ["assess", "test", "scale", "dass", "questionnaire"]):
        return {"next_node": "assessment_agent", "routing_confidence": 0.8}
    elif any(word in query_lower for word in ["help", "service", "doctor", "therapist", "where"]):
        return {"next_node": "resource_agent", "routing_confidence": 0.7}
    else:
        return {"next_node": "info_agent", "routing_confidence": 0.6}

def crisis_agent(state: AgentState) -> dict:
    """Handle crisis situations immediately."""
    llm, vectorstores = initialize_system()
    
    crisis_prompt = f"""
You are a crisis intervention specialist. The user has expressed thoughts that may indicate a mental health crisis.

User message: {state['user_query']}

IMPORTANT: Always provide immediate crisis resources and emotional support. Be empathetic but direct.

Provide:
1. Immediate validation of their feelings
2. Crisis hotline numbers and resources
3. Encourage immediate professional help
4. Reassurance that help is available

Be warm, caring, and non-judgmental while emphasizing safety.
"""
    
    try:
        response = llm.invoke(crisis_prompt)
        crisis_resources = get_crisis_resources()
        
        return {
            "messages": [{"role": "assistant", "content": f"{response.content}\n\n{crisis_resources}"}],
            "crisis_detected": True
        }
    except Exception as e:
        return {
            "messages": [{"role": "assistant", "content": f"I'm concerned about you and want to help. {get_crisis_resources()}"}],
            "crisis_detected": True
        }

def info_agent(state: AgentState) -> dict:
    """Provide mental health information using ChromaDB context."""
    llm, vectorstores = initialize_system()
    
    # Retrieve relevant context from ChromaDB
    context = query_chroma_collection(vectorstores, "mental_health_info", state['user_query'])
    coping_context = query_chroma_collection(vectorstores, "coping_strategies", state['user_query'])
    
    info_prompt = f"""
You are a knowledgeable mental health educator. Use the following context to provide helpful, evidence-based information.

User question: {state['user_query']}

Relevant information from knowledge base:
{context}

Coping strategies context:
{coping_context}

Provide:
1. Clear, accurate information based on the context
2. Evidence-based strategies when appropriate
3. Encouragement to seek professional help for serious concerns
4. Normalize mental health discussions

Be supportive, informative, and professional. Avoid diagnosing or providing medical advice.
"""
    
    try:
        response = llm.invoke(info_prompt)
        return {"messages": [{"role": "assistant", "content": response.content}]}
    except Exception as e:
        return {"messages": [{"role": "assistant", "content": "I'd be happy to help with mental health information. Could you please rephrase your question?"}]}

def resource_agent(state: AgentState) -> dict:
    """Connect users with mental health resources using ChromaDB context."""
    llm, vectorstores = initialize_system()
    
    # Retrieve relevant Singapore resources from ChromaDB
    context = query_chroma_collection(vectorstores, "singapore_resources", state['user_query'])
    
    resource_prompt = f"""
You are a Singapore mental health resource specialist. Use the following context to provide helpful resource information.

User question: {state['user_query']}

Singapore mental health resources from knowledge base:
{context}

Provide:
1. Specific Singapore mental health services relevant to their query
2. Contact information and addresses
3. Eligibility criteria and costs where applicable
4. How to access these services
5. Emergency contacts if needed

Be practical, specific, and helpful. Focus on actionable next steps.
"""
    
    try:
        response = llm.invoke(resource_prompt)
        return {"messages": [{"role": "assistant", "content": response.content}]}
    except Exception as e:
        # Fallback to basic resources if LLM fails
        basic_resources = """
Singapore Mental Health Resources:

🚨 **Emergency**: 995
📞 **Crisis Support**: SOS 1767 (24/7)
🏥 **IMH**: 6389-2000
🌟 **CHAT** (16-30 years): 6493-6500/6501

Visit your nearest polyclinic for mental health services or contact IMH directly.
"""
        return {"messages": [{"role": "assistant", "content": basic_resources}]}

def assessment_agent(state: AgentState) -> dict:
    """Guide users through mental health assessment using ChromaDB context."""
    llm, vectorstores = initialize_system()
    
    # Retrieve relevant DASS-21 and assessment context from ChromaDB
    context = query_chroma_collection(vectorstores, "dass21_guidelines", state['user_query'])
    
    assessment_prompt = f"""
You are a mental health assessment specialist. Use the following context to provide helpful assessment information.

User question: {state['user_query']}

Assessment guidelines from knowledge base:
{context}

Provide:
1. Information about appropriate mental health assessment tools
2. What to expect during professional assessments
3. How to prepare for assessments
4. Where to get professional assessments in Singapore
5. Limitations of self-assessment tools

Be informative and encouraging while emphasizing the importance of professional evaluation.
"""
    
    try:
        response = llm.invoke(assessment_prompt)
        return {"messages": [{"role": "assistant", "content": response.content}]}
    except Exception as e:
        # Fallback assessment information
        fallback_info = """
Mental Health Assessment Information:

🔍 **Professional Assessment Recommended**
For proper mental health assessment, please contact:
- IMH: 6389-2000 
- CHAT (ages 16-30): 6493-6500/6501
- Your family doctor

Assessment tools like DASS-21 can provide insights but should be interpreted by professionals.
"""
        return {"messages": [{"role": "assistant", "content": fallback_info}]}

def create_workflow():
    """Create the LangGraph workflow."""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("router", router_agent)
    workflow.add_node("crisis_agent", crisis_agent)
    workflow.add_node("info_agent", info_agent)
    workflow.add_node("resource_agent", resource_agent)
    workflow.add_node("assessment_agent", assessment_agent)
    
    # Set entry point
    workflow.set_entry_point("router")
    
    # Add routing logic
    def route_after_router(state: AgentState) -> str:
        return state["next_node"]
    
    workflow.add_conditional_edges(
        "router",
        route_after_router,
        {
            "crisis_agent": "crisis_agent",
            "info_agent": "info_agent", 
            "resource_agent": "resource_agent",
            "assessment_agent": "assessment_agent"
        }
    )
    
    # All agents end the workflow
    workflow.add_edge("crisis_agent", END)
    workflow.add_edge("info_agent", END)
    workflow.add_edge("resource_agent", END)
    workflow.add_edge("assessment_agent", END)
    
    return workflow.compile()

def run_mental_health_agent():
    """Main function to run the mental health agent."""
    try:
        # Initialize system
        llm, vectorstores = initialize_system()
        
        # Create workflow
        app = create_workflow()
        print("✅ LangGraph workflow compiled successfully")
        
        print("\n🤖 AI Mental Health Support Agent Ready!")
        print("Type 'quit' to exit")
        print("=" * 50)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Take care! Remember, help is always available when you need it.")
                break
                
            if not user_input:
                print("Please enter your question or concern.")
                continue
            
            # Create initial state
            initial_state = {
                "messages": [{"role": "user", "content": user_input}],
                "user_query": user_input,
                "next_node": "",
                "crisis_detected": False,
                "assessment_step": 0,
                "assessment_data": {},
                "routing_confidence": 0.0,
                "retrieved_context": ""
            }
            
            try:
                # Run the workflow
                result = app.invoke(initial_state)
                
                # Display response
                if result["messages"]:
                    assistant_message = result["messages"][-1]["content"]
                    print(f"\nAssistant: {assistant_message}")
                
            except Exception as e:
                print(f"\nI apologize, but I encountered an error. Please try rephrasing your question.")
                print("If you're in crisis, please contact emergency services (995) or SOS (1767) immediately.")
                
    except KeyboardInterrupt:
        print("\n\nGoodbye! Remember, support is always available when you need it.")
    except Exception as e:
        print(f"Error initializing system: {e}")
        print("Please check your .env file and ensure GROQ_API_KEY is set.")

if __name__ == "__main__":
    run_mental_health_agent()