# Agent Module Structure

## Overview
The AI Mental Health Agent has been refactored into a modular structure with each agent in its own file for better maintainability and organization.

## Quick Reference

### Import Agents
```python
from agent import (
    router_node,
    crisis_intervention_node,
    information_agent_node,
    resource_agent_node,
    assessment_agent_node,
    human_escalation_node,
    UpdateAgent
)
```

### Use Update Agent
```bash
# CLI commands
python agent/update_agent.py check    # Check for changes
python agent/update_agent.py status   # Show current state
python agent/update_agent.py auto     # Auto-update if needed
```

```python
# Python usage
from agent import UpdateAgent
agent = UpdateAgent()
agent.check_for_updates()
agent.perform_smart_update()
```

## Directory Structure
```
MentalHealth_AI/
├── agent/                          # Agent module package
│   ├── __init__.py                # Package initialization with exports
│   ├── router_agent.py            # Router agent (78 lines)
│   ├── crisis_agent.py            # Crisis intervention agent (57 lines)
│   ├── information_agent.py       # Information agent (52 lines)
│   ├── resource_agent.py          # Resource agent (64 lines)
│   ├── assessment_agent.py        # Assessment agent (60 lines)
│   ├── escalation_agent.py        # Human escalation agent (69 lines)
│   └── update_agent.py            # Smart update agent (382 lines)
├── app.py                         # Main application (315 lines)
└── ...
```

## Agent Modules

### 1. Router Agent (`agent/router_agent.py`)
**Purpose:** Intelligent query routing with RAG context
- **Function:** `router_node(state, llm, get_relevant_context)`
- **Features:**
  - Crisis keyword detection
  - RAG-enhanced routing decisions
  - LLM-based agent selection
  - Default fallback to information agent
- **Routes to:** crisis_intervention, information, resource, assessment, human_escalation

### 2. Crisis Intervention Agent (`agent/crisis_agent.py`)
**Purpose:** Immediate support with emergency protocols
- **Function:** `crisis_intervention_node(state, llm, get_relevant_context)`
- **Features:**
  - RAG retrieval of crisis protocols
  - Emergency contact information (Singapore)
  - Empathetic crisis response
  - Fallback to hardcoded emergency contacts
- **Output:** Crisis support message with immediate action steps

### 3. Information Agent (`agent/information_agent.py`)
**Purpose:** Mental health education with evidence-based knowledge
- **Function:** `information_agent_node(state, llm, get_relevant_context)`
- **Features:**
  - RAG retrieval from mental health knowledge base
  - Evidence-based information delivery
  - Coping strategies and guidance
  - Context attribution footer
- **Output:** Educational content with source attribution

### 4. Resource Agent (`agent/resource_agent.py`)
**Purpose:** Singapore mental health services and support
- **Function:** `resource_agent_node(state, llm, get_relevant_context)`
- **Features:**
  - RAG retrieval of Singapore services
  - Contact information and locations
  - Eligibility criteria
  - Operating hours and costs
- **Output:** Service recommendations with emergency contacts

### 5. Assessment Agent (`agent/assessment_agent.py`)
**Purpose:** Mental health screening and DASS-21 guidance
- **Function:** `assessment_agent_node(state, llm, get_relevant_context)`
- **Features:**
  - RAG retrieval of DASS-21 protocols
  - Self-assessment information
  - Professional evaluation guidance
  - Disclaimer about limitations
- **Output:** Assessment guidance with professional referral

### 6. Human Escalation Agent (`agent/escalation_agent.py`)
**Purpose:** Professional referrals and complex case support
- **Function:** `human_escalation_node(state, llm, get_relevant_context)`
- **Features:**
  - RAG retrieval of referral guidelines
  - Professional service recommendations
  - Validation of user concerns
  - Encouragement for professional help
- **Output:** Professional referral information with support message

### 7. Smart Update Agent (`agent/update_agent.py`)
**Purpose:** Monitor and update ChromaDB knowledge base
- **Class:** `UpdateAgent`
- **Features:**
  - File change detection (MD5 hashing)
  - Smart incremental updates
  - Automatic chunk management
  - State persistence
  - CLI interface
