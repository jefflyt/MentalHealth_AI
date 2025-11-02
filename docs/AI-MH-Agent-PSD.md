# AI Mental Health Agent - Project Specification Document (PSD)

**Project:** AI Mental Health Support Agent - Multi-Agent RAG System  
**Version:** 1.0  
**Date:** October 31, 2025  
**Framework:** LangGraph Multi-Agent System with RAG  

---

## 1. Project Overview

### 1.1 Project Summary
**Objective:** Develop a multi-agent AI system using LangGraph and RAG to provide anonymous, accessible mental health support for Singapore youth.

**Core Problem:** 30.6% of Singapore youth experience severe mental health symptoms with significant barriers to accessing support including stigma, cost, and limited availability.

**Solution:** Domain-agnostic multi-agent system adapted for mental health domain with intelligent routing through specialized agents.

### 1.2 Technical Architecture
**Core Stack:**
- **Orchestration:** LangGraph
- **LLM:** Groq with Llama 3.3 70B 
- **Embeddings:** HuggingFace all-mpnet-base-v2
- **Vector DB:** Chroma
- **Framework:** RAG (Retrieval-Augmented Generation)

### 1.3 Success Criteria
- [ ] Accurate query routing to appropriate agents (>85% accuracy)
- [ ] Crisis detection with zero false negatives
- [ ] RAG-based responses with relevant context
- [ ] Multi-step DASS-21 assessment workflow
- [ ] Human escalation for ambiguous cases
- [ ] LangGraph workflow executes without errors

---

## 2. System Architecture

### 2.1 Multi-Agent Design

```
┌─────────────────────────────────────────────────────────────┐
│                    USER QUERY INPUT                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   ROUTER NODE                                │
│ • Crisis keyword detection (priority)                        │
│ • LLM semantic classification                                │
│ • Confidence scoring (threshold: 0.6)                        │
└─────┬───────┬─────────┬─────────┬──────────┬────────────────┘
      │       │         │         │          │
      ▼       ▼         ▼         ▼          ▼
┌─────────┐ ┌─────┐ ┌─────────┐ ┌─────────┐ ┌──────────────┐
│ CRISIS  │ │INFO │ │RESOURCE │ │ASSESS   │ │HUMAN         │
│INTERV.  │ │AGENT│ │ AGENT   │ │ AGENT   │ │ESCALATION    │
└─────────┘ └─────┘ └─────────┘ └─────────┘ └──────────────┘
```

### 2.2 Agent Specifications

#### 2.2.1 Router Node
- **Function:** `router_node(state: AgentState) -> AgentState`
- **Inputs:** User query string
- **Processing:**
  1. Crisis keyword detection (highest priority)
  2. LLM semantic classification
  3. Confidence scoring
  4. Route determination
- **Outputs:** Updated state with `next_node` and `routing_confidence`

#### 2.2.2 Crisis Intervention Agent
- **Function:** `crisis_intervention_node(state: AgentState) -> AgentState`
- **Triggers:** Crisis keywords detected OR explicit crisis classification
- **Keywords:** ["kill myself", "want to die", "end it all", "hurt myself", "suicide", "not worth living", ...]
- **Response:** Immediate emergency resources (IMH: 6389-2222, Samaritans: 1767, Emergency: 995)
- **Priority:** Highest (bypasses normal routing)

#### 2.2.3 Information Agent
- **Function:** `information_agent_node(state: AgentState) -> AgentState`
- **Purpose:** Educational mental health information
- **RAG Source:** `mental_health_info` collection
- **Retrieval:** Top-K=3 relevant chunks
- **Response Style:** Educational, empathetic, evidence-based

#### 2.2.4 Resource Agent
- **Function:** `resource_agent_node(state: AgentState) -> AgentState`
- **Purpose:** Singapore mental health services and resources
- **RAG Source:** `singapore_resources` collection
- **Retrieval:** Top-K=4 relevant resources
- **Content:** IMH, CHAT, Samaritans, school counseling

#### 2.2.5 Assessment Agent
- **Function:** `assessment_agent_node(state: AgentState) -> AgentState`
- **Purpose:** Multi-step DASS-21 mental health screening
- **Workflow:** 21 questions (7 depression + 7 anxiety + 7 stress)
- **State Tracking:** `assessment_step` and `assessment_data`
- **Output:** Risk scores and recommendations

