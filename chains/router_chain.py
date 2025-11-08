"""
Router Chain - Intelligent routing to appropriate specialized agents
Analyzes user intent and routes to crisis, information, resource, or assessment agents
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def create_router_chain(llm):
    """
    Create a router chain that determines which agent should handle the query.
    
    Args:
        llm: LangChain LLM instance
        
    Returns:
        Router chain that outputs agent name
    """
    
    router_prompt = ChatPromptTemplate.from_template("""You are an intelligent routing system for a mental health support agent.

Analyze the user's message and determine which specialized agent should handle it.

Available Agents:
1. CRISIS - Handle immediate safety concerns, self-harm, suicidal ideation
2. INFORMATION - Provide information about mental health conditions, symptoms, treatments
3. RESOURCE - Help find mental health services, hotlines, support groups in Singapore
4. ASSESSMENT - Conduct mental health assessments, symptom tracking
5. GENERAL - General supportive conversation, check-ins, coping strategies

User Message: {query}

CRITICAL ROUTING RULES:
- If ANY mention of self-harm, suicide, immediate danger → CRISIS
- If asking about specific conditions, symptoms, diagnoses → INFORMATION
- If looking for therapists, hotlines, services, help → RESOURCE
- If wanting assessment, screening, symptom check → ASSESSMENT
- Otherwise → GENERAL

Output ONLY the agent name (CRISIS, INFORMATION, RESOURCE, ASSESSMENT, or GENERAL).

Agent:""")
    
    router_chain = router_prompt | llm | StrOutputParser()
    
    return router_chain


def create_distress_router_chain(llm):
    """
    Create a two-level router that first detects distress, then routes appropriately.
    
    Args:
        llm: LangChain LLM instance
        
    Returns:
        Dictionary with distress_chain and agent_chain
    """
    
    # Distress detection prompt
    distress_prompt = ChatPromptTemplate.from_template("""Analyze the user's message for emotional distress level.

User Message: {query}

Output ONLY one of:
- HIGH (immediate crisis, self-harm, suicide, severe distress)
- MILD (moderate distress, sadness, anxiety, stress)
- NONE (neutral, informational, general questions)

Distress Level:""")
    
    # Agent routing prompt (only used if distress is not HIGH)
    agent_prompt = ChatPromptTemplate.from_template("""Route this message to the appropriate agent.

User Message: {query}
Distress Level: {distress_level}

Available Agents:
- INFORMATION (mental health info, conditions, symptoms)
- RESOURCE (find services, hotlines, support)
- ASSESSMENT (mental health screening, symptom tracking)
- GENERAL (supportive conversation, coping strategies)

Output ONLY the agent name.

Agent:""")
    
    distress_chain = distress_prompt | llm | StrOutputParser()
    agent_chain = agent_prompt | llm | StrOutputParser()
    
    return {
        "distress_chain": distress_chain,
        "agent_chain": agent_chain
    }


def route_with_distress_detection(query: str, llm):
    """
    Two-level routing: detect distress → route to agent.
    
    Args:
        query: User message
        llm: LangChain LLM instance
        
    Returns:
        Tuple of (agent_name, distress_level)
    """
    
    chains = create_distress_router_chain(llm)
    
    # Step 1: Detect distress level
    distress_level = chains["distress_chain"].invoke({"query": query}).strip().upper()
    
    # Step 2: Route based on distress
    if distress_level == "HIGH":
        return ("CRISIS", distress_level)
    
    # Step 3: Route to specific agent
    agent = chains["agent_chain"].invoke({
        "query": query,
        "distress_level": distress_level
    }).strip().upper()
    
    return (agent, distress_level)


def create_menu_router_chain(llm):
    """
    Create a router for menu-based navigation.
    
    Args:
        llm: LangChain LLM instance
        
    Returns:
        Menu router chain
    """
    
    menu_prompt = ChatPromptTemplate.from_template("""You are routing a menu selection in a mental health support system.

User Input: {input}
Available Options: {options}

The user can:
1. Select a number from the menu
2. Type a description that matches an option
3. Ask to go back or return to main menu

Determine which menu option the user is selecting.

Output ONLY the option number (1, 2, 3, etc.) or "BACK" or "MAIN".

Selection:""")
    
    menu_router = menu_prompt | llm | StrOutputParser()
    
    return menu_router
