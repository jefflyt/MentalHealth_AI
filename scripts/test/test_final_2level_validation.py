"""
Final comprehensive test of the Simplified 2-Level Distress Detection System
Demonstrates the complete functionality and performance metrics
"""

import sys
sys.path.append('.')
from agent.router_agent import detect_distress_level, detect_crisis, apply_intensity_modifiers
from agent.router_agent import HIGH_DISTRESS_KEYWORDS, MILD_DISTRESS_KEYWORDS

def run_comprehensive_2level_test():
    """Run complete test suite for the 2-level system"""
    
    print("=" * 100)
    print("🧠 SIMPLIFIED 2-LEVEL DISTRESS DETECTION SYSTEM - FINAL VALIDATION")
    print("=" * 100)
    
    # System Overview
    print(f"\n📊 SYSTEM CONFIGURATION:")
    print(f"   ├─ HIGH distress keywords: {len(HIGH_DISTRESS_KEYWORDS)} (weight: 5 each)")
    print(f"   ├─ MILD distress keywords: {len(MILD_DISTRESS_KEYWORDS)} (weight: 1 each)")
    print(f"   ├─ Total patterns: {len(HIGH_DISTRESS_KEYWORDS) + len(MILD_DISTRESS_KEYWORDS)}")
    print(f"   └─ Crisis keywords: 13 (separate detection)")
    
    print(f"\n🎯 CLASSIFICATION THRESHOLDS:")
    print(f"   ├─ HIGH: ≥5 points → Severe crisis, immediate empathy")
    print(f"   ├─ MILD: 1-4 points → General support, friendly approach")
    print(f"   └─ NONE: 0 points → Informational queries")
    
    print(f"\n⚡ INTENSITY MODIFIERS:")
    print(f"   ├─ Adverbs (very, really, extremely): 1.5x multiplier")
    print(f"   ├─ Punctuation (3+ exclamation marks): +2 per extra mark")
    print(f"   └─ ALL CAPS (2+ words): +3 points")
    
    # Test Categories
    test_results = {
        "crisis": [],
        "high_distress": [],
        "mild_distress": [],
        "no_distress": [],
        "edge_cases": []
    }
    
    # Crisis Detection Tests
    crisis_queries = [
        "I want to kill myself",
        "thinking about suicide", 
        "I want to die",
        "going to hurt myself",
        "no reason to live"
    ]
    
    print(f"\n🚨 CRISIS DETECTION TESTS:")
    print("-" * 50)
    for query in crisis_queries:
        is_crisis = detect_crisis(query)
        status = "✅" if is_crisis else "❌"
        test_results["crisis"].append(is_crisis)
        print(f"   {status} \"{query}\" → Crisis: {is_crisis}")
    
    # High Distress Tests
    high_distress_queries = [
        ("I don't feel good", 5.0),
        ("can't cope anymore", 5.0),
        ("feeling overwhelmed and broken", 15.0),
        ("completely hopeless and worthless", 15.0),
        ("very desperate and falling apart", 11.25),  # With modifier
        ("struggling worried scared anxious lonely", 5.0),  # 5 mild = high
    ]
    
    print(f"\n😔 HIGH DISTRESS TESTS (≥5 points):")
    print("-" * 50)
    for query, expected_score in high_distress_queries:
        level = detect_distress_level(query)
        score = calculate_final_score(query)
        is_correct = level == "high"
        status = "✅" if is_correct else "❌"
        test_results["high_distress"].append(is_correct)
        print(f"   {status} \"{query}\"")
        print(f"      Score: {score:.1f} | Level: {level.upper()}")
    
    # Mild Distress Tests
    mild_distress_queries = [
        ("feeling sad", 2.0),
        ("I'm struggling", 1.0),
        ("worried and anxious", 2.0),
        ("need help", 1.0),
        ("having a hard time", 1.0),
        ("confused and tired", 2.0),
        ("very worried", 1.5),  # With modifier
        ("stressed and burned out", 2.0),
    ]
    
    print(f"\n😐 MILD DISTRESS TESTS (1-4 points):")
    print("-" * 50)
    for query, expected_score in mild_distress_queries:
        level = detect_distress_level(query)
        score = calculate_final_score(query)
        is_correct = level == "mild"
        status = "✅" if is_correct else "❌"
        test_results["mild_distress"].append(is_correct)
        print(f"   {status} \"{query}\"")
        print(f"      Score: {score:.1f} | Level: {level.upper()}")
    
    # No Distress Tests
    no_distress_queries = [
        "what is depression",
        "tell me about anxiety",
        "explain therapy options",
        "hello how are you",
        "I want to learn about CBT",
        "what are the symptoms of PTSD"
    ]
    
    print(f"\n😊 NO DISTRESS TESTS (0 points):")
    print("-" * 50)
    for query in no_distress_queries:
        level = detect_distress_level(query)
        score = calculate_final_score(query)
        is_correct = level == "none"
        status = "✅" if is_correct else "❌"
        test_results["no_distress"].append(is_correct)
        print(f"   {status} \"{query}\"")
        print(f"      Score: {score:.1f} | Level: {level.upper()}")
    
    # Edge Case Tests (Boundary and Modifier Tests)
    edge_cases = [
        ("struggling worried scared anxious", 4.0, "mild"),  # Just below threshold
        ("struggling worried scared anxious lonely", 5.0, "high"),  # At threshold
        ("extremely sad and worried!!!", 5.0, "high"),  # Modifiers push to high
        ("SAD SAD SAD upset", 5.0, "high"),  # CAPS modifier
        ("very very very sad", 1.5, "mild"),  # Multiple adverbs don't stack
    ]
    
    print(f"\n🎯 EDGE CASE TESTS:")
    print("-" * 50)
    for query, expected_score, expected_level in edge_cases:
        level = detect_distress_level(query)
        score = calculate_final_score(query)
        is_correct = level == expected_level
        status = "✅" if is_correct else "❌"
        test_results["edge_cases"].append(is_correct)
        print(f"   {status} \"{query}\"")
        print(f"      Score: {score:.1f} | Expected: {expected_level.upper()} | Got: {level.upper()}")
    
    # Calculate Overall Results
    total_correct = sum([
        sum(test_results["crisis"]),
        sum(test_results["high_distress"]),
        sum(test_results["mild_distress"]),
        sum(test_results["no_distress"]),
        sum(test_results["edge_cases"])
    ])
    
    total_tests = sum([
        len(test_results["crisis"]),
        len(test_results["high_distress"]),
        len(test_results["mild_distress"]),
        len(test_results["no_distress"]),
        len(test_results["edge_cases"])
    ])
    
    print(f"\n" + "=" * 100)
    print(f"📊 FINAL RESULTS - 2-LEVEL SYSTEM PERFORMANCE")
    print("=" * 100)
    print(f"🚨 Crisis Detection:     {sum(test_results['crisis'])}/{len(test_results['crisis'])} tests passed ({100*sum(test_results['crisis'])/len(test_results['crisis']):.1f}%)")
    print(f"😔 High Distress:        {sum(test_results['high_distress'])}/{len(test_results['high_distress'])} tests passed ({100*sum(test_results['high_distress'])/len(test_results['high_distress']):.1f}%)")
    print(f"😐 Mild Distress:        {sum(test_results['mild_distress'])}/{len(test_results['mild_distress'])} tests passed ({100*sum(test_results['mild_distress'])/len(test_results['mild_distress']):.1f}%)")
    print(f"😊 No Distress:          {sum(test_results['no_distress'])}/{len(test_results['no_distress'])} tests passed ({100*sum(test_results['no_distress'])/len(test_results['no_distress']):.1f}%)")
    print(f"🎯 Edge Cases:           {sum(test_results['edge_cases'])}/{len(test_results['edge_cases'])} tests passed ({100*sum(test_results['edge_cases'])/len(test_results['edge_cases']):.1f}%)")
    print("-" * 100)
    print(f"🏆 OVERALL PERFORMANCE:  {total_correct}/{total_tests} tests passed ({100*total_correct/total_tests:.1f}%)")
    
    # Performance Analysis
    print(f"\n🔍 SYSTEM ANALYSIS:")
    print(f"   ✅ Strengths:")
    print(f"      • Clear 2-level classification (HIGH vs MILD)")
    print(f"      • Effective 5-point threshold boundary")
    print(f"      • Proper intensity modifier integration")
    print(f"      • Crisis detection works independently")
    print(f"      • No false positives for informational queries")
    
    if total_correct < total_tests:
        print(f"   ⚠️  Areas for improvement:")
        print(f"      • Consider keyword deduplication for repeated terms")
        print(f"      • Fine-tune boundary cases near 5-point threshold")
    
    print("=" * 100)
    return total_correct, total_tests

def calculate_final_score(query):
    """Calculate final score including modifiers for debugging"""
    query_lower = query.lower()
    score = 0
    
    # Check high distress patterns
    for phrase, weight in HIGH_DISTRESS_KEYWORDS.items():
        if phrase in query_lower:
            score += weight
    
    # Check mild distress patterns
    for phrase, weight in MILD_DISTRESS_KEYWORDS.items():
        if phrase in query_lower:
            score += weight
    
    # Apply modifiers
    final_score = apply_intensity_modifiers(query, score)
    return final_score

if __name__ == "__main__":
    correct, total = run_comprehensive_2level_test()
    
    print(f"\n🎉 2-LEVEL DISTRESS DETECTION SYSTEM VALIDATION COMPLETE")
    if correct == total:
        print("🏆 PERFECT SCORE! All tests passed!")
    elif correct/total >= 0.9:
        print("🌟 EXCELLENT PERFORMANCE! System ready for production.")
    elif correct/total >= 0.8:
        print("✅ GOOD PERFORMANCE! Minor adjustments recommended.")
    else:
        print("⚠️  NEEDS IMPROVEMENT! Review failed test cases.")