#### 2.2.6 Human Escalation Agent
- **Function:** `human_escalation_node(state: AgentState) -> AgentState`
- **Triggers:** 
  - Routing confidence < 0.6
  - Explicit human help requests
  - Ambiguous queries
- **Response:** Professional mental health service information

### 2.3 State Management

```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[dict], add_messages]
    user_query: str
    next_node: str
    crisis_detected: bool
    assessment_step: int
    assessment_data: dict
    routing_confidence: float
    retrieved_context: str
```

---

## 3. Knowledge Base Architecture

### 3.1 Data Categories
```
data/
├── mental_health_info/
│   ├── depression_info.txt
│   ├── anxiety_info.txt
│   └── stress_info.txt
├── coping_strategies/
│   ├── breathing_exercises.txt
│   ├── mindfulness_techniques.txt
│   └── cognitive_strategies.txt
├── singapore_resources/
│   ├── imh_services.txt
│   ├── chat_services.txt
│   └── community_resources.txt
├── dass21_guidelines/
│   └── dass21_framework.txt
└── crisis_protocols/
    └── crisis_intervention.txt
```

### 3.2 Vector Database Structure
```
chroma_db/
├── mental_health_info/     # Educational content
├── coping_strategies/      # Evidence-based techniques
├── singapore_resources/    # Local services
├── dass21_guidelines/      # Assessment framework
└── crisis_protocols/       # Emergency procedures
```

### 3.3 Chunking Strategy
- **Chunk Size:** 500 tokens
- **Overlap:** 100 tokens
- **Strategy:** Recursive splitting (\n\n → \n → . → space)
- **Rationale:** Balance context preservation with retrieval precision

---

## 4. Implementation Specifications

### 4.1 Core Dependencies
```
langgraph>=0.0.30
langchain>=0.1.0
langchain-groq>=0.1.0
groq>=0.4.0
chromadb>=0.4.22
sentence-transformers>=2.2.0
python-dotenv>=1.0.0
tiktoken>=0.5.2
numpy>=1.24.0
pandas>=2.1.0
```

### 4.2 Environment Configuration
```bash
# Required API Key
GROQ_API_KEY=your_groq_api_key_here
```

### 4.3 File Structure
```
ai-mental-health-agent/
├── ingestion.py                # Knowledge base ingestion
├── app.py                      # LangGraph application
├── requirements.txt            # Dependencies
├── README.md                   # Documentation
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── data/                      # Raw knowledge base
├── chroma_db/                 # Vector database
├── utils/                     # Helper modules
└── tests/                     # Test scripts
```

---

## 5. Implementation Tasks

### 5.1 Phase 1: Knowledge Base Setup

#### Task 1.1: Data Preparation
- [ ] Create `/data/` directory structure
- [ ] Populate mental health information files
- [ ] Add Singapore-specific resource content
- [ ] Include DASS-21 assessment guidelines
- [ ] Add crisis intervention protocols

#### Task 1.2: Ingestion Pipeline (`ingestion.py`)
- [ ] Implement `load_documents_from_directory()`
- [ ] Implement `chunk_documents()` with recursive splitting
- [ ] Initialize SentenceTransformer('all-mpnet-base-v2')
- [ ] Implement `create_vector_store()` with Chroma
- [ ] Implement `persist_database()` with collection management
- [ ] Test ingestion pipeline with all categories

**Acceptance Criteria:**
```bash
# Expected output
============================================================
Processing category: mental_health_info
============================================================
Loaded 3 documents
Created 15 chunks
Creating vector store for collection: mental_health_info
Number of chunks: 15
Vector store saved to: chroma_db/mental_health_info
```

### 5.2 Phase 2: LangGraph Architecture

#### Task 2.1: State and LLM Setup
- [ ] Define `AgentState` TypedDict with all required fields
- [ ] Initialize ChatGroq with llama-3.3-70b-versatile
- [ ] Initialize SentenceTransformer embeddings
- [ ] Load Chroma vector stores for all collections
- [ ] Test LLM connectivity and embedding generation

