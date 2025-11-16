#!/usr/bin/env python3
"""
AI Mental Health Support Agent with Full RAG Integration
A multi-agent system using LangGraph and ChromaDB for knowledge-grounded responses
"""

import os

# Safety environment flags
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["CHROMA_DISABLE_TELEMETRY"] = "true"

import chromadb
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from typing import TypedDict, List, Dict, Any
from dotenv import load_dotenv

# Simple ConversationBufferMemory replacement (langchaibbn 1.0+ removed memory module)
class ConversationBufferMemory:
    """Simple conversation memory to replace deprecated langchain.memory.ConversationBufferMemory"""
    def __init__(self, memory_key="chat_history", return_messages=True, output_key="output"):
        self.memory_key = memory_key
        self.return_messages = return_messages
        self.output_key = output_key
        self.chat_history = []
    
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, Any]):
        """Save conversation context"""
        user_message = {"type": "human", "content": inputs.get("input", "")}
        ai_message = {"type": "ai", "content": outputs.get(self.output_key, "")}
        self.chat_history.append(user_message)
        self.chat_history.append(ai_message)
    
    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Load memory variables"""
        if self.return_messages:
            # Return as message objects
            class Message:
                def __init__(self, msg_type, content):
                    self.type = msg_type
                    self.content = content
            
            messages = [Message(msg["type"], msg["content"]) for msg in self.chat_history]
            return {self.memory_key: messages}
        else:
            return {self.memory_key: self.chat_history}
    
    def clear(self):
        """Clear conversation history"""
        self.chat_history = []

# Import chains and tools
from chains import create_rag_chain, create_router_chain, create_crisis_detection_chain
from tools import (
    create_assessment_tool,
    create_resource_finder_tool,
    create_crisis_hotline_tool,
    create_breathing_exercise_tool,
    create_mood_tracker_tool
)

# Import modular agents
from agent import (
    router_node,
    crisis_intervention_node,
    information_agent_node,
    resource_agent_node,
    assessment_agent_node,
    human_escalation_node
)

# Load environment variables
load_dotenv()

# Initialize ChromaDB with LangChain Retriever
chroma_client = chromadb.PersistentClient(path="./data/chroma_db")

# Global embeddings instance - MUST use remote API only (no local models)
embeddings = None

def get_embeddings():
    """Get remote HuggingFace API embeddings.
    
    Uses HuggingFace Inference API - NO local models, NO ONNX downloads.
    Requires HUGGINGFACE_API_TOKEN environment variable.
    """
    global embeddings
    if embeddings is not None:
        return embeddings
    
    hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
    if not hf_token:
        raise RuntimeError(
            "HUGGINGFACE_API_TOKEN is required for remote embeddings. "
            "Get your token at https://huggingface.co/settings/tokens"
        )
    
    # Use HuggingFace Inference API (remote only - no local model downloads)
    embeddings = HuggingFaceEndpointEmbeddings(
        model="sentence-transformers/all-MiniLM-L6-v2",
        task="feature-extraction",
        huggingfacehub_api_token=hf_token,
    )
    print("✅ Using remote HuggingFace API embeddings (sentence-transformers/all-MiniLM-L6-v2)")
    print("   No local models - embeddings run via HuggingFace Inference API")
    return embeddings

# Global retriever instance
retriever = None

# Global memory store for sessions (session_id -> memory)
session_memories: Dict[str, ConversationBufferMemory] = {}

# Global tools instances
tools = {
    "assessment": None,
    "resource_finder": None,
    "crisis_hotline": None,
    "breathing": None,
    "mood_tracker": None
}

# Global chains
chains = {
    "rag": None,
    "router": None,
    "crisis_detection": None
}


def get_or_create_memory(session_id: str = "default") -> ConversationBufferMemory:
    """Get or create conversation memory for a session."""
    if session_id not in session_memories:
        session_memories[session_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        )
    return session_memories[session_id]


def clear_session_memory(session_id: str = "default"):
    """Clear conversation memory for a session."""
    if session_id in session_memories:
        session_memories[session_id].clear()
        

def get_conversation_history(session_id: str = "default") -> str:
    """Get formatted conversation history."""
    memory = get_or_create_memory(session_id)
    history = memory.load_memory_variables({})
    
    messages = history.get("chat_history", [])
    if not messages:
        return "No previous conversation"
    
    # Format messages
    formatted = []
    for msg in messages:
        role = "User" if msg.type == "human" else "AI"
        formatted.append(f"{role}: {msg.content}")
    
    return "\n".join(formatted)

class AgentState(TypedDict):
    current_query: str
    messages: List[str]
    current_agent: str
    crisis_detected: bool
    context: str  # Added for RAG context
    distress_level: str  # 'high', 'mild', or 'none'
    last_menu_options: List[str]  # Track menu options for stateful turn tracking
    turn_count: int  # Track conversation turns
    session_id: str  # Session identifier for memory
    memory: ConversationBufferMemory  # Conversation memory instance

# Initialize Groq LLM
def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.1,  # Low temperature for consistency with natural variation
        max_tokens=150,  # Limit response length
        api_key=api_key
    )

def generate_query_seed(query: str) -> int:
    """Generate deterministic seed from query for consistent but varied responses."""
    import hashlib
    # Create hash of query text for deterministic seeding
    hash_object = hashlib.md5(query.lower().strip().encode())
    # Convert first 8 bytes to int for seed
    return int(hash_object.hexdigest()[:8], 16)

llm = get_llm()

# RAG Helper Functions
def get_relevant_context(query: str, n_results: int = 3) -> str:
    """Retrieve relevant context using LangChain Retriever."""
    global retriever
    
    if retriever is None:
        return "Retriever not initialized."
    
    try:
        # Use LangChain retriever (invoke method for compatibility)
        docs = retriever.invoke(query)
        
        if docs:
            # Format retrieved documents (limit to n_results)
            context_pieces = []
            for doc in docs[:n_results]:
                source = doc.metadata.get('source', 'Knowledge Base')
                context_pieces.append(f"[Source: {source}]\n{doc.page_content}")
            
            return "\n\n---\n\n".join(context_pieces)
        else:
            return "No specific information found in knowledge base."
    except Exception as e:
        print(f"Retriever query error: {e}")
        return "Unable to retrieve context at this time."

def initialize_chroma():
    """Initialize ChromaDB with LangChain Retriever using remote embeddings."""
    global retriever, chains, tools
    
    try:
        # Get remote embeddings (HuggingFace API - no local models)
        emb = get_embeddings()
        
        # Use LangChain Chroma wrapper with remote embeddings
        vectorstore = Chroma(
            client=chroma_client,
            collection_name="mental_health_kb",
            embedding_function=emb,
            persist_directory="./data/chroma_db"
        )
        
        # Create retriever with search parameters
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        
        print("✅ ChromaDB Retriever loaded from existing collection")
        
        # Initialize chains with retriever and LLM
        chains["rag"] = create_rag_chain(retriever, llm)
        chains["router"] = create_router_chain(llm)
        chains["crisis_detection"] = create_crisis_detection_chain(llm)
        print("✅ Chains initialized (RAG, Router, Crisis Detection)")
        
        # Initialize tools
        tools["assessment"] = create_assessment_tool()
        tools["resource_finder"] = create_resource_finder_tool()
        tools["crisis_hotline"] = create_crisis_hotline_tool()
        tools["breathing"] = create_breathing_exercise_tool()
        tools["mood_tracker"] = create_mood_tracker_tool()
        print("✅ Tools initialized (Assessment, Resource, Crisis, Breathing, Mood)")
        
        return vectorstore
        
    except Exception as e:
        # Create new collection and populate it
        print(f"📚 Creating new ChromaDB collection: {e}")
        
        # Load documents from knowledge directory
        knowledge_dir = "data/knowledge"
        documents = []
        metadatas = []
        ids = []
        
        if os.path.exists(knowledge_dir):
            for root, dirs, files in os.walk(knowledge_dir):
                for file in files:
                    if file.endswith('.txt'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                
                            # Split into chunks for better retrieval
                            chunks = split_into_chunks(content, max_length=1000)
                            
                            for i, chunk in enumerate(chunks):
                                documents.append(chunk)
                                metadatas.append({
                                    'source': file,
                                    'category': os.path.basename(root),
                                    'chunk_id': f"{file}_{i}"
                                })
                                ids.append(f"{file}_{i}")
                                
                        except Exception as e:
                            print(f"Error reading {file_path}: {e}")
        
        # Create vectorstore with documents using remote embeddings
        if documents:
            emb = get_embeddings()
            vectorstore = Chroma.from_texts(
                texts=documents,
                embedding=emb,
                metadatas=metadatas,
                ids=ids,
                persist_directory="./data/chroma_db",
                collection_name="mental_health_kb"
            )
            
            # Create retriever
            retriever = vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}
            )
            
            # Initialize chains
            chains["rag"] = create_rag_chain(retriever, llm)
            chains["router"] = create_router_chain(llm)
            chains["crisis_detection"] = create_crisis_detection_chain(llm)
            print("✅ Chains initialized")
            
            # Initialize tools
            tools["assessment"] = create_assessment_tool()
            tools["resource_finder"] = create_resource_finder_tool()
            tools["crisis_hotline"] = create_crisis_hotline_tool()
            tools["breathing"] = create_breathing_exercise_tool()
            tools["mood_tracker"] = create_mood_tracker_tool()
            print("✅ Tools initialized")
            
            print(f"✅ Created ChromaDB with {len(documents)} chunks, Retriever, Chains, and Tools")
        else:
            print("⚠️ No documents found in data directory")
            vectorstore = None
        
        return vectorstore

def split_into_chunks(text: str, max_length: int = 1000) -> List[str]:
    """Split text into chunks for better retrieval."""
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        if len(current_chunk + paragraph) < max_length:
            current_chunk += paragraph + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

# Wrapper functions to pass dependencies to modular agents
def router_wrapper(state: AgentState) -> AgentState:
    """Wrapper for router agent."""
    return router_node(state, llm, get_relevant_context)

def crisis_wrapper(state: AgentState) -> AgentState:
    """Wrapper for crisis intervention agent."""
    return crisis_intervention_node(state, llm, get_relevant_context)

def information_wrapper(state: AgentState) -> AgentState:
    """Wrapper for information agent."""
    return information_agent_node(state, llm, get_relevant_context)

def resource_wrapper(state: AgentState) -> AgentState:
    """Wrapper for resource agent."""
    return resource_agent_node(state, llm, get_relevant_context)

def assessment_wrapper(state: AgentState) -> AgentState:
    """Wrapper for assessment agent."""
    return assessment_agent_node(state, llm, get_relevant_context)

def escalation_wrapper(state: AgentState) -> AgentState:
    """Wrapper for human escalation agent."""
    return human_escalation_node(state, llm, get_relevant_context)

# Create the workflow
def create_workflow():
    """Create the RAG-enhanced LangGraph workflow."""
    workflow = StateGraph(AgentState)
    
    # Add nodes with wrapper functions
    workflow.add_node("router", router_wrapper)
    workflow.add_node("crisis_intervention", crisis_wrapper)
    workflow.add_node("information", information_wrapper)
    workflow.add_node("resource", resource_wrapper)
    workflow.add_node("assessment", assessment_wrapper)
    workflow.add_node("human_escalation", escalation_wrapper)
    
    # Set entry point
    workflow.set_entry_point("router")
    
    # Add conditional edges from router
    def route_to_agent(state):
        return state["current_agent"]
    
    workflow.add_conditional_edges(
        "router",
        route_to_agent,
        {
            "crisis_intervention": "crisis_intervention",
            "information": "information", 
            "resource": "resource",
            "assessment": "assessment",
            "human_escalation": "human_escalation"
        }
    )
    
    # All agents end the workflow
    workflow.add_edge("crisis_intervention", END)
    workflow.add_edge("information", END)
    workflow.add_edge("resource", END)
    workflow.add_edge("assessment", END)
    workflow.add_edge("human_escalation", END)
    
    return workflow.compile()

def check_for_data_updates():
    """Check for new/modified data and perform smart update if needed."""
    try:
        # Import update agent from agent module
        from agent import UpdateAgent
        
        # Get embeddings to pass to update agent
        emb = get_embeddings()
        
        agent = UpdateAgent(
            chroma_client=chroma_client,
            embedding_function=emb
        )
        print("\n🔍 Checking for data updates...")
        
        # Check for changes
        has_changes = agent.check_for_updates()
        
        if has_changes:
            print("🔄 Performing smart update...")
            agent.perform_smart_update()
            print("✅ ChromaDB updated with new data")
            return True
        else:
            return False
            
    except ImportError:
        # Update agent not available, skip check
        return False
    except Exception as e:
        print(f"⚠️  Update check error: {e}")
        return False

def main():
    """Main application with full RAG integration."""
    print("🧠 AI Mental Health Support Agent (RAG-Enhanced)")
    print("=" * 60)
    
    # Check for data updates before initializing
    check_for_data_updates()
    
    # Initialize ChromaDB with Retriever
    try:
        vectorstore = initialize_chroma()
        print("✅ ChromaDB Retriever initialized successfully")
    except Exception as e:
        print(f"❌ ChromaDB initialization error: {e}")
        return
    
    # Test RAG functionality with Retriever
    print("\n🔍 Testing Retriever...")
    test_context = get_relevant_context("CHAT services Singapore youth", n_results=2)
    print("✅ Retriever working")
    
    # Create workflow
    try:
        app = create_workflow()
        print("✅ LangGraph workflow created")
    except Exception as e:
        print(f"❌ Workflow creation error: {e}")
        return
    
    print("\n🤖 Mental Health Support Agent Ready!")
    print("Type 'quit' to exit")
    print("-" * 60)
    
    # Create session memory
    session_id = "cli_session"
    session_memory = get_or_create_memory(session_id)
    
    while True:
        try:
            user_input = input("\n💭 How can I support your mental health today? ")
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n💙 Take care! Remember, support is always available when you need it.")
                break
            
            if not user_input.strip():
                continue
            
            # Initialize state with memory
            initial_state = {
                "current_query": user_input,
                "messages": [],
                "current_agent": "",
                "crisis_detected": False,
                "context": "",
                "distress_level": "none",
                "last_menu_options": [],
                "turn_count": 0,
                "session_id": session_id,
                "memory": session_memory
            }
            
            # Run the workflow with RAG and Memory
            result = app.invoke(initial_state)
            
            # Save interaction to memory
            if result["messages"]:
                response = "\n".join(result["messages"])
                session_memory.save_context(
                    {"input": user_input},
                    {"output": response}
                )
            
            # Display response
            print("\n🤖 AI Mental Health Agent:")
            for message in result["messages"]:
                print(message)
                
        except KeyboardInterrupt:
            print("\n\n💙 Take care! Support is always available.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Let me try to help in a different way...")

if __name__ == "__main__":
    main()