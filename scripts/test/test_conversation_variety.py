"""
Test script to check conversation variety in distress responses
"""

import sys
sys.path.append('.')

from agent.router_agent import router_node, AgentState, detect_distress_level
from agent.information_agent import information_agent_node
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Mock ChromaDB context function
def mock_get_relevant_context(query, n_results=3):
    return "Mock mental health context about coping strategies and support."

# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)

def test_conversation_variety():
    """Test how the system responds to different distress expressions"""
    
    # Test cases with different distress levels
    test_cases = [
        ("i am sad", "MILD distress - simple sadness"),
        ("I AM SAD!!!", "HIGH distress - caps and punctuation"),
        ("i dont feel good", "HIGH distress - specific phrase"),
        ("feeling down", "MILD distress - feeling down"),
        ("I'm struggling", "MILD distress - struggling"),
        ("I'm really really sad and can't cope", "HIGH distress - multiple keywords"),
    ]
    
    print("="*80)
    print("🧪 CONVERSATION VARIETY TEST")
    print("="*80)
    
    for query, description in test_cases:
        print(f"\n🔍 Testing: \"{query}\" ({description})")
        print("-" * 60)
        
        # Detect distress level
        distress_level, score = detect_distress_level(query)
        print(f"📊 Distress Level: {distress_level.upper()}")
        
        # Create state
        state = AgentState(
            current_query=query,
            messages=[],
            current_agent="router",
            crisis_detected=False,
            context="",
            distress_level=""
        )
        
        # Route through router
        state = router_node(state, llm, mock_get_relevant_context)
        print(f"🧭 Routed to: {state['current_agent'].upper()}")
        
        # If routed to information agent, get response
        if state['current_agent'] == 'information':
            state = information_agent_node(state, llm, mock_get_relevant_context)
            response = state['messages'][-1] if state['messages'] else "No response"
            print(f"💬 Response Preview: {response[:100]}...")
        
        print("\n" + "="*60)

if __name__ == "__main__":
    test_conversation_variety()