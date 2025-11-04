#!/usr/bin/env python3
"""
Phase 2 Code Quality & Refactoring Improvements - Validation Test
Validates all improvements made in Phase 2.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from agent.router_agent import detect_distress_level, _matches_with_word_boundary, _is_negated
import logging


def test_tuple_return():
    """Test that detect_distress_level returns a tuple (level, score)."""
    print("\n🧪 Testing Tuple Return from detect_distress_level")
    print("=" * 60)
    
    test_cases = [
        ("I'm feeling anxious", "mild"),
        ("I can't cope anymore", "high"),
        ("What is depression?", "none")
    ]
    
    passed = 0
    for query, expected_level in test_cases:
        result = detect_distress_level(query)
        
        # Check it's a tuple
        if not isinstance(result, tuple):
            print(f"❌ '{query}' - Did not return tuple, got {type(result)}")
            continue
        
        # Check tuple has 2 elements
        if len(result) != 2:
            print(f"❌ '{query}' - Tuple should have 2 elements, got {len(result)}")
            continue
        
        level, score = result
        
        # Check types
        if not isinstance(level, str) or not isinstance(score, (int, float)):
            print(f"❌ '{query}' - Invalid types: level={type(level)}, score={type(score)}")
            continue
        
        # Check level matches expected
        if level == expected_level:
            print(f"✅ '{query}' → ({level}, {score:.1f})")
            passed += 1
        else:
            print(f"❌ '{query}' → ({level}, {score:.1f}), expected level: {expected_level}")
    
    print(f"\nResult: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_word_boundary_matching():
    """Test word-boundary matching prevents partial word matches."""
    print("\n🧪 Testing Word-Boundary Matching")
    print("=" * 60)
    
    test_cases = [
        # (phrase, text, should_match)
        ("over", "I am overwhelmed", False),  # Should NOT match "over" in "overwhelmed"
        ("over", "it's over", True),  # Should match standalone "over"
        ("sad", "I am sad", True),  # Should match standalone "sad"
        ("sad", "sadly disappointed", False),  # Should NOT match "sad" in "sadly"
        ("down", "feeling down", True),  # Should match standalone "down"
        ("down", "downtown life", False),  # Should NOT match "down" in "downtown"
    ]
    
    passed = 0
    for phrase, text, should_match in test_cases:
        result = _matches_with_word_boundary(phrase, text)
        expected = "match" if should_match else "not match"
        actual = "matched" if result else "not matched"
        
        if result == should_match:
            print(f"✅ '{phrase}' in '{text}' - correctly {actual}")
            passed += 1
        else:
            print(f"❌ '{phrase}' in '{text}' - {actual}, should {expected}")
    
    print(f"\nResult: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_enhanced_negation():
    """Test enhanced negation detection."""
    print("\n🧪 Testing Enhanced Negation Detection")
    print("=" * 60)
    
    test_cases = [
        # (phrase, text, phrase_position, should_be_negated)
        ("happy", "I am not at all happy", 18, True),  # "not at all"
        ("sad", "I am not really sad", 16, True),  # "not really"
        ("worried", "I never worried before", 8, True),  # "never"
        ("anxious", "I am anxious today", 5, False),  # No negation
        ("stressed", "hardly stressed", 7, True),  # "hardly"
    ]
    
    passed = 0
    for phrase, text, pos, should_be_negated in test_cases:
        result = _is_negated(phrase, text, pos)
        expected = "negated" if should_be_negated else "not negated"
        actual = "negated" if result else "not negated"
        
        if result == should_be_negated:
            print(f"✅ '{phrase}' in '{text}' - correctly {actual}")
            passed += 1
        else:
            print(f"❌ '{phrase}' in '{text}' - {actual}, should be {expected}")
    
    print(f"\nResult: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_logging_configured():
    """Test that logging is properly configured."""
    print("\n🧪 Testing Logging Configuration")
    print("=" * 60)
    
    try:
        from agent import router_agent, resource_agent, escalation_agent
        
        modules_to_check = [
            ('router_agent', router_agent),
            ('resource_agent', resource_agent),
            ('escalation_agent', escalation_agent)
        ]
        
        passed = 0
        for name, module in modules_to_check:
            if hasattr(module, 'logger'):
                logger = getattr(module, 'logger')
                if isinstance(logger, logging.Logger):
                    print(f"✅ {name} - logger configured")
                    passed += 1
                else:
                    print(f"❌ {name} - logger exists but wrong type: {type(logger)}")
            else:
                print(f"❌ {name} - no logger found")
        
        print(f"\nResult: {passed}/{len(modules_to_check)} modules have logging")
        return passed == len(modules_to_check)
        
    except Exception as e:
        print(f"❌ Error checking logging: {e}")
        return False


def test_build_sunny_prompt_usage():
    """Test that agents use build_sunny_prompt."""
    print("\n🧪 Testing build_sunny_prompt Usage")
    print("=" * 60)
    
    try:
        from agent.resource_agent import resource_agent_node
        from agent.escalation_agent import human_escalation_node
        import inspect
        
        agents_to_check = [
            ('resource_agent_node', resource_agent_node),
            ('human_escalation_node', human_escalation_node)
        ]
        
        passed = 0
        for name, func in agents_to_check:
            source = inspect.getsource(func)
            if 'build_sunny_prompt' in source:
                print(f"✅ {name} - uses build_sunny_prompt")
                passed += 1
            else:
                print(f"❌ {name} - does not use build_sunny_prompt")
        
        print(f"\nResult: {passed}/{len(agents_to_check)} agents use build_sunny_prompt")
        return passed == len(agents_to_check)
        
    except Exception as e:
        print(f"❌ Error checking build_sunny_prompt usage: {e}")
        return False


def test_no_duplicate_scoring():
    """Test that distress scoring is not duplicated in router_node."""
    print("\n🧪 Testing No Duplicate Distress Scoring")
    print("=" * 60)
    
    try:
        from agent.router_agent import router_node
        import inspect
        
        source = inspect.getsource(router_node)
        
        # Check that we don't have duplicate scoring logic
        # The refactored version should use the returned score directly
        if source.count('detect_distress_level(query)') == 1:
            print("✅ detect_distress_level called once")
            
            # Check we're unpacking the tuple
            if 'distress_level, distress_score = detect_distress_level' in source:
                print("✅ Tuple unpacking found - using returned score")
                
                # Check we're not recalculating score
                manual_score_calc = 'for phrase, weight in {**HIGH_DISTRESS_KEYWORDS'
                if manual_score_calc not in source:
                    print("✅ No duplicate manual score calculation")
                    return True
                else:
                    print("❌ Found duplicate manual score calculation")
                    return False
            else:
                print("❌ Not unpacking tuple correctly")
                return False
        else:
            count = source.count('detect_distress_level(query)')
            print(f"❌ detect_distress_level called {count} times, should be 1")
            return False
            
    except Exception as e:
        print(f"❌ Error checking duplicate scoring: {e}")
        return False


def test_early_routing():
    """Test that expensive operations are skipped for early-routed queries."""
    print("\n🧪 Testing Early Routing Optimization")
    print("=" * 60)
    
    try:
        from agent.router_agent import router_node
        import inspect
        
        source = inspect.getsource(router_node)
        lines = source.split('\n')
        
        # Find line numbers of key operations
        crisis_check_line = next((i for i, line in enumerate(lines) if 'detect_crisis' in line), -1)
        distress_check_line = next((i for i, line in enumerate(lines) if 'detect_distress_level' in line), -1)
        context_fetch_line = next((i for i, line in enumerate(lines) if 'get_relevant_context' in line and 'route classify' in line), -1)
        
        if crisis_check_line < context_fetch_line and distress_check_line < context_fetch_line:
            print(f"✅ Crisis check at line ~{crisis_check_line}")
            print(f"✅ Distress check at line ~{distress_check_line}")
            print(f"✅ Context fetch at line ~{context_fetch_line}")
            print("✅ Early routing optimizations in correct order")
            return True
        else:
            print(f"❌ Incorrect ordering:")
            print(f"   Crisis: {crisis_check_line}, Distress: {distress_check_line}, Context: {context_fetch_line}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking early routing: {e}")
        return False


def main():
    """Run all Phase 2 validation tests."""
    print("\n" + "=" * 70)
    print("🔧 PHASE 2 CODE QUALITY & REFACTORING - VALIDATION TESTS")
    print("=" * 70)
    
    results = []
    
    # Run all tests
    results.append(("Tuple Return", test_tuple_return()))
    results.append(("Word-Boundary Matching", test_word_boundary_matching()))
    results.append(("Enhanced Negation", test_enhanced_negation()))
    results.append(("No Duplicate Scoring", test_no_duplicate_scoring()))
    results.append(("Early Routing", test_early_routing()))
    results.append(("Logging Configuration", test_logging_configured()))
    results.append(("build_sunny_prompt Usage", test_build_sunny_prompt_usage()))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 PHASE 2 SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✅ ALL PHASE 2 IMPROVEMENTS VALIDATED!")
        print("\n🎉 Summary of Improvements:")
        print("  ✓ Tuple return from detect_distress_level (no duplicate scoring)")
        print("  ✓ Early routing optimization (crisis/distress before context fetch)")
        print("  ✓ Word-boundary keyword matching (no partial matches)")
        print("  ✓ Enhanced negation detection (compound patterns)")
        print("  ✓ Logging system implemented (router, resource, escalation)")
        print("  ✓ Shared build_sunny_prompt utility (consistent persona)")
    else:
        print("\n⚠️  Some tests failed - review errors above")
    
    print("=" * 70)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
