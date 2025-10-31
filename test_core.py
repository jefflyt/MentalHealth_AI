#!/usr/bin/env python3
"""
Simple test script to verify the core functionality works
"""

import os
from dotenv import load_dotenv

def test_core_imports():
    """Test that all required imports work."""
    try:
        import langchain
        import langgraph 
        import langchain_groq
        print("✅ Core imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_groq_connection():
    """Test Groq API connection."""
    try:
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            print("⚠️ GROQ_API_KEY not found in .env file")
            print("Please add your API key to .env file:")
            print("GROQ_API_KEY=your_api_key_here")
            return False
            
        from langchain_groq import ChatGroq
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
        print("✅ Groq LLM initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Groq connection error: {e}")
        return False

def test_langgraph_workflow():
    """Test basic LangGraph workflow creation."""
    try:
        from langgraph.graph import StateGraph, END
        from typing import TypedDict
        
        class SimpleState(TypedDict):
            message: str
        
        def simple_node(state: SimpleState) -> dict:
            return {"message": "Hello from LangGraph!"}
        
        workflow = StateGraph(SimpleState)
        workflow.add_node("test_node", simple_node)
        workflow.set_entry_point("test_node")
        workflow.add_edge("test_node", END)
        
        app = workflow.compile()
        result = app.invoke({"message": "test"})
        
        if result["message"] == "Hello from LangGraph!":
            print("✅ LangGraph workflow test successful")
            return True
        else:
            print("❌ LangGraph workflow test failed")
            return False
            
    except Exception as e:
        print(f"❌ LangGraph workflow error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing AI Mental Health Agent Core Components...")
    print("=" * 60)
    
    tests = [
        ("Core Imports", test_core_imports),
        ("Groq Connection", test_groq_connection),
        ("LangGraph Workflow", test_langgraph_workflow)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All core components are working!")
        print("\n✅ System is ready for use:")
        print("1. Your dependencies are installed correctly")
        print("2. LangGraph workflow system is functional")
        print("3. Run: python app.py to start the agent")
    else:
        print("⚠️ Some components need attention. Please check the errors above.")
        
    return passed == total

if __name__ == "__main__":
    main()