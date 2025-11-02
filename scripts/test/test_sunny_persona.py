#!/usr/bin/env python3
"""
Sunny Persona Demonstration
Shows how all agents can maintain consistent personality using centralized system
"""

from agent.sunny_persona import (
    get_sunny_persona, 
    get_distress_responses, 
    build_sunny_prompt,
    get_agent_specific_style,
    get_sample_interactions
)

def demonstrate_sunny_consistency():
    """Demonstrate how all agents maintain Sunny's consistent personality."""
    
    print("🌟 SUNNY PERSONA SYSTEM DEMONSTRATION")
    print("="*60)
    
    # Load Sunny's core personality
    sunny = get_sunny_persona()
    print(f"\n👋 Meet {sunny['name']}: {sunny['role']}")
    print(f"Greeting: {sunny['greeting']}")
    
    # Show core traits
    print(f"\n🌟 Core Personality Traits:")
    for trait in sunny['core_traits']:
        print(f"  • {trait}")
    
    # Show distress responses  
    print(f"\n💙 Distress Level Responses:")
    distress_responses = get_distress_responses()
    for level, response in distress_responses.items():
        print(f"  {level.upper()}: {response['opening']}")
    
    # Show agent-specific adaptations
    print(f"\n🤖 Agent-Specific Adaptations:")
    agents = ['information', 'crisis', 'escalation', 'resource', 'assessment']
    for agent in agents:
        style = get_agent_specific_style(agent)
        print(f"  {agent.upper()}: {style['focus']} - {style['tone']}")
    
    # Show sample interactions
    print(f"\n💬 Sample Interactions:")
    samples = get_sample_interactions()
    for interaction_type, dialogue in samples.items():
        print(f"\n  {interaction_type.replace('_', ' ').title()}:")
        print(f"    User: \"{dialogue['user']}\"")
        print(f"    Sunny: \"{dialogue['sunny'][:100]}...\"")
    
    # Show how to build prompts
    print(f"\n🔧 How Agents Use This System:")
    sample_prompt = build_sunny_prompt(
        agent_type='information',
        context="User is feeling anxious about work",
        specific_instructions="Provide supportive response with coping tip"
    )
    
    print(f"  Sample prompt structure (first 200 chars):")
    print(f"  \"{sample_prompt[:200]}...\"")
    
    print(f"\n✅ All agents now reference these consistent personality components!")
    print(f"📝 Update docs/SUNNY_PERSONA.md to change Sunny's characteristics")
    print("="*60)

if __name__ == "__main__":
    demonstrate_sunny_consistency()