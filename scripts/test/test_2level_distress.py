"""
Test script for SIMPLIFIED 2-LEVEL distress detection system
Tests the new HIGH/MILD system with proper thresholds and intensity modifiers
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
    
    # Check high distress patterns (weight: 5)
    for phrase, weight in HIGH_DISTRESS_KEYWORDS.items():
        if phrase in query_lower:
            score += weight
            matched_phrases.append(f"{phrase} (HIGH: +{weight})")
    
    # Check mild distress patterns (weight: 1)  
    for phrase, weight in MILD_DISTRESS_KEYWORDS.items():
        if phrase in query_lower:
            score += weight
            matched_phrases.append(f"{phrase} (MILD: +{weight})")
    
    base_score = score
    final_score = apply_intensity_modifiers(query, score)
    
    return base_score, final_score, matched_phrases


# Test queries for the SIMPLIFIED 2-LEVEL SYSTEM
test_queries = [
    # HIGH distress (score >= 5) - Crisis-level, immediate empathy needed
    ("i dont feel good", "HIGH"),  # Single high keyword = 5 points
    ("I can't cope anymore", "HIGH"),  # Single high keyword = 5 points
    ("I'm overwhelmed and breaking down", "HIGH"),  # Two high keywords = 10 points
    ("feel terrible and worthless", "HIGH"),  # Two high keywords = 10 points
    ("I'm really falling apart", "HIGH"),  # High keyword + modifier = 5 * 1.5 = 7.5
    ("completely hopeless", "HIGH"),  # High keyword + modifier = 5 * 1.5 = 7.5
    ("struggling struggling struggling worried stressed", "HIGH"),  # 5 mild keywords = 5 points
    
    # MILD distress (score 1-4) - General support, friendly approach
    ("feeling sad", "MILD"),  # Single mild keyword = 1 point
    ("I'm struggling", "MILD"),  # Single mild keyword = 1 point
    ("feeling anxious and worried", "MILD"),  # Two mild keywords = 2 points
    ("having a hard time", "MILD"),  # Single mild keyword = 1 point
    ("exhausted and tired", "MILD"),  # Two mild keywords = 2 points
    ("need help", "MILD"),  # Single mild keyword = 1 point
    ("confused about my feelings", "MILD"),  # Single mild keyword = 1 point
    ("not sure what to do", "MILD"),  # Single mild keyword = 1 point
    ("feeling down and lonely", "MILD"),  # Two mild keywords = 2 points
    
    # NONE (score = 0) - Informational queries
    ("hello", "NONE"),
    ("how are you", "NONE"),
    ("what is depression", "NONE"),
    ("tell me about anxiety", "NONE"),
    ("I want to learn about therapy", "NONE"),
    ("explain cognitive behavioral therapy", "NONE"),
    
    # Edge cases with modifiers
    ("I'm very sad", "MILD"),  # 1 * 1.5 = 1.5 (still mild)
    ("really really struggling", "MILD"),  # 1 * 1.5 = 1.5 (still mild)
    ("so worried and stressed!!", "MILD"),  # 2 * 1.5 = 3 (still mild)
    ("extremely anxious and scared!!!", "MILD"),  # 2 * 1.5 + 2 = 5 → Should be HIGH
    ("HELP HELP struggling badly", "MILD"),  # 2 + 3 (CAPS) = 5 → Should be HIGH
    
    # Multiple high keywords
    ("feel terrible and hopeless", "HIGH"),  # 5 + 5 = 10 points
    ("overwhelmed broken and worthless", "HIGH"),  # 5 + 5 + 5 = 15 points
]

print("=" * 90)
print("🧪 SIMPLIFIED 2-LEVEL DISTRESS DETECTION TEST SUITE")
print("=" * 90)
print(f"\n📊 System Overview:")
print(f"   - HIGH distress keywords: {len(HIGH_DISTRESS_KEYWORDS)} (weight: 5 each)")
print(f"   - MILD distress keywords: {len(MILD_DISTRESS_KEYWORDS)} (weight: 1 each)")
print(f"   - Total patterns: {len(HIGH_DISTRESS_KEYWORDS) + len(MILD_DISTRESS_KEYWORDS)}")
print(f"\n📏 Score Thresholds (SIMPLIFIED 2-LEVEL):")
print(f"   - HIGH: >= 5 points (severe crisis, immediate empathy)")
print(f"   - MILD: 1-4 points (general support, friendly approach)")
print(f"   - NONE: 0 points (informational)")
print(f"\n🔧 Intensity Modifiers:")
print(f"   - Adverbs (very, really, so, etc.): 1.5x multiplier")
print(f"   - Multiple !!! (3+): +2 points per extra mark")
print(f"   - ALL CAPS words (2+): +3 points")
print("\n" + "=" * 90)

correct = 0
total = 0
high_tests = 0
mild_tests = 0
none_tests = 0

for query, expected in test_queries:
    base_score, final_score, matched = calculate_score(query)
    level, score = detect_distress_level(query)
    
    # Track test distribution
    if expected == "HIGH":
        high_tests += 1
    elif expected == "MILD":
        mild_tests += 1
    else:
        none_tests += 1
    
    is_correct = level.upper() == expected.upper()
    
    if is_correct:
        correct += 1
        status = "✅"
    else:
        status = "❌"
    
    total += 1
    
    print(f"\n{status} Query: \"{query}\"")
    print(f"   Expected: {expected} | Detected: {level.upper()}")
    print(f"   Score: {base_score:.1f} (base) → {final_score:.1f} (final)")
    if matched:
        print(f"   Matched: {', '.join(matched[:3])}" + ("..." if len(matched) > 3 else ""))

print("\n" + "=" * 90)
print(f"📊 OVERALL RESULTS: {correct}/{total} tests passed ({100*correct/total:.1f}%)")
print(f"   HIGH distress tests: {high_tests}")
print(f"   MILD distress tests: {mild_tests}")  
print(f"   NONE distress tests: {none_tests}")
print("=" * 90)

# Test intensity modifiers specifically
print("\n🔍 INTENSITY MODIFIER ANALYSIS:")
print("-" * 90)

modifier_examples = [
    ("I'm sad", "Baseline mild"),
    ("I'm very sad", "Adverb modifier (1.5x)"),
    ("I'm really really sad", "Multiple adverbs (1.5x)"),
    ("I'm sad!!!", "Punctuation (+2)"),
    ("I'm SAD and UPSET", "CAPS modifier (+3)"),
    ("I'm extremely anxious and scared!!!", "All modifiers combined"),
]

for query, description in modifier_examples:
    base_score, final_score, matched = calculate_score(query)
    level, score = detect_distress_level(query)
    multiplier = final_score / base_score if base_score > 0 else 0
    
    print(f"\n   \"{query}\"")
    print(f"   {description}")
    print(f"   Score: {base_score:.1f} → {final_score:.1f} (×{multiplier:.2f}) → {level.upper()}")

print("\n" + "=" * 90)

# Boundary testing - critical thresholds
print("\n🎯 BOUNDARY THRESHOLD TESTING:")
print("-" * 90)

boundary_tests = [
    # Test the 5-point boundary (HIGH vs MILD)
    ("struggling worried scared", "MILD"),  # 3 points (should be MILD)
    ("struggling worried scared anxious", "MILD"),  # 4 points (should be MILD) 
    ("struggling worried scared anxious lonely", "HIGH"),  # 5 points (should be HIGH)
    ("don't feel good", "HIGH"),  # Exactly 5 points (should be HIGH)
    ("very worried", "MILD"),  # 1 * 1.5 = 1.5 (should be MILD)
    ("very struggling worried", "MILD"),  # 2 * 1.5 = 3 (should be MILD)
    ("extremely struggling worried anxious", "HIGH"),  # 3 * 1.5 = 4.5 → rounds to 5? Check this
]

print("Testing critical 5-point boundary between MILD and HIGH:")
for query, expected in boundary_tests:
    base_score, final_score, matched = calculate_score(query)
    level, score = detect_distress_level(query)
    
    is_correct = level.upper() == expected.upper()
    status = "✅" if is_correct else "❌"
    
    print(f"\n{status} \"{query}\"")
    print(f"   Score: {base_score:.1f} → {final_score:.1f} | Expected: {expected} | Got: {level.upper()}")

print("\n" + "=" * 90)
print("🏁 2-LEVEL SYSTEM TEST COMPLETE")
print("=" * 90)