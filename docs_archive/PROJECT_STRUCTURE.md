# Project Structure

## Overview
The AI Mental Health Support Agent is organized into a clean, modular structure for easy maintenance and scalability.

## Complete Directory Structure

```
MentalHealth_AI/
│
├── run_web.py                      # 🌐 Launch web interface (main entry point)
│
├── interface/                      # 🎨 User interfaces
│   ├── __init__.py
│   └── web/                        # Flask web interface
│       ├── __init__.py
│       ├── app.py                  # Flask application
│       ├── templates/
│       │   └── index.html          # Chat interface UI
│       └── static/                 # CSS, JS, images (future)
│
├── agent/                          # 🤖 AI Agent modules
│   ├── __init__.py                 # Package exports
│   ├── router_agent.py             # Query routing (78 lines)
│   ├── crisis_agent.py             # Crisis intervention (57 lines)
│   ├── information_agent.py        # Mental health education (52 lines)
│   ├── resource_agent.py           # Singapore services (64 lines)
│   ├── assessment_agent.py         # DASS-21 screening (60 lines)
│   ├── escalation_agent.py         # Professional referrals (69 lines)
│   └── update_agent.py             # Knowledge base updates (382 lines)
│
├── data/                           # 📚 Data and storage
│   ├── knowledge/                  # Knowledge base (13 files)
│   │   ├── mental_health_info/     # Anxiety, depression, stress
│   │   ├── singapore_resources/    # CHAT, IMH services
│   │   ├── coping_strategies/      # Breathing, CBT, mindfulness
│   │   ├── dass21_guidelines/      # Assessment protocols
│   │   └── crisis_protocols/       # Emergency procedures
│   └── chroma_db/                  # Vector database (168 chunks)
│       └── .update_state.json      # Update tracking
│
├── app.py                          # 🧠 Core agent system (315 lines)
│
├── requirements.txt                # 📦 Python dependencies
├── .env                            # 🔐 Environment variables (API keys)
│
└── Documentation/
    ├── README.md                   # Project overview
    ├── AGENT_STRUCTURE.md          # Agent architecture details
    ├── WEB_INTERFACE_GUIDE.md      # Web interface technical guide
    ├── FLASK_QUICKSTART.md         # Quick start guide
    ├── UPDATE_AGENT_GUIDE.md       # Knowledge base management
    └── PROJECT_STRUCTURE.md        # This file
```

## Quick Start Commands

### Start Web Interface
```bash
python run_web.py
# Opens at http://localhost:5001
```

### Update Knowledge Base
```bash
python agent/update_agent.py auto
```

### Check System Status
```bash
python agent/update_agent.py status
```

## Module Breakdown

### 1. Interface Layer (`interface/`)
**Purpose:** User-facing interfaces

- **web/app.py** - Flask web application
  - Routes: `/`, `/chat`, `/new-conversation`, `/history`, `/health`
  - Session management
  - Agent integration

- **web/templates/index.html** - Chat UI
  - Modern gradient design
  - Real-time messaging
  - Crisis alerts
  - Mobile responsive

### 2. Agent Layer (`agent/`)
**Purpose:** Specialized AI agents

- **router_agent.py** - Routes queries to appropriate specialist
- **crisis_agent.py** - Handles emergency situations
- **information_agent.py** - Provides mental health education
- **resource_agent.py** - Singapore service information
- **assessment_agent.py** - DASS-21 screening guidance
- **escalation_agent.py** - Professional referrals
- **update_agent.py** - Knowledge base management

### 3. Data Layer (`data/`)
**Purpose:** Knowledge storage and retrieval

