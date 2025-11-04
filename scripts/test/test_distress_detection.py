"""
Test script for enhanced distress detection with weighted scoring
"""

import sys
sys.path.append('.')
from agent.router_agent import detect_distress_level, apply_intensity_modifiers
from agent.router_agent import HIGH_DISTRESS_KEYWORDS, MILD_DISTRESS_KEYWORDS

def calculate_score(query):
    """Calculate the raw score for debugging"""
    query_lower = query.lower()
    score = 0
    
    matched_phrases = []
    
    for phrase, weight in HIGH_DISTRESS_KEYWORDS.items():
        if phrase in query_lower:
            score += weight
            matched_phrases.append(f"{phrase} (HIGH: +{weight})")
    
    # MODERATE_DISTRESS_KEYWORDS removed - now using 2-level system
    
    for phrase, weight in MILD_DISTRESS_KEYWORDS.items():
        if phrase in query_lower:
            score += weight
            matched_phrases.append(f"{phrase} (MILD: +{weight})")
    
    base_score = score
    final_score = apply_intensity_modifiers(query, score)
    
    return base_score, final_score, matched_phrases


# Test queries covering all distress levels
test_queries = [
    # HIGH distress (should be >= 15)
    ("i dont feel good", "HIGH"),
    ("I can't cope anymore", "HIGH"),
    ("I'm overwhelmed and breaking down", "HIGH"),
    ("feel terrible and worthless", "HIGH"),
    ("I'm really really falling apart!!!", "HIGH"),  # With modifiers
    
    # MILD distress (should be 1-4 in 2-level system)
    ("feeling sad", "MILD"),
    ("I'm struggling", "MILD"),
    ("feeling anxious and worried", "MILD"),
    ("having a hard time", "MILD"),
    ("I'm so exhausted", "MILD"),  # With modifier
    
    # MILD distress (should be 3-7)
    ("i need help", "MILD"),
    ("confused about my feelings", "MILD"),
    ("not sure what to do", "MILD"),
    ("need someone to talk to", "MILD"),
    ("feeling a bit off and lost", "MILD"),
    
    # NONE (should be < 3)
    ("hello", "NONE"),
    ("how are you", "NONE"),
    ("what is depression", "NONE"),
    ("tell me about anxiety", "NONE"),
    
    # Edge cases with modifiers
    ("I'm REALLY REALLY sad!!!", "MILD/HIGH"),  # Multiple modifiers
    ("feeling down and confused", "MILD"),  # Multiple mild keywords
    ("completely overwhelmed and can't take it", "HIGH"),  # Multiple high keywords
]

print("=" * 80)
print("🧪 DISTRESS DETECTION TEST SUITE - WEIGHTED SCORING")
print("=" * 80)
print(f"\n📊 System Stats:")
print(f"   - HIGH distress keywords: {len(HIGH_DISTRESS_KEYWORDS)} (weight: 5)")
print(f"   - MILD distress keywords: {len(MILD_DISTRESS_KEYWORDS)} (weight: 1)")
print(f"   - Total patterns: {len(HIGH_DISTRESS_KEYWORDS) + len(MILD_DISTRESS_KEYWORDS)}")
print(f"\n📏 Score Thresholds (SIMPLIFIED 2-LEVEL):")
print(f"   - HIGH: >= 5")
print(f"   - MILD: 1-4")
print(f"   - NONE: 0")
print("\n" + "=" * 80)

correct = 0
total = 0

for query, expected in test_queries:
    base_score, final_score, matched = calculate_score(query)
    level, score = detect_distress_level(query)
    
    # Check if match (allow flexibility for edge cases)
    if "/" in expected:
        is_correct = level.upper() in expected.split("/")
    else:
        is_correct = level.upper() == expected.upper()
    
    if is_correct:
        correct += 1
        status = "✅"
    else:
        status = "❌"
    
    total += 1
    
    print(f"\n{status} Query: \"{query}\"")
    print(f"   Expected: {expected} | Detected: {level.upper()}")
    print(f"   Score: {base_score:.1f} (base) → {final_score:.1f} (with modifiers)")
    if matched:
        print(f"   Matched: {', '.join(matched)}")

print("\n" + "=" * 80)
print(f"📊 RESULTS: {correct}/{total} tests passed ({100*correct/total:.1f}%)")
print("=" * 80)

# Additional analysis
print("\n🔍 INTENSITY MODIFIER TESTS:")
print("-" * 80)

modifier_tests = [
    ("I'm sad", "No modifiers"),
    ("I'm very sad", "Adverb (1.5x)"),
    ("I'm sad!!!", "Punctuation (+2)"),
    ("I'm VERY SAD!!!", "Adverb + punctuation + CAPS"),
]

for query, description in modifier_tests:
    base_score, final_score, matched = calculate_score(query)
    print(f"\n   \"{query}\" - {description}")
    print(f"   Score: {base_score:.1f} → {final_score:.1f}")
    print(f"   Multiplier: {final_score/base_score if base_score > 0 else 0:.2f}x")

print("\n" + "=" * 80)
