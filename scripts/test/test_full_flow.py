"""
Test the complete assessment-to-chat flow
"""

import requests
import json

def test_assessment_flow():
    """Test the complete flow: assessment → store results → chat with Sunny"""
    
    base_url = "http://localhost:5001"
    
    print("="*80)
    print("🧪 COMPLETE ASSESSMENT-TO-CHAT FLOW TEST")
    print("="*80)
    
    # Step 1: Simulate storing assessment results
    print("\n📊 Step 1: Storing sample assessment results...")
    
    sample_assessment = {
        "assessmentType": "dass21",
        "timestamp": "2025-11-03T15:30:00",
        "scores": {
            "depression": {"level": "moderate", "score": 15},
            "anxiety": {"level": "mild", "score": 8},
            "stress": {"level": "normal", "score": 4}
        }
    }
    
    try:
        # Store assessment results
        store_response = requests.post(
            f"{base_url}/store-assessment-results",
            json=sample_assessment,
            timeout=10
        )
        
        if store_response.status_code == 200:
            print("✅ Assessment results stored successfully")
            store_data = store_response.json()
            conversation_starter = store_data.get('conversation_starter', 'No starter provided')
            print(f"💬 Conversation starter: {conversation_starter}")
        else:
            print(f"❌ Failed to store assessment: {store_response.status_code}")
            return
            
    except requests.RequestException as e:
        print(f"❌ Network error storing assessment: {e}")
        return
    
    # Step 2: Test getting conversation starter
    print("\n🎯 Step 2: Getting conversation starter...")
    
    try:
        starter_response = requests.get(
            f"{base_url}/get-conversation-starter",
            timeout=10
        )
        
        if starter_response.status_code == 200:
            starter_data = starter_response.json()
            if starter_data.get('has_starter'):
                print("✅ Conversation starter available")
                print(f"💬 Message: {starter_data.get('message', 'No message')}")
            else:
                print("⚠️ No conversation starter available")
        else:
            print(f"❌ Failed to get starter: {starter_response.status_code}")
            
    except requests.RequestException as e:
        print(f"❌ Network error getting starter: {e}")
    
    # Step 3: Chat with Sunny using assessment results
    print("\n💬 Step 3: Chatting with Sunny (with assessment context)...")
    
    test_messages = [
        "Hi Sunny",
        "Tell me about my results",
        "What should I do about my depression?"
    ]
    
    for message in test_messages:
        print(f"\n👤 User: {message}")
        
        try:
            chat_response = requests.post(
                f"{base_url}/chat",
                json={"message": message},
                timeout=15
            )
            
            if chat_response.status_code == 200:
                chat_data = chat_response.json()
                response = chat_data.get('response', 'No response')
                print(f"🌟 Sunny: {response[:200]}{'...' if len(response) > 200 else ''}")
            else:
                print(f"❌ Chat failed: {chat_response.status_code}")
                
        except requests.RequestException as e:
            print(f"❌ Network error in chat: {e}")
    
    print(f"\n{'='*80}")
    print("🎉 Test completed! Check the responses above to see if Sunny:")
    print("   ✅ Acknowledges the assessment")
    print("   ✅ Provides gentle overview of results")  
    print("   ✅ Offers practical suggestions")
    print("   ✅ Shows empathy and support")
    print("="*80)

if __name__ == "__main__":
    test_assessment_flow()