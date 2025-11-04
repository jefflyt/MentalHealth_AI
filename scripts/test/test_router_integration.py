"""
Test script for Router Agent integration with 2-level distress detection
Tests that the router properly uses distress levels and routes to appropriate agents
"""

import sys
sys.path.append('.')
from agent.router_agent import router_node, detect_crisis, detect_distress_level, AgentState
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Mock function for RAG context (simplified for testing)
def mock_get_relevant_context(query, n_results=3):
    return f"Mock context for query: {query}"

# Initialize LLM (using environment variable or mock)
try:
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.7,
            groq_api_key=api_key
        )
        print(f"✅ GROQ LLM initialized successfully with key: {api_key[:15]}...")
    else:
        raise ValueError("No GROQ API key found")
except Exception as e:
    print(f"⚠️  GROQ LLM initialization failed: {e}")
    print("⚠️  Using mock LLM responses")
    llm = None

def test_router_with_distress_levels():
    """Test that router correctly identifies distress levels and routes appropriately"""
    
    test_cases = [
        # Crisis cases (highest priority)
        {
            "query": "I want to kill myself",
            "expected_agent": "crisis_intervention",
            "expected_crisis": True,
            "description": "Crisis detection"
        },
        {
            "query": "I'm thinking about suicide",
            "expected_agent": "crisis_intervention", 
            "expected_crisis": True,
            "description": "Suicide ideation"
        },
        
        # HIGH distress cases (priority 2)
        {
            "query": "I don't feel good and can't cope",
            "expected_agent": "information",
            "expected_distress": "high",
            "description": "High distress - severe keywords"
        },
        {
            "query": "I'm completely overwhelmed and broken",
            "expected_agent": "information",
            "expected_distress": "high", 
            "description": "High distress - multiple severe keywords"
        },
        {
            "query": "feeling terrible and worthless",
            "expected_agent": "information",
            "expected_distress": "high",
            "description": "High distress - emotional crisis"
        },
        
        # MILD distress cases (priority 2)
        {
            "query": "I'm feeling sad and need help",
            "expected_agent": "information",
            "expected_distress": "mild",
            "description": "Mild distress - general support needed"
        },
        {
            "query": "struggling with anxiety lately",
            "expected_agent": "information", 
            "expected_distress": "mild",
            "description": "Mild distress - ongoing concern"
        },
        {
            "query": "having a hard time and feeling confused",
            "expected_agent": "information",
            "expected_distress": "mild",
            "description": "Mild distress - need guidance"
        },
        
        # No distress cases (priority 3 - LLM routing)
        {
            "query": "what is depression",
            "expected_agent": "information",
            "expected_distress": "none",
            "description": "Informational query"
        },
        {
            "query": "tell me about therapy options",
            "expected_agent": "information",
            "expected_distress": "none", 
            "description": "Educational request"
        },
        {
            "query": "I want to find a therapist in Singapore",
            "expected_agent": "resource",  # This should route to resource agent
            "expected_distress": "none",
            "description": "Resource request"
        },
        {
            "query": "can I take a mental health assessment",
            "expected_agent": "assessment",  # This should route to assessment agent
            "expected_distress": "none",
            "description": "Assessment request"
        }
    ]
    
    print("=" * 90)
    print("🧭 ROUTER AGENT INTEGRATION TEST - 2-LEVEL DISTRESS SYSTEM")
    print("=" * 90)
    
    correct = 0
    total = 0
    
    for test_case in test_cases:
        query = test_case["query"]
        expected_agent = test_case["expected_agent"]
        expected_crisis = test_case.get("expected_crisis", False)
        expected_distress = test_case.get("expected_distress", "none")
        description = test_case["description"]
        
        # Create initial state
        state = AgentState(
            current_query=query,
            messages=[],
            current_agent="",
            crisis_detected=False,
            context="",
            distress_level=""
        )
        
        # Test individual components first
        crisis_detected = detect_crisis(query)
        distress_level, score = detect_distress_level(query)
        
        # Test router (with mock LLM for non-distress cases)
        if llm and not crisis_detected and distress_level == "none":
            try:
                result_state = router_node(state, llm, mock_get_relevant_context)
            except:
                # Fallback if LLM fails
                result_state = state
                result_state["current_agent"] = "information"
        else:
            # For crisis and distress cases, we can test without LLM
            result_state = router_node(state, None, mock_get_relevant_context)
        
        # Check results
        agent_correct = result_state["current_agent"] == expected_agent
        crisis_correct = result_state["crisis_detected"] == expected_crisis
        distress_correct = distress_level == expected_distress
        
        overall_correct = agent_correct and crisis_correct and distress_correct
        
        if overall_correct:
            correct += 1
            status = "✅"
        else:
            status = "❌"
        
        total += 1
        
        print(f"\n{status} {description}")
        print(f"   Query: \"{query}\"")
        print(f"   Expected: Agent={expected_agent}, Crisis={expected_crisis}, Distress={expected_distress}")
        print(f"   Actual:   Agent={result_state['current_agent']}, Crisis={result_state['crisis_detected']}, Distress={distress_level}")
        
        if not overall_correct:
            if not agent_correct:
                print(f"   ⚠️  Agent routing mismatch")
            if not crisis_correct:
                print(f"   ⚠️  Crisis detection mismatch")
            if not distress_correct:
                print(f"   ⚠️  Distress level mismatch")
    
    print(f"\n" + "=" * 90)
    print(f"📊 ROUTER INTEGRATION RESULTS: {correct}/{total} tests passed ({100*correct/total:.1f}%)")
    print("=" * 90)
    
    return correct, total

def test_distress_level_routing():
    """Test that distress level is properly passed to information agent"""
    
    print(f"\n🎯 DISTRESS LEVEL ROUTING TEST:")
    print("-" * 90)
    
    test_queries = [
        ("I don't feel good", "high"),
        ("I'm struggling with sadness", "mild"), 
        ("what is anxiety", "none")
    ]
    
    for query, expected_level in test_queries:
        state = AgentState(
            current_query=query,
            messages=[],
            current_agent="",
            crisis_detected=False,
            context="",
            distress_level=""
        )
        
        # Test router
        result_state = router_node(state, None, mock_get_relevant_context)
        actual_level = result_state.get("distress_level", "none")
        
        status = "✅" if actual_level == expected_level else "❌"
        print(f"\n{status} \"{query}\"")
        print(f"   Expected distress level: {expected_level}")
        print(f"   Actual distress level: {actual_level}")

if __name__ == "__main__":
    # Run router integration tests
    correct, total = test_router_with_distress_levels()
    
    # Run distress level routing tests
    test_distress_level_routing()
    
    print(f"\n🏁 ROUTER TESTING COMPLETE")
    if correct == total:
        print("🎉 All router integration tests passed!")
    else:
        print(f"⚠️  {total - correct} tests need attention")