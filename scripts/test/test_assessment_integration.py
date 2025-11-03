"""
Test script to verify assessment result integration with Sunny's chat responses
"""

import sys
sys.path.append('.')

from interface.web.app import build_assessment_context
from agent.information_agent import information_agent_node
from agent.router_agent import router_node, AgentState
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

def test_assessment_integration():
    """Test how Sunny responds to users with assessment results"""
    
    # Sample assessment results
    sample_results = {
        'assessmentType': 'dass21',
        'timestamp': '2025-11-03T10:30:00',
        'scores': {
            'depression': {'level': 'moderate', 'score': 15},
            'anxiety': {'level': 'mild', 'score': 8},
            'stress': {'level': 'normal', 'score': 4}
        }
    }
    
    print("="*80)
    print("🧪 ASSESSMENT INTEGRATION TEST")
    print("="*80)
    
    # Test context building
    context = build_assessment_context(sample_results)
    print(f"\n📊 Assessment Context Built:")
    print(f"{context}")
    print("\n" + "-"*60)
    
    # Test chat response
    user_query = "Hi Sunny"
    
    print(f"\n💬 User says: \"{user_query}\"")
    print(f"🎯 Has assessment results: YES")
    
    # Create state with assessment context
    state = AgentState(
        current_query=user_query,
        messages=[],
        current_agent="router",
        crisis_detected=False,
        context=context,  # Include assessment context
        distress_level=""
    )
    
    # Route through router
    state = router_node(state, llm, mock_get_relevant_context)
    print(f"🧭 Routed to: {state['current_agent'].upper()}")
    
    # If routed to information agent, get response
    if state['current_agent'] == 'information':
        state = information_agent_node(state, llm, mock_get_relevant_context)
        response = state['messages'][-1] if state['messages'] else "No response"
        print(f"\n🌟 Sunny's Response:")
        print(f"{response}")
    
    print("\n" + "="*80)

def test_different_assessment_types():
    """Test responses for different assessment types"""
    
    test_cases = [
        {
            'name': 'DASS-21 with High Anxiety',
            'results': {
                'assessmentType': 'dass21',
                'timestamp': '2025-11-03T10:30:00',
                'scores': {
                    'depression': {'level': 'normal', 'score': 3},
                    'anxiety': {'level': 'severe', 'score': 18},
                    'stress': {'level': 'mild', 'score': 12}
                }
            }
        },
        {
            'name': 'Mood Check - Low Score',
            'results': {
                'assessmentType': 'mood',
                'timestamp': '2025-11-03T10:30:00',
                'averageScore': 1.8
            }
        },
        {
            'name': 'Stress Assessment - High',
            'results': {
                'assessmentType': 'stress',
                'timestamp': '2025-11-03T10:30:00',
                'level': 'high',
                'percentage': 85
            }
        }
    ]
    
    print("\n" + "="*80)
    print("🎭 DIFFERENT ASSESSMENT TYPES TEST")
    print("="*80)
    
    for test_case in test_cases:
        print(f"\n🧪 Testing: {test_case['name']}")
        print("-" * 60)
        
        context = build_assessment_context(test_case['results'])
        print(f"📊 Context: {context[:100]}...")
        
        print(f"💡 Expected: Sunny should provide overview and suggestions for {test_case['results']['assessmentType']}")

if __name__ == "__main__":
    test_assessment_integration()
    test_different_assessment_types()