#### Task 2.2: Crisis Detection System
- [ ] Define comprehensive crisis keywords list (13+ variations)
- [ ] Implement `detect_crisis()` function
- [ ] Test crisis detection with positive/negative cases
- [ ] Ensure zero false negatives requirement

**Test Cases:**
```python
assert detect_crisis("I want to kill myself") == True
assert detect_crisis("I'm killing time") == False  # Acceptable false positive
assert detect_crisis("end it all") == True
assert detect_crisis("not worth living") == True
```

#### Task 2.3: RAG Retrieval System
- [ ] Implement `retrieve_context()` function
- [ ] Support category-specific retrieval
- [ ] Configure Top-K retrieval (K=3-5)
- [ ] Test semantic search across all collections
- [ ] Validate context relevance and quality

#### Task 2.4: Router Implementation
- [ ] Implement `router_node()` with crisis priority
- [ ] Create LLM classification prompt
- [ ] Parse confidence scores from LLM response
- [ ] Implement confidence threshold logic (0.6)
- [ ] Test routing accuracy across query types

**Test Routing:**
```python
# Information queries → information_agent
# Resource queries → resource_agent  
# Assessment queries → assessment_agent
# Crisis queries → crisis_intervention
# Ambiguous queries → human_escalation
```

### 5.3 Phase 3: Agent Implementation

#### Task 3.1: Crisis Intervention Agent
- [ ] Implement `crisis_intervention_node()`
- [ ] Create emergency response template
- [ ] Include all crisis hotlines (IMH: 6389-2222, SOS: 1767, Emergency: 995)
- [ ] Test crisis response generation
- [ ] Validate compassionate tone

#### Task 3.2: Information Agent
- [ ] Implement `information_agent_node()`
- [ ] Integrate RAG retrieval from mental_health_info
- [ ] Create empathetic response prompt template
- [ ] Test educational response quality
- [ ] Ensure no medical diagnosis claims

#### Task 3.3: Resource Agent
- [ ] Implement `resource_agent_node()`
- [ ] Integrate RAG retrieval from singapore_resources
- [ ] Create resource recommendation prompt template
- [ ] Test Singapore-specific resource accuracy
- [ ] Format responses with clear contact information

#### Task 3.4: Assessment Agent
- [ ] Implement `assessment_agent_node()` with multi-step logic
- [ ] Create DASS-21 question bank (21 questions)
- [ ] Implement state tracking for assessment progress
- [ ] Create scoring calculation functions
- [ ] Generate risk-appropriate recommendations

#### Task 3.5: Human Escalation Agent
- [ ] Implement `human_escalation_node()`
- [ ] Create professional referral template
- [ ] Include multiple service options
- [ ] Test ambiguous query handling

### 5.4 Phase 4: Workflow Construction

#### Task 4.1: Graph Building
- [ ] Create StateGraph(AgentState)
- [ ] Add all agent nodes
- [ ] Set router as entry point
- [ ] Configure conditional edges from router
- [ ] Add terminal edges to END
- [ ] Compile workflow graph

#### Task 4.2: Testing Interface
- [ ] Implement `run_agent()` console interface
- [ ] Add conversation history display
- [ ] Show routing decisions and confidence scores
- [ ] Test all agent types with sample queries
- [ ] Validate error handling

---

## 6. Testing Specifications

### 6.1 Unit Tests

#### Test Suite 1: Crisis Detection
```python
def test_crisis_detection():
    assert detect_crisis("I want to kill myself") == True
    assert detect_crisis("want to die") == True
    assert detect_crisis("end it all") == True
    assert detect_crisis("hurt myself") == True
    assert detect_crisis("not worth living") == True
    assert detect_crisis("Hello there") == False
```

#### Test Suite 2: Router Classification
```python
def test_router_classification():
    # Information queries
    assert route_query("What is depression?") == "information_agent"
    assert route_query("How to manage anxiety?") == "information_agent"
    
    # Resource queries
    assert route_query("Where can I get help?") == "resource_agent"
    assert route_query("Free mental health services?") == "resource_agent"
    
    # Assessment queries
    assert route_query("Check my mental health") == "assessment_agent"
    assert route_query("Take a screening") == "assessment_agent"
    
    # Crisis queries (highest priority)
    assert route_query("I want to kill myself") == "crisis_intervention"
```