- **knowledge/** - Source documents (13 files, 5 categories)
- **chroma_db/** - Vector database (168 chunks)

### 4. Core System (`app.py`)
**Purpose:** Agent orchestration

- LangGraph workflow
- ChromaDB integration
- RAG pipeline
- Agent coordination

## File Counts

```
Python Files:
├── Interface: 3 files (web app + init files)
├── Agents: 8 files (7 agents + init)
├── Core: 1 file (app.py)
├── Utils: 1 file (run_web.py)
└── Total: 13 Python files

Data Files:
├── Knowledge: 13 .txt files
├── Vector DB: ~168 chunks
└── Config: 3 files (.env, requirements.txt, .update_state.json)

Documentation:
└── 6 markdown files
```

## Line Count Summary

```
Total Project Lines: ~1,500+
├── Core System (app.py): 315 lines
├── Agent Modules: 788 lines
│   ├── Core agents: 404 lines (6 files)
│   └── Update agent: 382 lines
├── Web Interface: 300+ lines
│   ├── Flask app: 155 lines
│   └── HTML/CSS/JS: ~200 lines
└── Launch script: 20 lines
```

## Dependencies

### Python Packages (requirements.txt)
```
Core:
- langgraph>=0.0.55         (Multi-agent framework)
- langchain>=0.1.10         (LLM framework)
- langchain-groq>=0.1.0     (Groq integration)
- groq>=0.4.2               (LLM API)

Database:
- chromadb>=0.4.22          (Vector database)

Web:
- flask>=3.0.0              (Web framework)

Utilities:
- python-dotenv>=1.0.0      (Environment variables)
- pydantic>=2.5.0           (Data validation)
- numpy>=1.24.0             (Numerical computing)
```

### Environment Variables (.env)
```
GROQ_API_KEY=your_api_key           # Required
FLASK_SECRET_KEY=your_secret        # Optional (auto-generated)
```

## Data Flow

```
User Browser (localhost:5001)
    ↓
Flask Server (interface/web/app.py)
    ↓
Agent Workflow (app.py)
    ↓
Router Agent (agent/router_agent.py)
    ↓ [Routes to appropriate specialist]
    ├─→ Crisis Agent
    ├─→ Information Agent
    ├─→ Resource Agent
    ├─→ Assessment Agent
    └─→ Escalation Agent
        ↓
    ChromaDB Query (data/chroma_db/)
        ↓
    RAG Context Retrieval
        ↓
    LLM Generation (Groq Llama 3.3 70B)
        ↓
    Response → Flask → User Browser
```

## Architecture Principles

### 1. Modularity
- Each agent is independent and self-contained
- Easy to add, remove, or modify agents
- Clear separation of concerns

### 2. Scalability
- Interface layer separate from business logic
- Agents can run independently
- ChromaDB handles large knowledge bases

### 3. Maintainability
- Small, focused files (~50-80 lines per agent)
- Clear naming conventions
- Comprehensive documentation

### 4. Flexibility
- Easy to add new interfaces (CLI, API, mobile)
- Agents can be reused in different contexts
- Pluggable knowledge sources

## Adding New Components

### New Agent
```python
# 1. Create agent/new_agent.py
def new_agent_node(state, llm, get_relevant_context):
    # Agent logic
    return state

# 2. Update agent/__init__.py
from .new_agent import new_agent_node

# 3. Update app.py workflow
workflow.add_node("new_agent", new_agent_wrapper)
```

### New Interface
```python
# 1. Create interface/cli/
# 2. Add CLI application
# 3. Import agent system
from app import create_workflow
```

### New Knowledge Category
```bash
# 1. Add files to data/knowledge/new_category/
# 2. Run update agent
python agent/update_agent.py auto
```

## Testing

### Run Web Interface
```bash
python run_web.py
# Test at http://localhost:5001
```

### Test Agent System
```python
from agent import router_node, crisis_intervention_node
# Test individual agents
```

### Update Knowledge Base
```bash
python agent/update_agent.py check   # Check for changes
python agent/update_agent.py auto    # Auto-update
python agent/update_agent.py status  # View current state
```

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 "interface.web.app:app"
```

### Environment Setup
```bash
# Set in production environment
export GROQ_API_KEY="your_production_key"
export FLASK_SECRET_KEY="secure_random_key"
export FLASK_ENV="production"
```

## Version History

- **v2.1** - Reorganized Flask GUI into interface/web/
- **v2.0** - Added update_agent.py, modular agent structure
- **v1.5** - Flask web interface implemented
- **v1.0** - Core agent system with ChromaDB RAG

## Future Enhancements

### Planned
1. **CLI Interface** - interface/cli/ for terminal usage
2. **API Interface** - interface/api/ for REST API
3. **Static Assets** - interface/web/static/ for custom CSS/JS
4. **User Profiles** - Persistent user data and preferences
5. **Analytics Dashboard** - Usage metrics and insights

### Under Consideration
- Mobile app integration
- Multi-language support
- Voice interface
- Advanced analytics
- Admin panel

## Maintenance

### Regular Tasks
```bash
# Weekly: Update knowledge base
python agent/update_agent.py auto

# Monthly: Update dependencies
pip install --upgrade -r requirements.txt

# As needed: Check system health
curl http://localhost:5001/health
```

### Troubleshooting
See individual guides:
- Web issues → WEB_INTERFACE_GUIDE.md
- Agent issues → AGENT_STRUCTURE.md
- Update issues → UPDATE_AGENT_GUIDE.md