- **Commands:**
  - `check`: Check for changes
  - `update`: Perform smart update
  - `auto`: Auto-update if needed
  - `force`: Force full rebuild
  - `status`: Show current state
- **Output:** Update summary with statistics

## Integration with Main App

### app.py Structure
```python
# Import modular agents
from agent import (
    router_node,
    crisis_intervention_node,
    information_agent_node,
    resource_agent_node,
    assessment_agent_node,
    human_escalation_node,
    UpdateAgent  # Smart update agent
)

# Wrapper functions pass dependencies
def router_wrapper(state):
    return router_node(state, llm, get_relevant_context)

# ... similar wrappers for other agents

# Update checking function
def check_for_data_updates():
    from agent import UpdateAgent
    agent = UpdateAgent()
    # ... auto-update logic

# Workflow creation
def create_workflow():
    workflow = StateGraph(AgentState)
    workflow.add_node("router", router_wrapper)
    workflow.add_node("crisis_intervention", crisis_wrapper)
    # ... other nodes
```

## Agent Function Signature
All agents follow the same signature pattern:
```python
def agent_node(state: AgentState, llm: ChatGroq, get_relevant_context) -> AgentState:
    """Agent description."""
    query = state["current_query"]
    context = get_relevant_context(f"query for {query}", n_results=3)
    # ... agent logic
    state["messages"].append(response)
    state["current_agent"] = "complete"
    return state
```

## Dependencies
Each agent module imports:
- `typing.TypedDict, List` - Type hints
- `langchain_groq.ChatGroq` - LLM interface
- `AgentState` - State definition (duplicated for module independence)

## RAG Integration
All agents use RAG through the `get_relevant_context` function:
1. Agent receives query
2. Constructs context-specific query for ChromaDB
3. Retrieves relevant chunks (n_results varies by agent)
4. Passes context + query to LLM
5. Returns grounded response

## Benefits of Modular Structure
1. **Maintainability:** Each agent is self-contained and easy to update
2. **Testability:** Individual agents can be tested in isolation
3. **Readability:** Reduced file size (315 vs 579 lines in app.py)
4. **Scalability:** Easy to add new agents without cluttering main file
5. **Reusability:** Agents can be imported and used in different contexts

## Testing
```python
# Test imports
from agent import router_node, crisis_intervention_node
# ✅ All 6 agents imported successfully

# Test individual agent
state = {
    "current_query": "I feel anxious",
    "messages": [],
    "current_agent": "",
    "crisis_detected": False,
    "context": ""
}
result = information_agent_node(state, llm, get_relevant_context)
```

## Future Enhancements
1. Add agent-specific configuration files
2. Implement agent testing suite
3. Create agent performance metrics
4. Add agent response caching
5. Develop agent behavior logging

## Line Count Summary
- **Total Lines:** 1103
- **app.py:** 315 lines (45% reduction from 579)
- **agent/ module:** 788 lines (distributed across 8 files)
  - **Core agents:** 404 lines (6 specialized agents)
  - **update_agent.py:** 382 lines (smart update system)
- **Average per core agent:** ~58 lines per specialized agent

## Important Notes

### File Naming Convention
Agent files are named with `_agent.py` suffix to avoid conflicts with Python standard library modules (e.g., `resource_agent.py` instead of `resource.py` to avoid conflicting with the `resource` standard library module).

### Update Agent Usage
The update agent can be used both as a module and as a CLI:

**As a module:**
```python
from agent import UpdateAgent
agent = UpdateAgent()
agent.check_for_updates()
agent.perform_smart_update()
```

**As a CLI:**
```bash
python agent/update_agent.py status
python agent/update_agent.py check
python agent/update_agent.py auto
```

## Version History
- **v2.1:** Added update_agent.py to agent module, renamed files to avoid stdlib conflicts
- **v2.0:** Modular agent structure implemented
- **v1.0:** Original monolithic app.py structure
