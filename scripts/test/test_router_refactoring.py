#!/usr/bin/env python3
"""
Test script for router agent refactoring validation.
Tests the new priority system, negation handling, and state management.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from agent.router_agent import (
    detect_distress_level, 
    detect_explicit_intent, 
    detect_menu_reply,
    extract_menu_selection,
    update_menu_context,
    AgentState
)


def test_negation_handling():
    """Test that negation words prevent false positive distress detection."""
    print("\n🧪 Testing Negation Handling")
    print("=" * 50)
    
    test_cases = [
        ("I am not depressed", "none"),
        ("I don't feel sad", "none"), 
        ("I'm not worried about anything", "none"),
        ("I never feel anxious", "none"),
        ("I am depressed", "mild"),
        ("I feel sad today", "mild"),
        ("I'm worried about work", "mild"),
        ("Not feel good at all", "high"),  # Matches "not feel good" exactly
        ("I can't take it anymore", "high")
    ]
    
    for query, expected in test_cases:
        level, score = detect_distress_level(query)
        status = "✅" if level == expected else "❌"
        print(f"{status} '{query}' → {level} (score: {score:.1f}, expected: {expected})")


def test_explicit_intent_detection():
    """Test explicit intent detection for specific agents."""
    print("\n🎯 Testing Explicit Intent Detection")
    print("=" * 50)
    
    test_cases = [
        ("I want to take an assessment", "assessment"),
        ("Can you test my mental health?", "assessment"),
        ("Where can I find a therapist in Singapore?", "resource"),
        ("I need professional help services", "resource"),
        ("I want to talk to a real person", "human_escalation"),
        ("Can I speak to a human counselor?", "human_escalation"),
        ("How are you feeling today?", None),  # General query
        ("What is anxiety?", None)  # General information
    ]
    
    for query, expected in test_cases:
        result = detect_explicit_intent(query)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{query}' → {result} (expected: {expected})")


def test_menu_reply_detection():
    """Test menu reply detection and selection extraction."""
    print("\n📋 Testing Menu Reply Detection")
    print("=" * 50)
    
    menu_options = [
        "Learn about anxiety management",
        "Find local support groups", 
        "Take a mental health assessment"
    ]
    
    test_cases = [
        ("1", True, "Learn about anxiety management"),
        ("2", True, "Find local support groups"),
        ("3", True, "Take a mental health assessment"),
        ("4", False, ""),  # Out of range
        ("first", True, "Learn about anxiety management"),
        ("second one", True, "Find local support groups"),
        ("the third", True, "Take a mental health assessment"),
        ("option 2", True, "Find local support groups"),
        ("hello", False, ""),  # Not a menu reply
    ]
    
    for query, expected_is_reply, expected_selection in test_cases:
        is_reply = detect_menu_reply(query, menu_options)
        selection = extract_menu_selection(query, menu_options)
        
        status1 = "✅" if is_reply == expected_is_reply else "❌"
        status2 = "✅" if selection == expected_selection else "❌"
        
        print(f"{status1} '{query}' → is_reply: {is_reply} (expected: {expected_is_reply})")
        print(f"{status2} '{query}' → selection: '{selection}' (expected: '{expected_selection}')")


def test_priority_system():
    """Test that explicit intent overrides distress detection."""
    print("\n🏆 Testing Priority System Logic")
    print("=" * 50)
    
    # These queries should route to specific agents despite containing distress keywords
    test_cases = [
        ("I'm feeling anxious and want to take an assessment", "assessment"),
        ("I'm worried and need to find a therapist", "resource"),
        ("I feel sad but want to talk to a counselor", "human_escalation"),
        ("I'm depressed, can you test me?", "assessment")
    ]
    
    for query, expected_intent in test_cases:
        level, score = detect_distress_level(query)
        explicit = detect_explicit_intent(query)
        
        # Explicit intent should be found despite distress
        status = "✅" if explicit == expected_intent else "❌"
        print(f"{status} '{query}'")
        print(f"   Distress: {level} (score: {score:.1f}), Explicit Intent: {explicit} (should prioritize explicit)")


def test_state_management():
    """Test state management for menu context."""
    print("\n🔄 Testing State Management")
    print("=" * 50)
    
    # Create mock state
    state: AgentState = {
        "current_query": "",
        "messages": [],
        "current_agent": "",
        "crisis_detected": False,
        "context": "",
        "distress_level": "none",
        "last_menu_options": [],
        "turn_count": 0
    }
    
    # Test menu context update
    menu_options = ["Option A", "Option B", "Option C"]
    update_menu_context(state, menu_options)
    
    status = "✅" if state["last_menu_options"] == menu_options else "❌"
    print(f"{status} Menu context updated: {state['last_menu_options']}")
    
    # Test menu reply detection with state
    is_reply = detect_menu_reply("2", state["last_menu_options"])
    selection = extract_menu_selection("2", state["last_menu_options"])
    
    status1 = "✅" if is_reply else "❌"
    status2 = "✅" if selection == "Option B" else "❌"
    
    print(f"{status1} Menu reply detected for '2'")
    print(f"{status2} Selection extracted: '{selection}'")


def main():
    """Run all router refactoring tests."""
    print("🧭 Router Agent Refactoring Validation Tests")
    print("=" * 60)
    
    test_negation_handling()
    test_explicit_intent_detection()  
    test_menu_reply_detection()
    test_priority_system()
    test_state_management()
    
    print("\n" + "=" * 60)
    print("✅ Router refactoring tests completed!")
    print("🔍 Review any ❌ failures above for issues")


if __name__ == "__main__":
    main()