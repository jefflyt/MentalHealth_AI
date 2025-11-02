# 🧠 AI Mental Health Support Agent

> A comprehensive multi-agent system providing mental health support with Singapore-specific resources, built with LangGraph, ChromaDB RAG, and Flask web interface.

## 🌟 Overview

An AI-powered mental health support system featuring:
- 🤖 **6 Specialized AI Agents** (Router, Crisis, Information, Resource, Assessment, Escalation)
- 🌐 **Beautiful Web Interface** (Flask-based chat UI)
- 📚 **RAG-Enhanced Responses** (ChromaDB with 168 knowledge chunks)
- 🇸🇬 **Singapore-Specific Resources** (CHAT, IMH, local services)
- 🚨 **Crisis Detection** (Automatic emergency support)
- 🔄 **Smart Knowledge Management** (Auto-update agent)

## 🏗️ Architecture

```
User Browser (http://localhost:5001)
    ↓
Flask Web Interface
    ↓
Agent Router (3-Level Priority System)
    ├── Priority 1: Crisis Keywords → Crisis Agent
    ├── Priority 2: Distress Detection → Information Agent (Menu: 1-4)
    └── Priority 3: LLM Routing → [Resource|Assessment|Escalation]
    ↓
ChromaDB RAG (168 chunks from 13 files)
    ↓
Groq LLM (Llama 3.3 70B)
    ↓
Response with Singapore Resources
```

### Routing Logic:

1. **🚨 Crisis Detection** (Highest Priority)
   - Keywords: suicide, self-harm, want to die, etc.
   - Routes to: **Crisis Agent** (immediate support)

2. **😔 Distress Level Detection** (Medium Priority)
   - **3-Level System**: HIGH 🔴 / MODERATE 🟡 / MILD 🟢
   - Routes to: **Information Agent** (tailored response based on distress level)
   
   **🔴 HIGH Distress Examples:**
   - "i dont feel good", "can't cope", "overwhelmed", "breaking down"
   - Response: Immediate empathy + supportive menu with emphasis on urgent help
   
   **🟡 MODERATE Distress Examples:**
   - "feeling sad", "struggling", "hard time", "anxious", "depressed"
   - Response: Warm acknowledgment + standard numbered menu (1-4)
   
   **🟢 MILD Distress Examples:**
   - "i need help", "confused", "not sure", "need someone to talk to"
   - Response: Welcoming, open-ended invitation + bullet-point options

3. **🎯 Specific Requests** (Standard Routing)
   - Uses LLM to intelligently route to specialized agents
   - Resource Agent: Singapore services
   - Assessment Agent: DASS-21 screening
   - Escalation Agent: Professional referrals

## 📁 Project Structure

```
MentalHealth_AI/
├── run_web.py                  # 🚀 Launch web interface
│
├── interface/                  # 🎨 User interfaces
│   └── web/
│       ├── app.py              # Flask application
│       └── templates/
│           └── index.html      # Chat UI
│
├── agent/                      # 🤖 AI Agents (8 modules)
│   ├── router_agent.py         # Query routing
│   ├── crisis_agent.py         # Crisis intervention
│   ├── information_agent.py    # Mental health education
│   ├── resource_agent.py       # Singapore services
│   ├── assessment_agent.py     # DASS-21 screening
│   ├── escalation_agent.py     # Professional referrals
│   └── update_agent.py         # Knowledge base updates
│
├── data/                       # 📚 Data storage
│   ├── knowledge/              # 13 source files, 5 categories
│   │   ├── mental_health_info/
│   │   ├── singapore_resources/
│   │   ├── coping_strategies/
│   │   ├── dass21_guidelines/
│   │   └── crisis_protocols/
│   └── chroma_db/              # Vector database (168 chunks)
│
├── app.py                      # 🧠 Core agent system
├── requirements.txt            # 📦 Dependencies
├── .env                        # 🔐 API keys
│
└── Documentation/
    ├── README.md               # This file
    ├── QUICKSTART.md           # How to run
    └── GUIDE.md                # Complete technical guide
```

## ✨ Key Features

### 🤖 Multi-Agent System
- **Router Agent**: Intelligently routes queries with 3-level priority system
  - 🚨 **Priority 1**: Crisis detection (suicide, self-harm) → Crisis Agent
  - 😔 **Priority 2**: Distress level detection (HIGH/MODERATE/MILD) → Information Agent
    - **HIGH 🔴**: Immediate empathy ("i dont feel good", "can't cope")
    - **MODERATE 🟡**: Warm support ("feeling sad", "struggling")
    - **MILD 🟢**: Friendly welcome ("i need help", "confused")
  - 🎯 **Priority 3**: Specific requests (services, assessment) → Specialized agents
- **Crisis Agent**: Immediate support for emergencies (24/7 contacts)
- **Information Agent**: Evidence-based mental health education with adaptive responses
  - Tailors empathy level to detected distress (HIGH/MODERATE/MILD)
  - Provides numbered menu (1-4) or bullet points based on intensity
  - Handles coping strategies, understanding feelings, and general support
