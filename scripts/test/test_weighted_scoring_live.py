"""
Live test of weighted scoring in the actual agent system
"""

import sys
sys.path.append('.')

from agent.router_agent import detect_distress_level, HIGH_DISTRESS_KEYWORDS, MODERATE_DISTRESS_KEYWORDS, MILD_DISTRESS_KEYWORDS, apply_intensity_modifiers

def calculate_score_detailed(query):
    """Calculate score with detailed breakdown"""
    query_lower = query.lower()
    score = 0
    matches = []
    
    for phrase, weight in HIGH_DISTRESS_KEYWORDS.items():
        if phrase in query_lower:
            score += weight
            matches.append(f"'{phrase}' (HIGH: {weight})")
    
    for phrase, weight in MODERATE_DISTRESS_KEYWORDS.items():
        if phrase in query_lower:
            score += weight
            matches.append(f"'{phrase}' (MOD: {weight})")
    
    for phrase, weight in MILD_DISTRESS_KEYWORDS.items():
        if phrase in query_lower:
            score += weight
            matches.append(f"'{phrase}' (MILD: {weight})")
    
    base_score = score
    final_score = apply_intensity_modifiers(query, score)
    
    return base_score, final_score, matches

print("=" * 80)
print("🔬 LIVE WEIGHTED SCORING DEMONSTRATION")
print("=" * 80)
print("\nThis demonstrates how the new weighted scoring system works in real-time.")
print("Each query shows the exact score calculation and level detection.\n")
print("=" * 80)

# Real-world test queries
test_cases = [
    "i dont feel good",
    "feeling sad",
    "I'm really overwhelmed!!!",
    "i need help",
    "I'm struggling and exhausted",
    "can't cope anymore",
    "hello",
    "what is anxiety?",
]

for query in test_cases:
    base_score, final_score, matches = calculate_score_detailed(query)
    level = detect_distress_level(query)
    
    print(f"\n📝 Query: \"{query}\"")
    print(f"   └─ Detected Level: {level.upper()}")
    print(f"   └─ Base Score: {base_score:.1f} → Final Score: {final_score:.1f}")
    if matches:
        print(f"   └─ Matched Keywords: {', '.join(matches)}")
    else:
        print(f"   └─ No distress keywords detected")
    
    # Show modifier effects if any
    if final_score != base_score:
        modifier_effect = final_score - base_score
        print(f"   └─ ⚡ Intensity Modifiers: +{modifier_effect:.1f} points")

print("\n" + "=" * 80)
print("✅ WEIGHTED SCORING SYSTEM ACTIVE")
print("=" * 80)
print("\n💡 Key Features:")
print("   • 165+ keyword patterns across 3 distress levels")
print("   • Weighted scoring (HIGH: 5, MODERATE: 3, MILD: 1)")
print("   • Intensity modifiers for adverbs, punctuation, and CAPS")
print("   • Dynamic thresholds: HIGH ≥10, MODERATE 5-9, MILD 1-4")
print("\n" + "=" * 80)
