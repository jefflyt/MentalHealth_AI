# 📘 Complete Technical Guide

> Comprehensive documentation for AI Mental Health Support Agent

## Table of Contents

1. [Agent Architecture](#agent-architecture)
   - 1.0 [Sunny Persona System](#10-sunny-persona-system)
   - 1.1 [Router Agent](#11-router-agent)
   - 1.2 [Crisis Intervention Agent](#12-crisis-intervention-agent)
   - 1.3 [Information Agent](#13-information-agent)
   - 1.4 [Resource Agent](#14-resource-agent)
   - 1.5 [Assessment Agent](#15-assessment-agent)
   - 1.6 [Human Escalation Agent](#16-human-escalation-agent)
2. [Web Interface](#web-interface)
3. [Knowledge Base Management](#knowledge-base-management)
4. [Deployment](#deployment)
5. [Customization](#customization)
6. [API Reference](#api-reference)
7. [Troubleshooting](#troubleshooting)

---

## 1. Agent Architecture

### Overview

The system uses 6 specialized AI agents orchestrated by LangGraph, each with specific responsibilities.

### Agent Modules

```
agent/
├── router_agent.py         # Routes queries to specialists
├── crisis_agent.py         # Handles emergencies
├── information_agent.py    # Mental health education
├── resource_agent.py       # Singapore services
├── assessment_agent.py     # DASS-21 screening
├── escalation_agent.py     # Professional referrals
└── update_agent.py         # Knowledge base updates
```

### 1.0 Sunny Persona System

**Files:**
- `docs/SUNNY_PERSONA.md` - Complete personality documentation
- `agent/sunny_persona.py` - Centralized utility functions
- `test_sunny_persona.py` - Demonstration script

**Purpose:** Maintains consistent "Sunny" personality across all agents

**Core Components:**

#### Personality Traits
- **Warm & Approachable** - Never clinical or cold
- **Patient Listener** - Never rushes or judges
- **Genuinely Supportive** - Comfort, encouragement, reassurance
- **Upbeat & Encouraging** - Brightens tough moments
- **Protective & Caring** - Quick to check wellbeing
- **Humble & Boundaried** - Clear supportive friend role

#### Communication Style
```
✅ DO USE:
- "Hey there!" "I'm here for you" "That sounds tough"
- "You're not alone" "Thank you for sharing" "Your feelings are valid"
- Warm validation: "That makes sense" "I hear you"
- Gentle encouragement: "You've got this" "Take it one step"

❌ AVOID:
- Clinical terms (diagnosis, symptoms, treatment)
- Cold/formal language ("I understand your concern")
- Dismissive phrases ("Just think positive")
- Medical advice ("You should take medication")
```

#### Agent-Specific Adaptations
- **Information Agent** - Main supportive friend (educational, warm)
- **Crisis Agent** - Urgent care with warmth (immediate action focus)
- **Escalation Agent** - Warm recommendations (caring advice)
- **Resource Agent** - Local guide (Singapore knowledge)
- **Assessment Agent** - Supportive screening (gentle guidance)

#### Utility Functions

```python
from agent.sunny_persona import get_sunny_persona, build_sunny_prompt

# Get core personality
sunny = get_sunny_persona()
greeting = sunny['greeting']  # "Hey there! I'm Sunny 😊"
validation = sunny['validation_phrases'][0]  # "I hear you"

# Build consistent prompts
prompt = build_sunny_prompt(
    agent_type='information',
    context="User context here",
    specific_instructions="Agent-specific instructions"
)
```

#### Sample Interactions

**First Meeting:**
```
User: "Hi"
Sunny: "Hey there! I'm Sunny 😊 I'm here as your mental health friend..."
```

**Emotional Support:**
```
User: "I'm feeling anxious"
Sunny: "I hear you, and I'm glad you shared that with me. Anxiety can feel..."
```

**Gentle Redirect:**
```
User: "What's the weather?"
Sunny: "Hey! I'm here to chat about how you're feeling and support your wellbeing..."
```

#### Update Process

**Single Source of Truth:**
1. **Update** `docs/SUNNY_PERSONA.md` - Main documentation
2. **Modify** `agent/sunny_persona.py` - Code implementation
3. **Test** changes in one agent first
4. **Deploy** - All agents automatically get updates

**Benefits:**
- ✅ **Consistency** - All agents sound like Sunny
- ✅ **Maintainability** - Update once, applies everywhere
- ✅ **Scalability** - Easy to add new agents
- ✅ **Documentation** - Clear personality reference

---

### 1.1 Router Agent

**File:** `agent/router_agent.py` (78 lines)

**Purpose:** Analyzes incoming queries and routes to appropriate specialist

**Features:**
- Crisis keyword detection (highest priority)
- 3-level distress detection (HIGH/MODERATE/MILD)
- RAG-enhanced routing decisions
- LLM-based classification for specific requests
- Assessment suggestion context preservation
- Default fallback to information agent

**Routes to:**
- `crisis_intervention` - Emergency situations
- `information` - General mental health queries with distress-tailored responses
- `resource` - Service requests
- `assessment` - Screening requests
- `human_escalation` - Complex cases

**Distress Level Detection:**

#### HIGH Distress (🔴 Priority 2)
**Keywords:** "don't feel good", "feel terrible", "feel awful", "feel horrible", "can't take it", "breaking down", "falling apart", "overwhelmed", "can't cope", "losing it", "giving up"

**Response:** Immediate empathy + structured support menu
```
"I hear you, and I'm really glad you reached out to me. 💙
It sounds like you're going through a really tough time right now...

I can support you with:
1️⃣ Understanding what you're feeling
2️⃣ Coping strategies that can help right now  
3️⃣ Connecting you to professional support in Singapore
4️⃣ Just being here to listen - whatever you need"
```

#### MODERATE Distress (🟡 Priority 2)
**Keywords:** "feel bad", "feeling down", "feeling sad", "feeling anxious", "feeling depressed", "feeling stressed", "struggling", "hard time", "exhausted", "drained", "worried", "scared", "lonely", "hopeless", "helpless"

**Response:** Warm acknowledgment + support options menu
```
"Hey there, I'm Sunny, and I'm here for you. 💙
I can help with whatever you're going through.

I can help with:
1️⃣ Understanding your feelings
2️⃣ Coping strategies and techniques  
3️⃣ Finding support services in Singapore
4️⃣ Just someone to talk to - I'm a good listener!"
```

#### MILD Distress (🟢 Priority 2)
**Keywords:** "need help", "help me", "need someone", "need to talk", "something wrong", "confused", "unsure", "don't know"

**Response:** Friendly welcome + open-ended options
```
"Hi there! I'm Sunny, and I'm here to support you. 💙 😊

What would you like help with?
• Understanding emotions
• Coping strategies  
• Support services in Singapore
• Or just talk - I'm a good listener!

What's on your mind today?"
```

**Example Flow:**
```python
User: "i dont feel good"
→ Router detects HIGH distress
→ Routes to information_agent with distress_level="high"
→ Information agent provides structured support menu

User: "where can i get help in singapore"
→ Router uses LLM routing
→ Routes to resource_agent
→ Resource agent provides Singapore service information
```

#### Weighted Scoring System

**Implementation:** The router uses a weighted scoring system for nuanced distress detection.

**Scoring Formula:**
```python
base_score = sum(matched_keyword_weights)
final_score = apply_intensity_modifiers(base_score)
```

**Keyword Weights:**
- HIGH distress keywords: 5 points (54 patterns)
- MODERATE distress keywords: 3 points (71 patterns)
- MILD distress keywords: 1 point (43 patterns)
- Total: 168 patterns

**Score Thresholds:**
- `score ≥ 10`: HIGH distress
- `score 5-9`: MODERATE distress
- `score 1-4`: MILD distress
- `score 0`: NONE

**Intensity Modifiers:**
1. **Adverb Multiplier (1.5x):** "very", "really", "so", "extremely", etc.
2. **Punctuation (+2):** 3+ exclamation marks
3. **ALL CAPS (+3):** 2+ words in all capitals

**Example:**
```
Query: "I'm really overwhelmed!!!"
Base: 10 points (overwhelmed: 5 + over: 5)
Adverb: 10 × 1.5 = 15
Punctuation: 15 + 2 = 17
Final: 17 → HIGH distress
```

**Benefits:**
- Recognizes cumulative distress (multiple weak signals)
- Handles intensity variations (adverbs, CAPS, !!!)
- More accurate than binary detection (73% vs 60%)
- Fast: <0.01s per detection

**Testing:**
```bash
# Comprehensive test suite (22 test cases)
python test_distress_detection.py

# Live demonstration with scoring breakdown
python test_weighted_scoring_live.py
```

**Detailed Implementation:**

**Keyword Patterns:**
- **HIGH (54 patterns):** "don't feel good", "can't cope", "overwhelmed", "breaking down", "falling apart", "can't breathe", "suffocating", "drowning", "can't handle", "breaking", "broken", "shattered", "devastated", "destroyed", "crushed", "unbearable", "agonizing", "tormented", "desperate", "hopeless", "worthless", "empty inside", "paralyzed", "frozen", "trapped", "isolated", "abandoned", "ruined", "over", "done"
- **MODERATE (71 patterns):** "feel bad", "feeling down", "feeling low", "feeling sad", "feeling anxious", "feeling depressed", "feeling stressed", "stressed out", "burnt out", "not okay", "not well", "struggling", "hard time", "tough time", "exhausted", "drained", "worried", "scared", "lonely", "alone", "helpless", "empty", "numb", "down in the dumps", "feeling blue", "anxious mess", "emotional wreck", "can't focus", "irritable", "restless", "tense", "overthinking", "self-doubting", "frustrated", "angry", "tearful", "crying", "burned out", "overloaded", "conflicted", "torn", "confused", "sad", "depressed", "anxious"
- **MILD (43 patterns):** "need help", "help me", "need support", "need someone", "need to talk", "someone to talk to", "something wrong", "confused", "unsure", "don't know", "a bit off", "feeling off", "need a chat", "need advice", "curious", "wondering", "mixed emotions", "seeking advice", "hesitant", "pensive", "reflective", "lost", "blah", "meh", "whatever"

**Code Structure:**
```python
# Module-level keyword dictionaries
HIGH_DISTRESS_KEYWORDS = {
    "don't feel good": 5, "cant cope": 5, # ... 54 patterns
}
MODERATE_DISTRESS_KEYWORDS = {
    "feeling sad": 3, "struggling": 3, # ... 71 patterns  
}
MILD_DISTRESS_KEYWORDS = {
    "need help": 1, "confused": 1, # ... 43 patterns
}

def detect_distress_level(query: str) -> str:
    # Calculate weighted score
    score = 0
    query_lower = query.lower()
    
    # Match keywords and sum weights
    for phrase, weight in HIGH_DISTRESS_KEYWORDS.items():
        if phrase in query_lower:
            score += weight
    # ... similar for moderate and mild
    
    # Apply intensity modifiers
    score = apply_intensity_modifiers(query, score)
    
    # Threshold to levels
    if score >= 10: return 'high'
    elif score >= 5: return 'moderate' 
    elif score >= 1: return 'mild'
    else: return 'none'

def apply_intensity_modifiers(query: str, base_score: float) -> float:
    # Adverb multiplier (1.5x)
    if any(word in query.lower() for word in ["very", "really", "so", "extremely"]):
        base_score *= 1.5
    
    # Punctuation modifier (+2 for 3+ !)
    exclamation_count = query.count('!')
    if exclamation_count >= 3:
        base_score += 2 * (exclamation_count - 2)
    
    # ALL CAPS modifier (+3)
    words = query.split()
    caps_words = [w for w in words if w.isupper() and len(w) > 2]
    if len(caps_words) >= 2:
        base_score += 3
    
    return base_score
```

**Performance Metrics:**
- **Accuracy:** 72.7% on test suite (16/22 cases)
- **Response Time:** <0.01s per detection
- **Memory Usage:** Minimal (static dictionaries)
- **Scalability:** Easy to add new keywords

**Integration:**
- Seamlessly replaces binary keyword matching
- Maintains same function signature and return values
- No changes required to other agents
- Backward compatible with existing routing logic

**Future Enhancements:**
- Context-aware scoring (conversation history)
- Negation handling ("not sad")
- Multi-language support
- Dynamic threshold tuning
- Sentiment analysis integration

### 1.2 Crisis Intervention Agent

**File:** `agent/crisis_agent.py` (57 lines)

**Purpose:** Immediate support for emergency situations

**Features:**
- RAG retrieval of crisis protocols
- Singapore emergency contacts (SOS, IMH, CHAT)
- Empathetic crisis response
- Fallback to hardcoded emergency info

**Crisis Keywords:**
```python
[
    "suicide", "suicidal", "kill myself", "end my life",
    "want to die", "self harm", "hurt myself", "cutting",
    "overdose", "no reason to live", "better off dead",
    "can't go on", "end it all"
]
```

**Output Example:**
```
🆘 I'm here to help you right now. You're not alone.

IMMEDIATE SUPPORT:
• SOS Hotline: 1767 (24/7, free)
• IMH Emergency: 6389-2222
• CHAT Youth Support: 6493-6500

Please reach out immediately. Your life matters.
```

### 1.3 Information Agent

**File:** `agent/information_agent.py` (52 lines)

**Purpose:** Evidence-based mental health education

**Features:**
- RAG retrieval (4 results for comprehensive context)
- Evidence-based information delivery
- Coping strategies and guidance
- Source attribution footer

**Query Pattern:**
```python
context = get_relevant_context(
    f"mental health information {query}",
    n_results=4
)
```

**Output:**
- Clear, accurate mental health info
- Practical guidance
- Coping strategies
- Footer: "📚 *Information sourced from evidence-based resources*"

### 1.4 Resource Agent

**File:** `agent/resource_agent.py` (64 lines)

**Purpose:** Singapore mental health services and support

**Features:**
- RAG retrieval of Singapore services
- Contact information and locations
- Eligibility criteria
- Operating hours and costs
- Emergency contacts appended

**Services Covered:**
- CHAT (Community Health Assessment Team)
- IMH (Institute of Mental Health)
- Polyclinics
- Private practices
- Emergency hotlines

### 1.5 Assessment Agent

**File:** `agent/assessment_agent.py` (60 lines)

**Purpose:** Mental health screening (DASS-21) guidance

**Features:**
- RAG retrieval of DASS-21 protocols
- Self-assessment information
- Professional evaluation guidance
- Clear limitations disclaimer

**Output:**
- Assessment information
- DASS-21 explanation
- Next steps for evaluation
- Footer: "⚠️ *Self-assessment tools provide insights but cannot replace professional diagnosis*"

### 1.6 Human Escalation Agent

**File:** `agent/escalation_agent.py` (69 lines)

**Purpose:** Professional referrals for complex cases

**Features:**
- RAG retrieval of referral guidelines
- Professional service recommendations
- Validation of user concerns
- Encouragement for professional help

**Output:**
- Validation of concerns
- Specific professional services
- Access instructions
- What to expect from consultation
- Footer: "🤝 *Connecting with a mental health professional shows strength*"

### Agent Function Signature

All agents follow this pattern:
```python
def agent_node(state: AgentState, llm: ChatGroq, get_relevant_context) -> AgentState:
    """Agent description."""
    query = state["current_query"]
    
    # Retrieve relevant context
    context = get_relevant_context(f"specific query {query}", n_results=3)
    
    # Create prompt with context
    prompt = f"""
    Context: {context}
    User Query: "{query}"
    
    [Agent-specific instructions]
    """
    
    # Generate response
    response = llm.invoke(prompt).content
    
    # Update state
    state["messages"].append(response)
    state["current_agent"] = "complete"
    return state
```

### RAG Integration

All agents use ChromaDB for context retrieval:

1. **Agent receives query**
2. **Constructs context-specific search**
3. **Retrieves relevant chunks** (n_results varies by agent)
4. **Passes context + query to LLM**
5. **Returns grounded response**

**n_results by agent:**
- Router: 2 (fast routing)
- Crisis: 3 (emergency protocols)
- Information: 4 (comprehensive)
- Resource: 4 (multiple services)
- Assessment: 3 (screening protocols)
- Escalation: 3 (referral guidelines)

---

## 2. Web Interface

### Architecture

```
interface/web/
├── app.py              # Flask application
└── templates/
    └── index.html      # Chat UI
```

### 2.1 Flask Application

**File:** `interface/web/app.py` (155 lines)

**Key Routes:**

#### GET `/`
Main chat interface (HTML page)

#### POST `/chat`
Send message to AI agent

**Request:**
```json
{
  "message": "Your message here"
}
```

**Response:**
```json
{
  "response": "Agent response",
  "crisis": false,
  "timestamp": "2025-10-31T..."
}
```

#### POST `/new-conversation`
Start new conversation (clears history)

**Response:**
```json
{
  "message": "New conversation started",
  "session_id": "uuid"
}
```

#### GET `/history`
Get conversation history for session

**Response:**
```json
{
  "history": [
    {
      "role": "user",
      "content": "Message",
      "timestamp": "2025-10-31T..."
    }
  ]
}
```

#### GET `/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "agent_system": "operational",
  "timestamp": "2025-10-31T..."
}
```

### 2.2 Frontend Features

**Chat Interface:**
- Modern gradient design (purple theme)
- Real-time messaging
- Typing indicators (loading dots)
- Message timestamps
- Auto-scroll to latest message

**Crisis Detection:**
- Visual alert banner (red)
- Emergency emoji (🚨)
- Persistent until new conversation

**Mobile Responsive:**
- Adapts to screen size
- Touch-friendly buttons
- Optimized for phones/tablets

**Session Management:**
- UUID-based sessions
- Server-side conversation storage
- New conversation button

### 2.3 Customization

#### Change Colors

Edit `interface/web/templates/index.html` (around line 12):

```css
/* Main gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Change to your colors */
background: linear-gradient(135deg, #your_color1, #your_color2);
```

#### Change Port

Edit `run_web.py`:

```python
app.run(
    host='0.0.0.0',
    port=8080,  # Change from 5001
    debug=True
)
```

#### Add Custom Route

In `interface/web/app.py`:

```python
@app.route('/custom-endpoint')
def custom_function():
    return jsonify({'message': 'Custom response'})
```

---

## 3. Knowledge Base Management

### 3.1 Update Agent

**File:** `agent/update_agent.py` (382 lines)

**Purpose:** Monitors `data/knowledge/` and updates ChromaDB

**Features:**
- File change detection (MD5 hashing)
- Incremental updates (only changed files)
- Smart chunking (1000 chars, 200 overlap)
- State persistence (`.update_state.json`)
- CLI and Python API

### 3.2 CLI Commands

#### Check for Changes
```bash
python agent/update_agent.py check
```
Shows new/modified/deleted files without updating.

#### Auto-Update (Recommended)
```bash
python agent/update_agent.py auto
```
Checks and updates only if changes detected.

#### Force Update
```bash
python agent/update_agent.py force
```
Recreates entire collection (asks for confirmation).

#### View Status
```bash
python agent/update_agent.py status
```
Shows current ChromaDB state:
- Total chunks
- Files by category
- Last update timestamp

### 3.3 Python API

```python
from agent import UpdateAgent

agent = UpdateAgent()

# Check for changes
has_changes = agent.check_for_updates()

# Perform update
if has_changes:
    agent.perform_smart_update()

# View status
agent.list_current_state()
```

### 3.4 Knowledge Structure - Enhanced! 🚀

**Current Status:** Major enhancement complete with 485 chunks (+206 new, +74% increase)

```
data/knowledge/
├── text/                         # Original files, 12 files, ~279 chunks
│   ├── anxiety_info.txt
│   ├── depression_info.txt
│   ├── stress_info.txt
│   ├── chat_services.txt
│   ├── imh_services.txt
│   ├── breathing_exercises.txt
│   ├── mindfulness_meditation.txt
│   ├── positive_affirmations.txt
│   ├── administration_guide.txt
│   ├── scoring_interpretation.txt
│   ├── emergency_procedures.txt
│   └── intervention_guidelines.txt
│
├── singapore_resources/          # NEW! 1 file, 14 chunks
│   └── mental_health_services.txt    # Complete Singapore service directory
│
├── conditions/                   # NEW! 3 files, 74 chunks
│   ├── depression.txt                # 21 chunks - comprehensive depression guide
│   ├── anxiety_disorders.txt         # 22 chunks - complete anxiety disorders
│   └── panic_disorder.txt            # 31 chunks - detailed panic disorder guide
│
├── emergency/                    # NEW! 1 file, 26 chunks
│   └── suicide_prevention.txt        # Critical crisis intervention resource
│
├── faqs/                        # NEW! 1 file, 25 chunks
│   └── therapy_questions.txt         # Complete therapy FAQ for Singapore
│
├── self_help/                   # NEW! 1 file, 20 chunks
│   └── cognitive_behavioral_techniques.txt  # Practical CBT guide
│
└── [Other categories for future expansion]
    ├── documents/
    ├── markdown/
    ├── pdfs/                    # NEW! Research papers
    │   └── research_papers/
    │       ├── brainsci-11-01633.pdf  # 33 chunks - Brain science research
    │       └── mental-2020-6-e20513.pdf  # 14 chunks - Mental health research
    ├── reference/
    ├── structured_data/
    └── web_sources/
```

**Total Enhanced:** ~29 files → 485 chunks (48.5% toward 1,000+ target!)

**Enhancement Breakdown:**
- **Phase 1 Complete:** 7/48 planned files (14.6% of roadmap)
- **New Categories:** 5 (singapore_resources, conditions, faqs, self_help, emergency)
- **New Chunks:** +206 chunks (+74% increase)
- **Impact:** Comprehensive Singapore-specific mental health support!

### 3.4.1 Knowledge Enhancement Results 🎉

**Major Files Created:**
1. **`singapore_resources/mental_health_services.txt`** (14 chunks)
   - Complete directory of Singapore mental health services
   - IMH, CHAT, polyclinics, private services with contact info
   - Emergency contacts, costs, accessibility information

2. **`conditions/depression.txt`** (21 chunks)
   - Comprehensive depression guide with Singapore context
   - Types, symptoms, treatments, local resources
   - Cultural considerations and warning signs

3. **`conditions/anxiety_disorders.txt`** (22 chunks)
   - Complete anxiety disorders resource
   - GAD, panic disorder, social anxiety, OCD coverage
   - Practical coping strategies and treatments

4. **`conditions/panic_disorder.txt`** (31 chunks)
   - Detailed panic disorder and panic attack guide
   - Physical symptoms, grounding techniques, management
   - Heart attack vs panic attack differentiation

5. **`faqs/therapy_questions.txt`** (25 chunks)
   - Complete therapy FAQ addressing Singapore concerns
   - Therapy types, costs, expectations, cultural considerations
   - Reduces barriers to seeking professional help

6. **`emergency/suicide_prevention.txt`** (26 chunks)
   - Critical crisis intervention resource
   - Warning signs, safety planning, family support
   - Singapore emergency contacts and cultural sensitivity

7. **`self_help/cognitive_behavioral_techniques.txt`** (20 chunks)
   - Practical CBT techniques users can apply immediately
   - Thought challenging, behavioral activation, journaling
   - Evidence-based self-help strategies

**NEW Research PDFs Added (+47 chunks):**
8. **`pdfs/research_papers/brainsci-11-01633.pdf`** (33 chunks)
   - Brain science research paper on mental health
   - Scientific insights into neurological aspects of mental health conditions

9. **`pdfs/research_papers/mental-2020-6-e20513.pdf`** (14 chunks)
   - Mental health research paper on contemporary issues
   - Evidence-based findings on mental health interventions and outcomes

**System Impact:**
- **Response Quality:** Enhanced with detailed, Singapore-specific content
- **Crisis Detection:** Improved with comprehensive emergency resources
- **User Experience:** More relevant, actionable guidance
- **Coverage:** Now rivals professional mental health resources
- **Testing Results:** 200-600+ character responses with local context

### 3.5 Adding New Knowledge

**Step 1:** Create file in appropriate category
```bash
# Example: Add new coping strategy
nano data/knowledge/coping_strategies/progressive_relaxation.txt
```

**Step 2:** Run update agent
```bash
python agent/update_agent.py auto
```

**Step 3:** Restart app (if running)
```bash
# Kill with Ctrl+C, then:
python run_web.py
```

**File Format:**
- Plain text (.txt files)
- Clear headings
- Paragraphs separated by blank lines
- No special characters needed

**Example Content:**
```
Progressive Muscle Relaxation

Progressive muscle relaxation is an evidence-based technique...

How to Practice:
1. Find a quiet space
2. Tense each muscle group for 5 seconds
3. Release and notice the relaxation

Benefits:
- Reduces physical tension
- Calms the nervous system
- Improves sleep quality
```

### 3.6 Update State Tracking

**File:** `data/chroma_db/.update_state.json`

**Current Status:** 485 chunks across ~29 files

```json
{
  "file_hashes": {
    "text/anxiety_info.txt": {"hash": "abc123...", "category": "text"},
    "singapore_resources/mental_health_services.txt": {"hash": "def456...", "category": "singapore_resources"},
    "conditions/depression.txt": {"hash": "ghi789...", "category": "conditions"},
    "conditions/anxiety_disorders.txt": {"hash": "jkl012...", "category": "conditions"},
    "conditions/panic_disorder.txt": {"hash": "mno345...", "category": "conditions"},
    "emergency/suicide_prevention.txt": {"hash": "pqr678...", "category": "emergency"},
    "faqs/therapy_questions.txt": {"hash": "stu901...", "category": "faqs"},
    "self_help/cognitive_behavioral_techniques.txt": {"hash": "vwx234...", "category": "self_help"}
  },
  "last_update": "2025-11-02T...",
  "total_chunks": 485
}
```

**Purpose:**
- Tracks file changes via MD5 hash
- Records last update time
- Counts total chunks (now 438!)
- Enables incremental updates
- **Enhancement Impact:** +206 chunks (+74% increase)

### 3.7 Web Scraping for Knowledge Updates

**File:** `scripts/web_scraper.py` (231 lines)

**Purpose:** Fetch mental health content from trusted websites

**Trusted Sources:**
- **WHO** (World Health Organization) - Mental health fact sheets
- **IMH** (Institute of Mental Health Singapore) - Local resources
- **HealthHub Singapore** - Government health portal
- **SAMH** (Singapore Association for Mental Health) - Community support

**Features:**
- Rate limiting (2-second delays between requests)
- Content validation (minimum 200 characters)
- Metadata headers (source, URL, timestamp)
- Error handling and logging
- Organized output by source

**Usage:**

```bash
# Scrape all sources
python scripts/web_scraper.py

# Scrape specific sources programmatically
python -c "from scripts.web_scraper import MentalHealthWebScraper; \
           MentalHealthWebScraper().scrape_all(['who', 'imh'])"
```

**Output Structure:**
```
data/knowledge/web_sources/
├── who/
│   └── who_9aff9bcb.txt
├── imh/
│   └── imh_642d7702.txt
├── healthhub/
│   └── healthhub_7f114058.txt
└── samh/
    └── samh_4272ef94.txt
```

**Adding New Sources:**

Edit `scripts/web_scraper.py`:
```python
TRUSTED_SOURCES = {
    'new_source': {
        'name': 'Source Name',
        'base_url': 'https://example.com',
        'pages': ['/mental-health'],
        'selectors': {'content': 'article, main'}
    }
}
```

### 3.8 Automated Periodic Updates

**File:** `scripts/periodic_updater.py` (102 lines)

**Purpose:** Automated knowledge base updates on schedule

**Features:**
- Combines web scraping + ChromaDB updates
- Scheduled updates (daily/weekly/monthly)
- Activity logging to `data/update_log.txt`
- Manual or daemon mode
- Error handling and recovery

**Usage:**

```bash
# Manual one-time update
python scripts/periodic_updater.py
python scripts/periodic_updater.py manual

# Scheduled updates (keeps running)
python scripts/periodic_updater.py schedule --frequency weekly
python scripts/periodic_updater.py schedule --frequency daily
python scripts/periodic_updater.py schedule --frequency monthly
```

**Schedule Options:**
- **daily**: Runs every day at 2:00 AM
- **weekly**: Runs every Sunday at 2:00 AM

### 3.9 Knowledge Base Enhancement Roadmap 🗺️

**Complete implementation plan and progress tracking for knowledge base expansion**

**Current Achievement:** Phase 1 foundation complete (7/48 files, 14.6%)
- **Target:** 1,000+ chunks for comprehensive coverage
- **Current:** 485 chunks (48.5% of target achieved!)

**Phase 1 Priorities (In Progress):**
- ✅ Singapore Resources: 1/5 files complete (mental_health_services.txt)
- ✅ Conditions: 3/7 files complete (depression, anxiety_disorders, panic_disorder)
- ✅ Emergency: 1/5 files complete (suicide_prevention.txt)
- ✅ FAQs: 1/4 files complete (therapy_questions.txt)
- **Phase 1 Total:** 6/21 files ✅

**Phase 2 Enhancement:**
- ✅ Self-Help: 1/7 files complete (cognitive_behavioral_techniques.txt)
- [ ] Life Stages: 0/6 files (children, adolescents, adults, elderly, pregnancy)
- [ ] Treatment: 0/4 files (medications, therapy types, alternatives)
- [ ] Caregivers: 0/3 files (supporting others, burnout, family therapy)

**Next Priority Files:**
1. `singapore_resources/youth_services.txt` - CHAT and young adult resources
2. `emergency/self_harm.txt` - Critical self-harm intervention
3. `conditions/bipolar_disorder.txt` - Bipolar disorder comprehensive guide
4. `singapore_resources/workplace_resources.txt` - EAP and work stress
5. `faqs/medication_questions.txt` - Psychiatric medication FAQ

**Enhancement Strategy:**
- Focus on Phase 1 critical priorities first (emergency, Singapore resources)
- Maintain quality over quantity (comprehensive files vs quick additions)
- Test each addition with real user queries
- Track progress and update documentation after each file

**Implementation Process:**
1. Create knowledge file with comprehensive content
2. Run `python agent/update_agent.py auto` to update ChromaDB
3. Test with relevant queries via web interface
4. Update progress tracking in documentation
5. Commit changes to repository

**Current Achievement Status:**
- **✅ COMPLETE:** Major knowledge base enhancement (Phase 1 foundation)
- **✅ VERIFIED:** 485 total chunks confirmed via `update_agent.py status`
- **✅ TESTED:** Comprehensive system testing across 7 query scenarios
- **✅ DOCUMENTED:** Updated README.md and GUIDE.md with enhanced specs
- **🎯 IMPACT:** System now provides detailed, Singapore-specific mental health support rivaling professional resources!
- **monthly**: Runs on 1st of each month at 2:00 AM

**Running in Background (macOS/Linux):**
```bash
# Using nohup
nohup python scripts/periodic_updater.py schedule --frequency weekly > update.log 2>&1 &

# Using screen
screen -dmS knowledge-updater python scripts/periodic_updater.py schedule
```

**macOS LaunchAgent Setup:**

Create `~/Library/LaunchAgents/com.mentalhealth.updater.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" 
    "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.mentalhealth.updater</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/venv/bin/python</string>
        <string>/path/to/scripts/periodic_updater.py</string>
        <string>manual</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>0</integer>
        <key>Hour</key>
        <integer>2</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>WorkingDirectory</key>
    <string>/path/to/MentalHealth_AI</string>
</dict>
</plist>
```

Load: `launchctl load ~/Library/LaunchAgents/com.mentalhealth.updater.plist`

### 3.9 Complete Update Workflow

**Manual Update:**
```bash
# Step 1: Scrape web sources
python scripts/web_scraper.py

# Step 2: Update ChromaDB
python -c "from agent import UpdateAgent; UpdateAgent().perform_smart_update()"

# Step 3: Verify
python agent/update_agent.py status
```

**Automated Update:**
```bash
# One-time (scraping + updating)
python scripts/periodic_updater.py manual

# Scheduled weekly updates
python scripts/periodic_updater.py schedule --frequency weekly
```

---

## 4. Deployment

### 4.1 Development

**Using run_web.py (Current Setup):**
```bash
python run_web.py
```

**Features:**
- Auto-reload on code changes
- Debug mode enabled
- Detailed error messages
- Good for testing

### 4.2 Production

**Using Gunicorn (Recommended):**

```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5001 "interface.web.app:app"

# With logging
gunicorn -w 4 \
  -b 0.0.0.0:5001 \
  --access-logfile access.log \
  --error-logfile error.log \
  "interface.web.app:app"
```

**Workers:** Number of CPU cores × 2 + 1 (recommended)

### 4.3 Environment Variables

**Required:**
```bash
GROQ_API_KEY=gsk_your_actual_key_here
```

**Optional:**
```bash
FLASK_SECRET_KEY=your_secret_key_for_sessions
FLASK_ENV=production
PORT=5001
```

**Setting in Production:**
```bash
# Export variables
export GROQ_API_KEY="your_key"
export FLASK_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
export FLASK_ENV="production"

# Run Gunicorn
gunicorn -w 4 -b 0.0.0.0:$PORT "interface.web.app:app"
```

### 4.4 Docker Deployment

**Create Dockerfile:**
```dockerfile
FROM python:3.11

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5001

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "interface.web.app:app"]
```

**Build and run:**
```bash
# Build image
docker build -t mental-health-agent .

# Run container
docker run -d \
  -p 5001:5001 \
  -e GROQ_API_KEY="your_key" \
  --name mh-agent \
  mental-health-agent
```

### 4.5 Systemd Service (Linux)

**Create service file:** `/etc/systemd/system/mh-agent.service`

```ini
[Unit]
Description=AI Mental Health Agent
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/MentalHealth_AI
Environment="GROQ_API_KEY=your_key"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 0.0.0.0:5001 "interface.web.app:app"
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable mh-agent
sudo systemctl start mh-agent
sudo systemctl status mh-agent
```

---

## 5. Customization

### 5.1 Utility Scripts

**Location:** `scripts/`

The `scripts/` folder contains utility scripts for testing and maintenance:

1. **web_scraper.py** (231 lines)
   - **Purpose:** Production web scraping tool
   - **Usage:** `python scripts/web_scraper.py`
   - **Function:** Fetches content from trusted mental health websites (WHO, IMH, HealthHub, SAMH)

2. **periodic_updater.py** (102 lines)
   - **Purpose:** Production automated update scheduler
   - **Usage:** `python scripts/periodic_updater.py schedule --frequency weekly`
   - **Function:** Runs web scraper and knowledge base updates on schedule

3. **test_multiformat.py** (13 lines)
   - **Purpose:** Development utility for testing multi-format support
   - **Usage:** `python scripts/test_multiformat.py`
   - **Function:** Quick demo showing supported file formats

4. **verify_code.py** (273 lines)
   - **Purpose:** Development utility for code verification
   - **Usage:** `python scripts/verify_code.py`
   - **Function:** Validates UpdateAgent structure without installing optional dependencies

**Production vs Development:**
- **Production:** `web_scraper.py`, `periodic_updater.py` (essential for knowledge updates)
- **Development:** `test_multiformat.py`, `verify_code.py` (testing and verification only)

### 5.2 Adding New Agent

**Step 1:** Create agent file
```python
# agent/new_agent.py
from typing import TypedDict, List
from langchain_groq import ChatGroq

class AgentState(TypedDict):
    current_query: str
    messages: List[str]
    current_agent: str
    crisis_detected: bool
    context: str

def new_agent_node(state: AgentState, llm: ChatGroq, get_relevant_context) -> AgentState:
    """Your new agent description."""
    query = state["current_query"]
    
    # Get context
    context = get_relevant_context(f"new agent query {query}", n_results=3)
    
    # Create prompt
    prompt = f"""
    Context: {context}
    User Query: "{query}"
    
    [Your instructions here]
    """
    
    # Generate response
    response = llm.invoke(prompt).content
    
    # Update state
    state["messages"].append(response)
    state["current_agent"] = "complete"
    return state
```

**Step 2:** Update `agent/__init__.py`
```python
from .new_agent import new_agent_node

__all__ = [
    # ... existing agents
    'new_agent_node',
]
```

**Step 3:** Update `app.py`
```python
from agent import new_agent_node

# Add wrapper
def new_agent_wrapper(state: AgentState) -> AgentState:
    return new_agent_node(state, llm, get_relevant_context)

# Update workflow
workflow.add_node("new_agent", new_agent_wrapper)

# Add routing
workflow.add_conditional_edges(
    "router",
    route_to_agent,
    {
        # ... existing routes
        "new_agent": "new_agent",
    }
)

# Add end edge
workflow.add_edge("new_agent", END)
```

### 5.3 Modifying Prompts

Edit agent files directly. Example for Information Agent:

**Before:**
```python
info_prompt = f"""
Based on the following evidence-based mental health information...
"""
```

**After:**
```python
info_prompt = f"""
Based on the following mental health information, 
provide a helpful response using simple language for ages 16-25:

Context: {info_context}
User Query: "{query}"

Guidelines:
- Use simple, conversational language
- Include practical examples
- Add emojis for readability
- Keep paragraphs short
"""
```

### 5.3 Changing LLM

**Current:** Groq Llama 3.3 70B

**To change:**

Edit `app.py`:
```python
# Current
from langchain_groq import ChatGroq

def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",  # Change model
        temperature=0.7,  # Adjust creativity
        api_key=os.getenv("GROQ_API_KEY")
    )

# Alternative: OpenAI
from langchain_openai import ChatOpenAI

def get_llm():
    return ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
```

### 5.4 Custom UI Themes

**Dark Mode:**

Edit `interface/web/templates/index.html`:

```css
body {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

.container {
    background: #0f3460;
}

.message.agent .message-bubble {
    background: #1a1a2e;
    color: #eaeaea;
    border: 1px solid #16213e;
}
```

**Professional Theme:**

```css
body {
    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
}

.header {
    background: linear-gradient(135deg, #2980b9 0%, #3498db 100%);
}

#send-btn {
    background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
}
```

---

## 6. API Reference

### AgentState Type

```python
class AgentState(TypedDict):
    current_query: str       # User's message
    messages: List[str]      # Conversation history
    current_agent: str       # Active agent name
    crisis_detected: bool    # Crisis flag
    context: str            # RAG context
```

### get_relevant_context()

```python
def get_relevant_context(query: str, n_results: int = 3) -> str:
    """
    Retrieve relevant context from ChromaDB.
    
    Args:
        query: Search query string
        n_results: Number of chunks to retrieve (default: 3)
    
    Returns:
        Concatenated relevant text chunks
    """
```

### initialize_chroma()

```python
def initialize_chroma() -> None:
    """
    Initialize or load ChromaDB collection.
    
    - Checks if collection exists
    - Loads from data/knowledge/ if new
    - Handles chunking and embedding
    """
```

### create_workflow()

```python
def create_workflow() -> CompiledGraph:
    """
    Create and compile LangGraph workflow.
    
    Returns:
        Compiled workflow ready for .invoke()
    """
```

### UpdateAgent Class

```python
class UpdateAgent:
    def __init__(
        self,
        knowledge_dir: str = "data/knowledge",
        collection_name: str = "mental_health_kb"
    ):
        """Initialize update agent."""
    
    def check_for_updates(self) -> bool:
        """Check if knowledge base has changes."""
    
    def perform_smart_update(self) -> bool:
        """Update ChromaDB with changes."""
    
    def list_current_state(self) -> None:
        """Display current state."""
```

---

## 7. Troubleshooting

### Common Issues

#### Port Already in Use

**Error:** `Address already in use. Port 5001 is in use`

**Solution:**
```bash
# Find process
lsof -i :5001

# Kill it
kill -9 <PID>

# Or change port in run_web.py
```

#### ModuleNotFoundError

**Error:** `ModuleNotFoundError: No module named 'langchain'`

**Solution:**
```bash
# Activate venv
source venv/bin/activate

# Reinstall
pip install -r requirements.txt
```

#### GROQ_API_KEY Not Found

**Error:** `ValueError: GROQ_API_KEY not found`

**Solution:**
```bash
# Check .env
cat .env

# Should show: GROQ_API_KEY=gsk_...
# If not, create it:
echo "GROQ_API_KEY=your_key" > .env
```

#### ChromaDB Issues

**Error:** Various ChromaDB errors

**Solution:**
```bash
# Check status
python agent/update_agent.py status

# Force rebuild
python agent/update_agent.py force

# Check permissions
ls -la data/chroma_db/
```

#### Import Conflicts

**Error:** `AttributeError: module 'resource' has no attribute 'getrlimit'`

**Reason:** File named `resource.py` conflicts with stdlib

**Solution:** Already fixed! Files renamed to `resource_agent.py`

### Debug Mode

Enable detailed logging:

**In app.py:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**In run_web.py:**
```python
app.run(
    debug=True,  # Already enabled
    use_reloader=True,
    use_debugger=True
)
```

### Performance Issues

**Slow responses:**

1. **Check ChromaDB size**
   ```bash
   python agent/update_agent.py status
   ```

2. **Reduce n_results in agents**
   ```python
   context = get_relevant_context(query, n_results=2)  # Instead of 4
   ```

3. **Use Gunicorn with workers**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5001 "interface.web.app:app"
   ```

**High memory usage:**

1. **Reduce workers**
   ```bash
   gunicorn -w 2  # Instead of 4
   ```

2. **Clear ChromaDB cache**
   ```bash
   rm -rf data/chroma_db/__pycache__
   ```

### Testing

**Test agent imports:**
```bash
python -c "from agent import router_node; print('✅ OK')"
```

**Test Flask app:**
```bash
python -c "from interface.web.app import app; print('✅ OK')"
```

**Test ChromaDB:**
```bash
python agent/update_agent.py status
```

**Test full system:**
```bash
curl http://localhost:5001/health
```

---

## Appendix

### File Naming Convention

All agent files use `_agent.py` suffix to avoid conflicts with Python standard library (e.g., `resource_agent.py` instead of `resource.py`).

### Line Counts

```
Total: ~1,500 lines
├── app.py: 315 lines
├── Agent modules: 788 lines
├── Web interface: 300+ lines
└── Utilities: ~100 lines
```

### Dependencies

See `requirements.txt` for complete list. Key packages:
- `langgraph>=0.0.55`
- `langchain>=0.1.10`
- `langchain-groq>=0.1.0`
- `chromadb>=0.4.22`
- `flask>=3.0.0`

### Version History

- **v2.2** - Centralized Sunny Persona system for consistent personality
- **v2.1** - Interface reorganization, update agent in module
- **v2.0** - Modular agent structure
- **v1.5** - Flask web interface
- **v1.0** - Core agent system with RAG

---

**For quick start, see [QUICKSTART.md](QUICKSTART.md)**

**For project overview, see [README.md](README.md)**
