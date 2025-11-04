#!/usr/bin/env python3
"""
Test Menu Selection Routing
Verifies that subsequent menu selections (like "IMH Helpline") are routed correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from agent.router_agent import detect_explicit_intent, detect_distress_level


def test_menu_routing():
    """Test that resource menu items are recognized as resource requests, not distress."""
    print("\n" + "=" * 70)
    print("🧪 TESTING MENU SELECTION ROUTING")
    print("=" * 70)
    
    test_cases = [
        {
            "query": "Support services in Singapore",
            "expected_agent": "resource",
            "description": "Top-level resource request"
        },
        {
            "query": "IMH Helpline",
            "expected_agent": "resource",
            "description": "Specific helpline selection"
        },
        {
            "query": "SOS Hotline",
            "expected_agent": "resource",
            "description": "Crisis hotline selection"
        },
        {
            "query": "CHAT service",
            "expected_agent": "resource",
            "description": "CHAT service selection"
        },
        {
            "query": "therapy",
            "expected_agent": "resource",
            "description": "Therapy inquiry"
        },
        {
            "query": "I need help",
            "expected_agent": "",  # Should NOT match explicit intent (could be distress)
            "description": "Ambiguous help request (should check distress)"
        },
        {
            "query": "where can i get help",
            "expected_agent": "resource",
            "description": "Where to get help inquiry"
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in test_cases:
        query = test["query"]
        expected = test["expected_agent"]
        desc = test["description"]
        
        # Check explicit intent detection
        detected_agent = detect_explicit_intent(query)
        
        # Also check distress level to see if it would interfere
        distress_level, distress_score = detect_distress_level(query)
        
        print(f"\n📝 Query: '{query}'")
        print(f"   Description: {desc}")
        print(f"   Expected agent: {expected if expected else '(none - check distress)'}")
        print(f"   Detected agent: {detected_agent if detected_agent else '(none)'}")
        print(f"   Distress level: {distress_level} (score: {distress_score:.1f})")
        
        if detected_agent == expected:
            print(f"   ✅ PASS")
            passed += 1
        else:
            print(f"   ❌ FAIL - Expected '{expected}', got '{detected_agent}'")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"📊 RESULTS: {passed} passed, {failed} failed")
    print("=" * 70)
    
    if failed == 0:
        print("✅ All menu routing tests passed!")
        print("\n💡 Menu selections will correctly route to Resource Agent")
        print("   instead of being detected as distress queries.")
    else:
        print(f"⚠️  {failed} test(s) failed - review routing logic")
    
    return failed == 0


if __name__ == "__main__":
    success = test_menu_routing()
    sys.exit(0 if success else 1)