- **Resource Agent**: Singapore mental health services (CHAT, IMH)
- **Assessment Agent**: DASS-21 screening guidance
- **Escalation Agent**: Professional referral recommendations

### 🌐 Web Interface
- Modern, responsive chat UI (mobile-friendly)
- Real-time messaging with typing indicators
- Crisis detection with visual alerts
- Session-based conversation management
- New conversation button

### 📚 Knowledge Base (168 Chunks)
- **Mental Health Info**: Anxiety, depression, stress
- **Singapore Resources**: CHAT, IMH, emergency services
- **Coping Strategies**: Breathing, mindfulness, CBT
- **DASS-21 Guidelines**: Assessment protocols
- **Crisis Protocols**: Emergency procedures

### 🔄 Smart Updates
- Automatic change detection (MD5 hashing)
- Incremental updates (only changed files)
- CLI and Python API
- State persistence

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **LLM** | Groq Llama 3.3 70B |
| **Framework** | LangGraph (multi-agent) |
| **Vector DB** | ChromaDB (persistent) |
| **Embeddings** | all-MiniLM-L6-v2 (384d) |
| **Web** | Flask 3.0 |
| **Python** | 3.9-3.13 (3.13 compatible!) |

## 📊 System Stats

- **Total Lines**: ~1,500
- **Agent Modules**: 7 files (coping agent removed - redundant)
- **Core System**: 315 lines
- **Web Interface**: 300+ lines
- **Knowledge Base**: 13 files, 168 chunks
- **Response Time**: <2s with RAG
- **Distress Detection**: 3-level system (HIGH/MODERATE/MILD) with 40+ patterns

## 🧪 Sample Queries

Try these in the web interface:

**🔴 HIGH Distress (triggers immediate empathy):**
- "i dont feel good"
- "I can't cope anymore"
- "I'm overwhelmed"
- "feel terrible"

**🟡 MODERATE Distress (triggers warm support):**
- "I'm struggling"
- "feeling sad"
- "feeling anxious"
- "having a hard time"

**🟢 MILD Distress (triggers friendly welcome):**
- "i need help"
- "confused about my feelings"
- "not sure what to do"
- "need someone to talk to"

**General Information:**
- "I'm feeling anxious lately"
- "What is depression?"
- "Stress management techniques"

**Singapore Resources:**
- "Where can I get help in Singapore?"
- "Tell me about CHAT services"
- "Mental health clinics near me"

**Assessment:**
- "How do I know if I have anxiety?"
- "Tell me about DASS-21"
- "Mental health screening"

**Coping Strategies:**
- "Breathing exercises for anxiety"
- "Mindfulness techniques"
- "CBT techniques for negative thoughts"

**Crisis (will trigger emergency support):**
- "I'm having thoughts of self-harm"
- "I don't want to live anymore"

## 📖 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Setup and run guide (5 minutes - START HERE!)
- **[GUIDE.md](GUIDE.md)** - Complete technical guide
  - Agent architecture and routing logic
  - Web interface setup and customization
  - Knowledge base management (manual + web scraping)
  - Deployment options and best practices
  - API reference and troubleshooting
- **[README.md](README.md)** - This file (project overview)

## 🔐 Security & Safety

### Crisis Response
- ✅ Immediate crisis detection
- ✅ Singapore emergency contacts (SOS: 1767, IMH: 6389-2222)
- ✅ Visual alerts in web UI
- ✅ Professional escalation pathways

### Data Privacy
- ✅ Session-based (no persistent user data)
- ✅ Secure API key management
- ✅ No external data sharing
- ✅ Local vector database

### Clinical Boundaries
- ⚠️ **Not a replacement** for professional care
- ⚠️ **Educational support** only
- ⚠️ **Encourages** professional consultation
- ⚠️ **Clear disclaimers** in all responses

## 🚀 Getting Started

1. **Read [QUICKSTART.md](QUICKSTART.md)** - 5-minute setup
2. **Start the app**: `python run_web.py`
3. **Open browser**: http://localhost:5001
4. **Start chatting!**

For detailed technical information, see **[GUIDE.md](GUIDE.md)**.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test thoroughly (especially crisis detection!)
4. Submit pull request

## 📄 License

Educational and research purposes. Not for clinical use without proper licensing.

## ⚠️ Disclaimer

**This system provides support, not diagnosis or treatment.**

For emergencies:
- 🚨 **Singapore**: 995 (Emergency), 1767 (SOS 24/7)
- 🏥 **IMH Emergency**: 6389-2222
- 💬 **CHAT**: 6493-6500 (Ages 16-30)

Always consult qualified mental health professionals for clinical care.

## 🎯 Version

**v2.2** - Enhanced distress detection with 3-level response system (HIGH/MODERATE/MILD)

---

**Ready to start?** → See [QUICKSTART.md](QUICKSTART.md)

**Need technical details?** → See [GUIDE.md](GUIDE.md)

**Questions?** Open an issue on GitHub.
