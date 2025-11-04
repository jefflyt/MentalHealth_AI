# 🧠 AI Mental Health Support Agent

> A comprehensive multi-agent system providing mental health support with Singapore-specific resources, built with LangGraph, ChromaDB RAG, and Flask web interface.

## 🌟 Overview

An AI-powered mental health support system featuring:
- 🤖 **6 Specialized AI Agents** (Router, Crisis, Information, Resource, Assessment, Escalation)
- 🌐 **Beautiful Web Interface** (Flask-based chat UI)
- 📚 **RAG-Enhanced Responses** (ChromaDB with 485 knowledge chunks - Enhanced!)
- 🇸🇬 **Singapore-Specific Resources** (CHAT, IMH, local services)
- 🚨 **Crisis Detection** (Automatic emergency support)
- 🔄 **Smart Knowledge Management** (Auto-update agent)

## 🏗️ Architecture

```
User Browser (http://localhost:5001)
    ↓
Flask Web Interface
    ↓
Agent Router (5-Level Priority System)
    ├── Priority 1: Crisis Keywords → Crisis Agent
    ├── Priority 2: Menu Replies → Information Agent (contextual)
    ├── Priority 3: Explicit Intent → [Resource|Assessment|Escalation]
    ├── Priority 4: Distress Detection → Information Agent (HIGH/MILD)
    └── Priority 5: LLM Routing → General queries
    ↓
ChromaDB RAG (485 chunks from ~29 files - Enhanced!)
    ↓
[Optional] Re-ranker (Cross-encoder for better relevance)
    ↓
Groq LLM (Llama 3.3 70B)
    ↓
Response with Singapore Resources
```

### Routing Logic:

1. **🚨 Crisis Detection** (Highest Priority)
   - Keywords: suicide, suicidal, kill myself, end my life, self-harm, hurt myself, cutting, overdose, etc.
   - Routes to: **Crisis Agent** (immediate support with emergency contacts)

2. **😔 Distress Level Detection** (Medium Priority)
   - **SIMPLIFIED 2-Level System**: HIGH 🔴 / MILD 🟢
   - **Weighted Scoring**: Keyword patterns with point values (HIGH: 5pts, MILD: 1pt)
   - **Intensity Modifiers**: Adverbs (1.5x), punctuation (+2), ALL CAPS (+3)
   - Routes to: **Information Agent** with tailored responses based on distress level
   
   **🔴 HIGH Distress Examples:**
   - "i dont feel good", "can't cope", "overwhelmed", "breaking down", "feel terrible"
   - Response: **Immediate empathy** ("I hear you") + full supportive context + structured numbered menu (1-4 options)
   
   **� MILD Distress Examples:**
   - "feeling sad", "i need help", "confused", "struggling", "anxious", "worried"
   - Response: **Friendly support** ("here to support you") + encouraging context + casual bullet-point options (•)

**🎯 Enhanced Response Examples:**
- "I think I have depression, where can I get help in Singapore?" → Comprehensive Singapore service directory with IMH, polyclinics, costs
- "How do I stop anxiety from controlling my life?" → Detailed anxiety management with practical techniques  
- "I had a panic attack today" → Complete panic disorder guide with grounding techniques
- "What should I expect in my first therapy session?" → Full therapy FAQ with Singapore context

3. **🎯 Specific Requests** (Standard Routing)
   - Uses LLM to intelligently route to specialized agents
   - Resource Agent: Singapore services (CHAT, IMH)
   - Assessment Agent: DASS-21 screening tools
   - Escalation Agent: Professional referrals
   - Information Agent: General mental health education

5. **🤖 LLM Routing** (Priority 5 - Fallback)
   - General queries without crisis/distress/explicit intent
   - Uses RAG context to intelligently route
   - Routes to: Information Agent (default) or specialized agents based on context

**💡 Additional Features:**
- **Assessment Suggestions**: After vague responses, suggests self-assessment tools
- **Context Preservation**: Maintains conversation state across interactions
- **Adaptive Responses**: Tailors empathy level to detected distress

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
│   ├── reranker.py             # Re-ranker (optional)
│   └── update_agent.py         # Knowledge base updates
│
├── data/                       # 📚 Data storage
│   ├── knowledge/              # ~29 source files, 13 categories
│   │   ├── text/                   # Original files (~279 chunks)
│   │   ├── singapore_resources/    # NEW! Comprehensive SG services
│   │   ├── conditions/             # NEW! Detailed condition guides
│   │   ├── emergency/              # NEW! Crisis intervention
│   │   ├── faqs/                   # NEW! Therapy & treatment FAQs
│   │   ├── self_help/              # NEW! Practical techniques
│   │   └── [8 more categories]     # Documents, PDFs, web sources, etc.
│   └── chroma_db/              # Vector database (485 chunks!)
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
  - 😔 **Priority 2**: Distress level detection (HIGH/MILD) → Information Agent
    - **HIGH 🔴**: Immediate empathy ("i dont feel good", "can't cope") → Numbered menu (1-4)
    - **MILD �**: Friendly support ("feeling sad", "i need help") → Bullet-point options (•)
  - 🎯 **Priority 3**: Specific requests (services, assessment) → Specialized agents