#### Test Suite 3: RAG Retrieval
```python
def test_rag_retrieval():
    context = retrieve_context("depression symptoms", "mental_health_info", k=3)
    assert len(context) > 0
    assert "depression" in context.lower()
    
    resources = retrieve_context("help Singapore", "singapore_resources", k=3)
    assert "IMH" in resources or "CHAT" in resources
```

### 6.2 Integration Tests

#### Test Suite 4: End-to-End Workflow
```python
def test_workflow_execution():
    state = {
        "user_query": "What is anxiety?",
        "messages": [],
        "next_node": "",
        "crisis_detected": False,
        "assessment_step": 0,
        "assessment_data": {},
        "routing_confidence": 0.0,
        "retrieved_context": ""
    }
    
    result = app.invoke(state)
    assert len(result["messages"]) > 0
    assert "anxiety" in result["messages"][-1]["content"].lower()
```

### 6.3 Performance Tests

#### Test Suite 5: Response Times
- [ ] Router classification: < 2 seconds
- [ ] RAG retrieval: < 1 second
- [ ] Complete workflow: < 5 seconds
- [ ] Vector store loading: < 10 seconds

### 6.4 Safety Tests

#### Test Suite 6: Crisis Handling
- [ ] Zero false negatives on crisis keywords
- [ ] Immediate crisis resource display
- [ ] No harmful advice generation
- [ ] Appropriate escalation triggers

---

## 7. Quality Assurance

### 7.1 Code Quality Standards
- [ ] PEP 8 compliance
- [ ] Comprehensive docstrings
- [ ] Type hints for all functions
- [ ] Error handling for API failures
- [ ] Modular, single-responsibility functions

### 7.2 Documentation Requirements
- [ ] README.md with setup instructions
- [ ] API key configuration guide
- [ ] System architecture diagram
- [ ] Design rationale documentation
- [ ] Testing procedures

### 7.3 Security Considerations
- [ ] API key protection (.env files)
- [ ] No sensitive data in code
- [ ] Input sanitization
- [ ] Safe RAG context handling
- [ ] Crisis data privacy

---

## 8. Deployment Specifications

### 8.1 Environment Requirements
- **Python:** 3.9+
- **Memory:** 4GB+ (for sentence transformers)
- **Storage:** 2GB+ (for vector database)
- **Network:** Internet access for Groq API

### 8.2 Installation Procedure
```bash
# 1. Clone repository
git clone <repository_url>
cd ai-mental-health-agent

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with GROQ_API_KEY

# 5. Build knowledge base
python ingestion.py

# 6. Run application
python app.py
```

### 8.3 Verification Steps
```bash
# Expected: Vector database created
ls chroma_db/
# Should show: mental_health_info/ coping_strategies/ singapore_resources/ dass21_guidelines/ crisis_protocols/

# Expected: Application starts
python app.py
# Should show: AI MENTAL HEALTH SUPPORT AGENT console
```

---

## 9. Risk Management

### 9.1 Technical Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| API failures | High | Error handling, fallback responses |
| Model hallucinations | High | RAG grounding, response validation |
| Vector DB corruption | Medium | Backup procedures, rebuild capability |
| Dependency conflicts | Low | Virtual environments, pinned versions |

### 9.2 Safety Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| Missed crisis queries | Critical | Comprehensive keyword list, LLM backup |
| Harmful advice | High | No diagnosis claims, professional referrals |
| Privacy breach | Medium | Local processing, no data storage |
| System downtime | Medium | Clear limitations, human alternatives |

### 9.3 Ethical Considerations
- [ ] Clear AI system limitations
- [ ] No medical diagnosis claims
- [ ] Professional help encouragement
- [ ] Cultural sensitivity (Singapore context)
- [ ] Privacy protection (anonymous system)

---

## 10. Success Metrics

