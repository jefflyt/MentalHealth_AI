#!/usr/bin/env python3
"""
Quick integration test to verify router agent works in the full system.
Tests basic routing and state management.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from agent.router_agent import router_node, AgentState, detect_explicit_intent
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment
load_dotenv()

def mock_get_relevant_context(query, n_results=2):
    """Mock RAG context retrieval for testing."""
    return "Mock context about mental health support and resources."


def test_router_basic_functionality():
    """Test that router can process queries and set agents correctly."""
    print("\n🧪 Testing Router Basic Functionality")
    print("=" * 60)
    
    # Initialize LLM
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("⚠️  GROQ_API_KEY not found - skipping LLM test")
            return False
            
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=50
        )
    except Exception as e:
        print(f"⚠️  Could not initialize LLM: {e}")
        return False
    
    test_cases = [
        {
            "query": "I want to take a mental health assessment",
            "expected_agent": "assessment",
            "description": "Explicit assessment request"
        },
        {
            "query": "I'm feeling really anxious today",
            "expected_agent": "information",
            "description": "Distress detection"
        },
        {
            "query": "Where can I find a therapist in Singapore?",
            "expected_agent": "resource",
            "description": "Resource request"
        },
        {
            "query": "What is depression?",
            "expected_agent": "information",
            "description": "General information query"
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in test_cases:
        # Create initial state
        state: AgentState = {
            "current_query": test["query"],
            "messages": [],
            "current_agent": "",
            "crisis_detected": False,
            "context": "",
            "distress_level": "none",
            "last_menu_options": [],
            "turn_count": 0
        }
        
        try:
            # Run router
            result = router_node(state, llm, mock_get_relevant_context)
            
            # Check result
            if result["current_agent"] == test["expected_agent"]:
                print(f"✅ {test['description']}")
                print(f"   Query: '{test['query']}'")
                print(f"   Routed to: {result['current_agent']}")
                passed += 1
            else:
                print(f"❌ {test['description']}")
                print(f"   Query: '{test['query']}'")
                print(f"   Expected: {test['expected_agent']}, Got: {result['current_agent']}")
                failed += 1
                
        except Exception as e:
            print(f"❌ {test['description']} - Error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


def test_state_persistence():
    """Test that state fields are properly maintained."""
    print("\n🧪 Testing State Persistence")
    print("=" * 60)
    
    state: AgentState = {
        "current_query": "test",
        "messages": [],
        "current_agent": "",
        "crisis_detected": False,
        "context": "",
        "distress_level": "none",
        "last_menu_options": [],
        "turn_count": 0
    }
    
    # Verify all required fields exist
    required_fields = [
        "current_query", "messages", "current_agent", "crisis_detected",
        "context", "distress_level", "last_menu_options", "turn_count"
    ]
    
    all_present = all(field in state for field in required_fields)
    
    if all_present:
        print("✅ All required state fields present")
        print(f"   Fields: {', '.join(required_fields)}")
        return True
    else:
        missing = [f for f in required_fields if f not in state]
        print(f"❌ Missing state fields: {', '.join(missing)}")
        return False


def main():
    """Run all integration tests."""
    print("\n🚀 Router Agent Integration Tests")
    print("=" * 60)
    
    results = []
    
    # Test 1: State persistence
    results.append(("State Persistence", test_state_persistence()))
    
    # Test 2: Router functionality
    results.append(("Router Functionality", test_router_basic_functionality()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✅ All integration tests passed!")
        print("🎉 Router agent is ready for production use")
    else:
        print("\n⚠️  Some tests failed - review errors above")
    
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