- **Crisis Agent**: Immediate support for emergencies (24/7 contacts)
- **Information Agent**: Evidence-based mental health education with adaptive responses
  - Tailors empathy level to detected distress (HIGH/MILD)
  - HIGH: Numbered menu (1-4) with immediate empathy and full support
  - MILD: Bullet-point options (•) with friendly encouragement
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

### 📚 Knowledge Base (485 Chunks - Enhanced!) 🚀

**Major Enhancement Complete:** +206 chunks (+74% increase)

**🔄 Re-ranker Integration (Enabled):**
- Cross-encoder based re-ranking for improved relevance
- Using Python 3.11 with PyTorch and sentence-transformers support
- Improves retrieval accuracy by 15-25% for complex queries
- <200ms additional latency with TinyBERT model
- ~9ms average re-ranking time with excellent query matching

**Original Categories (~279 chunks):**
- **Mental Health Info**: Anxiety, depression, stress basics
- **Singapore Resources**: CHAT, IMH emergency services  
- **Coping Strategies**: Breathing, mindfulness, basic CBT
- **DASS-21 Guidelines**: Assessment protocols
- **Crisis Protocols**: Emergency procedures

**NEW Enhanced Categories (+206 chunks):**
- **🇸🇬 Singapore Resources**: Comprehensive service directory (IMH, polyclinics, private practice)
- **🧠 Conditions**: Detailed guides (depression, anxiety disorders, panic disorder)
- **🚨 Emergency**: Crisis intervention (suicide prevention, safety planning)
- **❓ FAQs**: Complete therapy questions (types, costs, expectations)
- **🛠️ Self-Help**: Practical CBT techniques (thought challenging, behavioral activation)
- **📄 Research PDFs**: Scientific papers (mental health research, brain science)

**Impact:** System now provides comprehensive, Singapore-specific mental health support!

**Enhancement Roadmap:** Following comprehensive enhancement plan
- **Current Progress:** 7/48 planned files (14.6% complete)
- **Target:** 1,000+ chunks for comprehensive coverage
- **Achievement:** 48.5% of target reached!

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
| **Re-ranker** | Cross-encoder TinyBERT (optional) |
| **Web** | Flask 3.0 |
| **Python** | 3.11.13 (conda environment) |

## 📊 System Stats

- **Total Lines**: ~2,000
- **Agent Modules**: 8 files (including re-ranker)
- **Core System**: 315 lines
- **Web Interface**: 300+ lines
- **Re-ranker**: 250+ lines (optional)
- **Knowledge Base**: ~29 files, 485 chunks (Enhanced!)
- **Response Time**: <2s with RAG (RAG + re-ranker: <2.5s)
- **Re-ranking Latency**: ~100-200ms (TinyBERT model)
- **Distress Detection**: Simplified weighted scoring system 
  - **HIGH keywords**: Crisis-level patterns (weight: 5 points)
  - **MILD keywords**: General support patterns (weight: 1 point)
  - **Intensity modifiers**: Adverbs (1.5x), punctuation (+2), ALL CAPS (+3)
  - **Score thresholds**: HIGH ≥5, MILD 1-4, NONE 0

## 🧪 Sample Queries

Try these in the web interface:

**🔴 HIGH Distress (triggers immediate empathy + numbered menu):**
- "i dont feel good"
- "I can't cope anymore"
- "I'm overwhelmed"
- "feel terrible"
- "breaking down"
- "can't handle this"

**� MILD Distress (triggers friendly support + bullet points):**
- "I'm struggling"
- "feeling sad"
- "feeling anxious"
- "having a hard time"
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
2. **Activate environment**: `conda activate mentalhealth_py311` or `source activate_env.sh`
3. **Start the app**: `python run_web.py`
4. **Open browser**: http://localhost:5001
5. **Start chatting!**

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

---

**Ready to start?** → See [QUICKSTART.md](QUICKSTART.md)

**Need technical details?** → See [GUIDE.md](GUIDE.md)

**Questions?** Open an issue on GitHub.
