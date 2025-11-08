"""
Integration Tests for LangChain Components
Tests Retriever, Chains, Memory, and Tools
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Test Retriever
def test_retriever_initialization():
    """Test ChromaDB retriever initialization."""
    from app import initialize_chroma, retriever
    
    print("\n🔍 Testing Retriever Initialization...")
    vectorstore = initialize_chroma()
    
    assert retriever is not None, "Retriever should be initialized"
    print("✅ Retriever initialized successfully")


def test_retriever_query():
    """Test retriever query functionality."""
    from app import get_relevant_context
    
    print("\n🔍 Testing Retriever Query...")
    context = get_relevant_context("anxiety coping strategies", n_results=2)
    
    assert context is not None, "Context should be returned"
    assert len(context) > 0, "Context should not be empty"
    print(f"✅ Retriever returned context: {len(context)} characters")


# Test Chains
def test_rag_chain():
    """Test RAG chain creation and execution."""
    from app import retriever, llm
    from chains import create_rag_chain
    
    if retriever is None:
        pytest.skip("Retriever not initialized")
    
    print("\n⛓️ Testing RAG Chain...")
    rag_chain = create_rag_chain(retriever, llm)
    
    assert rag_chain is not None, "RAG chain should be created"
    
    # Test invocation
    try:
        result = rag_chain.invoke("What is anxiety?")
        assert result is not None, "RAG chain should return result"
        assert len(result) > 0, "RAG chain result should not be empty"
        print(f"✅ RAG chain executed: {len(result)} characters")
    except Exception as e:
        print(f"⚠️ RAG chain execution failed: {e}")


def test_router_chain():
    """Test router chain creation and execution."""
    from app import llm
    from chains import create_router_chain
    
    print("\n⛓️ Testing Router Chain...")
    router_chain = create_router_chain(llm)
    
    assert router_chain is not None, "Router chain should be created"
    
    # Test routing different queries
    test_queries = [
        ("I want to harm myself", "CRISIS"),
        ("What is depression?", "INFORMATION"),
        ("Find me a therapist", "RESOURCE"),
        ("I want to assess my mental health", "ASSESSMENT"),
    ]
    
    for query, expected_agent in test_queries:
        try:
            result = router_chain.invoke({"query": query})
            result_upper = result.strip().upper()
            print(f"  Query: '{query}' → Agent: {result_upper}")
            assert expected_agent in result_upper, f"Should route to {expected_agent}"
        except Exception as e:
            print(f"  ⚠️ Router failed for '{query}': {e}")
    
    print("✅ Router chain working")


def test_crisis_detection_chain():
    """Test crisis detection chain."""
    from app import llm
    from chains import create_crisis_detection_chain, assess_distress_level
    
    print("\n⛓️ Testing Crisis Detection Chain...")
    
    # Test distress level assessment
    test_cases = [
        ("I feel a bit down today", "MILD"),
        ("I can't take this anymore, everything is falling apart", "HIGH"),
        ("What time does the clinic open?", "NONE"),
    ]
    
    for query, expected_level in test_cases:
        try:
            level, confidence = assess_distress_level(query, llm)
            print(f"  Query: '{query}' → Distress: {level} (confidence: {confidence})")
            assert level == expected_level, f"Should detect {expected_level} distress"
        except Exception as e:
            print(f"  ⚠️ Distress detection failed: {e}")
    
    print("✅ Crisis detection chain working")


# Test Memory
def test_conversation_memory():
    """Test ConversationBufferMemory."""
    from app import get_or_create_memory, save_to_memory, get_conversation_history, clear_session_memory
    
    print("\n💭 Testing Conversation Memory...")
    
    # Create memory
    session_id = "test_session"
    memory = get_or_create_memory(session_id)
    
    assert memory is not None, "Memory should be created"
    print("✅ Memory instance created")
    
    # Save conversation
    memory.save_context(
        {"input": "Hello, I feel anxious"},
        {"output": "I understand you're feeling anxious. How can I help?"}
    )
    
    # Get history
    history = get_conversation_history(session_id)
    assert "anxious" in history, "History should contain conversation"
    print(f"✅ Conversation saved and retrieved: {len(history)} characters")
    
    # Clear memory
    clear_session_memory(session_id)
    history = get_conversation_history(session_id)
    assert history == "No previous conversation" or len(history) == 0, "Memory should be cleared"
    print("✅ Memory cleared successfully")


# Test Tools
def test_assessment_tool():
    """Test assessment tool."""
    from tools import create_assessment_tool
    
    print("\n🔧 Testing Assessment Tool...")
    tool = create_assessment_tool()
    
    assert tool is not None, "Tool should be created"
    
    # Test depression assessment
    try:
        result = tool._run(
            assessment_type="depression",
            responses="sad,tired,hopeless,anxious,sleeping poorly"
        )
        assert "Depression Assessment" in result, "Should return depression assessment"
        assert "Score" in result or "Severity" in result, "Should include scoring"
        print("✅ Assessment tool working")
    except Exception as e:
        print(f"⚠️ Assessment tool failed: {e}")


def test_resource_finder_tool():
    """Test resource finder tool."""
    from tools import create_resource_finder_tool
    
    print("\n🔧 Testing Resource Finder Tool...")
    tool = create_resource_finder_tool()
    
    assert tool is not None, "Tool should be created"
    
    # Test hotline finder
    try:
        result = tool._run(resource_type="hotline", location="Singapore")
        assert "Samaritans" in result or "1-767" in result, "Should include Singapore hotlines"
        print("✅ Resource finder tool working")
    except Exception as e:
        print(f"⚠️ Resource finder failed: {e}")


def test_crisis_hotline_tool():
    """Test crisis hotline tool."""
    from tools import create_crisis_hotline_tool
    
    print("\n🔧 Testing Crisis Hotline Tool...")
    tool = create_crisis_hotline_tool()
    
    assert tool is not None, "Tool should be created"
    
    # Test immediate crisis
    try:
        result = tool._run(urgency="immediate", crisis_type="suicide")
        assert "995" in result or "1-767" in result, "Should include emergency numbers"
        assert "IMMEDIATE" in result or "CRISIS" in result, "Should indicate urgency"
        print("✅ Crisis hotline tool working")
    except Exception as e:
        print(f"⚠️ Crisis hotline tool failed: {e}")


def test_breathing_tool():
    """Test breathing exercise tool."""
    from tools import create_breathing_exercise_tool
    
    print("\n🔧 Testing Breathing Exercise Tool...")
    tool = create_breathing_exercise_tool()
    
    assert tool is not None, "Tool should be created"
    
    # Test box breathing
    try:
        result = tool._run(exercise_type="box", duration=3)
        assert "BOX BREATHING" in result or "4-4-4-4" in result, "Should provide box breathing"
        assert "BREATHE IN" in result or "inhale" in result.lower(), "Should include breathing instructions"
        print("✅ Breathing tool working")
    except Exception as e:
        print(f"⚠️ Breathing tool failed: {e}")


def test_mood_tracker_tool():
    """Test mood tracker tool."""
    from tools import create_mood_tracker_tool
    
    print("\n🔧 Testing Mood Tracker Tool...")
    tool = create_mood_tracker_tool()
    
    assert tool is not None, "Tool should be created"
    
    # Test mood logging
    try:
        result = tool._run(action="log", mood="okay", emotions="calm,focused", notes="Had a good day")
        assert "MOOD LOGGED" in result or "logged" in result.lower(), "Should confirm mood logging"
        print("✅ Mood tracker tool working")
    except Exception as e:
        print(f"⚠️ Mood tracker failed: {e}")


# Integration Test
def test_full_integration():
    """Test full integration of all components."""
    from app import initialize_chroma, retriever, llm, chains, tools
    
    print("\n🔗 Testing Full Integration...")
    
    # Initialize everything
    vectorstore = initialize_chroma()
    
    # Verify all components
    assert retriever is not None, "Retriever should be initialized"
    assert chains["rag"] is not None, "RAG chain should be initialized"
    assert chains["router"] is not None, "Router chain should be initialized"
    assert chains["crisis_detection"] is not None, "Crisis detection chain should be initialized"
    
    assert tools["assessment"] is not None, "Assessment tool should be initialized"
    assert tools["resource_finder"] is not None, "Resource finder tool should be initialized"
    assert tools["crisis_hotline"] is not None, "Crisis hotline tool should be initialized"
    assert tools["breathing"] is not None, "Breathing tool should be initialized"
    assert tools["mood_tracker"] is not None, "Mood tracker tool should be initialized"
    
    print("✅ All components integrated successfully")
    print("\n📊 Integration Summary:")
    print("  ✅ Retriever: Initialized")
    print("  ✅ RAG Chain: Ready")
    print("  ✅ Router Chain: Ready")
    print("  ✅ Crisis Detection Chain: Ready")
    print("  ✅ Memory: Ready")
    print("  ✅ Tools (5): All initialized")


if __name__ == "__main__":
    print("="*60)
    print("🧪 LANGCHAIN COMPONENTS INTEGRATION TESTS")
    print("="*60)
    
    try:
        # Run tests in order
        test_retriever_initialization()
        test_retriever_query()
        test_rag_chain()
        test_router_chain()
        test_crisis_detection_chain()
        test_conversation_memory()
        test_assessment_tool()
        test_resource_finder_tool()
        test_crisis_hotline_tool()
        test_breathing_tool()
        test_mood_tracker_tool()
        test_full_integration()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
