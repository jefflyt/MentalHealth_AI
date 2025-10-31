#!/usr/bin/env python3
"""
AI Mental Health Support Agent with Full RAG Integration
A multi-agent system using LangGraph and ChromaDB for knowledge-grounded responses
"""

import os
import chromadb
from chromadb.utils import embedding_functions
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from typing import TypedDict, List
from dotenv import load_dotenv

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

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./data/chroma_db")
embedding_function = embedding_functions.DefaultEmbeddingFunction()

class AgentState(TypedDict):
    current_query: str
    messages: List[str]
    current_agent: str
    crisis_detected: bool
    context: str  # Added for RAG context

# Initialize Groq LLM
def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,  # Balanced for consistency
        max_tokens=150,  # Limit response length
        api_key=api_key
    )

llm = get_llm()

# RAG Helper Functions
def get_relevant_context(query: str, n_results: int = 3) -> str:
    """Retrieve relevant context from ChromaDB for RAG."""
    try:
        collection = chroma_client.get_collection("mental_health_kb")
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        if results and results['documents'] and results['documents'][0]:
            # Combine retrieved documents
            context_pieces = []
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                source = metadata.get('source', 'Knowledge Base')
                context_pieces.append(f"[Source: {source}]\n{doc}")
            
            return "\n\n---\n\n".join(context_pieces)
        else:
            return "No specific information found in knowledge base."
    except Exception as e:
        print(f"ChromaDB query error: {e}")
        return "Unable to retrieve context at this time."

def initialize_chroma():
    """Initialize ChromaDB with knowledge base documents."""
    try:
        # Try to get existing collection
        collection = chroma_client.get_collection("mental_health_kb")
        print("✅ ChromaDB collection already exists and loaded")
        return collection
    except:
        # Create new collection and populate it
        print("📚 Creating and populating ChromaDB collection...")
        collection = chroma_client.create_collection(
            name="mental_health_kb",
            embedding_function=embedding_function
        )
        
        # Load documents from knowledge directory
        knowledge_dir = "data/knowledge"
        documents = []
        
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
                                documents.append({
                                    'content': chunk,
                                    'source': file,
                                    'chunk_id': f"{file}_{i}",
                                    'category': os.path.basename(root)
                                })
                        except Exception as e:
                            print(f"Error reading {file_path}: {e}")
        
        # Add documents to ChromaDB
        if documents:
            collection.add(
                documents=[doc['content'] for doc in documents],
                metadatas=[{
                    'source': doc['source'], 
                    'category': doc['category'],
                    'chunk_id': doc['chunk_id']
                } for doc in documents],
                ids=[doc['chunk_id'] for doc in documents]
            )
            print(f"✅ Added {len(documents)} document chunks to ChromaDB")
        else:
            print("⚠️ No documents found in data directory")
        
        return collection

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
        
        agent = UpdateAgent()
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
    
    # Initialize ChromaDB
    try:
        collection = initialize_chroma()
        print("✅ ChromaDB initialized successfully")
    except Exception as e:
        print(f"❌ ChromaDB initialization error: {e}")
        return
    
    # Test RAG functionality
    print("\n🔍 Testing RAG retrieval...")
    test_context = get_relevant_context("CHAT services Singapore youth", n_results=2)
    print("✅ RAG retrieval working")
    
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
    
    while True:
        try:
            user_input = input("\n💭 How can I support your mental health today? ")
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n💙 Take care! Remember, support is always available when you need it.")
                break
            
            if not user_input.strip():
                continue
            
            # Initialize state
            initial_state = {
                "current_query": user_input,
                "messages": [],
                "current_agent": "",
                "crisis_detected": False,
                "context": ""
            }
            
            # Run the workflow with RAG
            result = app.invoke(initial_state)
            
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