### 10.1 Functional Metrics
- [ ] **Router Accuracy:** >85% correct agent classification
- [ ] **Crisis Detection:** 100% recall (zero false negatives)
- [ ] **RAG Relevance:** >80% contextually relevant retrievals
- [ ] **Response Quality:** >80% empathetic, helpful responses
- [ ] **System Reliability:** >95% uptime during testing

### 10.2 Performance Metrics
- [ ] **Response Time:** <5 seconds end-to-end
- [ ] **Memory Usage:** <4GB during operation
- [ ] **Token Efficiency:** <1000 tokens per query average
- [ ] **Vector Search:** <500ms retrieval time

### 10.3 User Experience Metrics
- [ ] **Ease of Use:** Clear console interface
- [ ] **Help Accessibility:** Immediate crisis resources
- [ ] **Information Quality:** Evidence-based responses
- [ ] **Resource Accuracy:** Up-to-date Singapore services

---

## 11. Maintenance Plan

### 11.1 Regular Updates
- [ ] **Monthly:** Review crisis keyword list
- [ ] **Quarterly:** Update Singapore resource information
- [ ] **Bi-annually:** Retrain models if needed
- [ ] **Annually:** Full system architecture review

### 11.2 Monitoring
- [ ] Log all crisis detections
- [ ] Track routing confidence scores
- [ ] Monitor API usage and costs
- [ ] Review user interaction patterns

### 11.3 Improvement Areas
- [ ] Enhanced crisis detection models
- [ ] Multilingual support (Mandarin, Malay, Tamil)
- [ ] Sentiment analysis integration
- [ ] Web interface development
- [ ] Conversation history tracking

---

## 12. Project Timeline

### Phase 1: Foundation (Week 1-2)
- [ ] Environment setup and dependencies
- [ ] Knowledge base preparation
- [ ] Ingestion pipeline development
- [ ] Vector database construction

### Phase 2: Core Development (Week 3-4)
- [ ] LangGraph architecture implementation
- [ ] Crisis detection system
- [ ] RAG retrieval system
- [ ] Router node development

### Phase 3: Agent Implementation (Week 5-6)
- [ ] All five agent nodes
- [ ] Multi-step assessment workflow
- [ ] Response generation systems
- [ ] Error handling

### Phase 4: Integration & Testing (Week 7-8)
- [ ] Workflow construction and compilation
- [ ] Comprehensive testing suite
- [ ] Performance optimization
- [ ] Documentation completion

### Phase 5: Deployment & Validation (Week 9-10)
- [ ] System deployment
- [ ] End-to-end validation
- [ ] Safety testing
- [ ] Final documentation

---

## 13. Appendices

### Appendix A: Crisis Keywords List
```python
CRISIS_KEYWORDS = [
    "kill myself", "want to die", "end it all", "commit suicide",
    "hurt myself", "cut myself", "self harm", "not worth living",
    "better off dead", "end my life", "take my own life",
    "no reason to live", "can't go on", "suicide", "suicidal"
]
```

### Appendix B: DASS-21 Question Framework
- **Depression Questions:** 7 items (sadness, hopelessness, worthlessness)
- **Anxiety Questions:** 7 items (panic, fear, worry)
- **Stress Questions:** 7 items (tension, irritability, impatience)

### Appendix C: Singapore Mental Health Resources
- **IMH Emergency:** 6389-2222 (24/7)
- **Samaritans:** 1767 (24/7)
- **CHAT:** 6493-6500 (Weekdays 1pm-9pm)
- **Emergency Services:** 995

### Appendix D: Response Templates
#### Crisis Response Template:
```
🚨 **CRISIS SUPPORT AVAILABLE NOW** 🚨

I can hear that you're in a lot of pain right now. Your life matters, and there are people who want to help you immediately.

**Please reach out to these crisis services RIGHT NOW:**

📞 **IMH Emergency Helpline (24/7)**
   Phone: 6389-2222
   Immediate psychiatric emergency support

📞 **Samaritans of Singapore (24/7)**
   Phone: 1767
   Confidential emotional support

📞 **Emergency Services**
   Phone: 995
   For immediate life-threatening situations
```

---

**Document Status:** APPROVED FOR IMPLEMENTATION  
**Next Review:** November 15, 2025  
**Implementation Lead:** [To be assigned]  
**Technical Reviewer:** [To be assigned]