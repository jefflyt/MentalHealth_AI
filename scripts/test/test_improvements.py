"""
Quick test to verify the improved distress detection and response variety
"""

import sys
sys.path.append('.')

# Test the distress detection scores
from agent.router_agent import detect_distress_level, apply_intensity_modifiers

def test_improved_detection():
    test_cases = [
        ("i am sad", "Should be MILD"),
        ("I AM SAD!!!", "Should be HIGH due to caps + punctuation"),
        ("i dont feel good", "Should be HIGH due to specific phrase"),
        ("feeling down", "Should be MILD"),
        ("I'm struggling", "Should be MILD"),
        ("I'm really really sad and can't cope", "Should be HIGH due to multiple keywords + modifiers"),
    ]
    
    print("="*80)
    print("🧪 IMPROVED DISTRESS DETECTION TEST")
    print("="*80)
    
    for query, expected in test_cases:
        # Calculate raw score
        query_lower = query.lower()
        from agent.router_agent import HIGH_DISTRESS_KEYWORDS, MILD_DISTRESS_KEYWORDS
        
        raw_score = 0
        for phrase, weight in HIGH_DISTRESS_KEYWORDS.items():
            if phrase in query_lower:
                raw_score += weight
        for phrase, weight in MILD_DISTRESS_KEYWORDS.items():
            if phrase in query_lower:
                raw_score += weight
        
        final_score = apply_intensity_modifiers(query, raw_score)
        level = detect_distress_level(query)
        
        print(f"\n📝 \"{query}\"")
        print(f"   Expected: {expected}")
        print(f"   Raw Score: {raw_score} → Final Score: {final_score:.1f}")
        print(f"   Detected Level: {level.upper()}")
        
        # Show modifiers
        if final_score != raw_score:
            print(f"   Modifiers applied: +{final_score - raw_score:.1f}")

def test_response_variety():
    """Test that responses are varied"""
    from agent.sunny_persona import get_distress_responses
    
    print("\n" + "="*80)
    print("🎭 RESPONSE VARIETY TEST")
    print("="*80)
    
    print("\n🔥 HIGH DISTRESS RESPONSES (should vary):")
    for i in range(5):
        responses = get_distress_responses()
        high_response = responses['high']
        print(f"   {i+1}. {high_response['opening']}")
    
    print("\n😊 MILD DISTRESS RESPONSES (should vary):")
    for i in range(5):
        responses = get_distress_responses()
        mild_response = responses['mild']
        print(f"   {i+1}. {mild_response['opening']}")

if __name__ == "__main__":
    test_improved_detection()
    test_response_variety()