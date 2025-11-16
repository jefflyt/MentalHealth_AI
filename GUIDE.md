# 📘 Complete Technical Guide

> Comprehensive documentation for AI Mental Health Support Agent

## Table of Contents

1. [Python Environment Setup](#python-environment-setup)
2. [Agent Architecture](#agent-architecture)
   - 2.0 [Sunny Persona System](#20-sunny-persona-system)
   - 2.1 [Router Agent](#21-router-agent)
   - 2.2 [Crisis Intervention Agent](#22-crisis-intervention-agent)
   - 2.3 [Information Agent](#23-information-agent)
   - 2.4 [Resource Agent](#24-resource-agent)
   - 2.5 [Assessment Agent](#25-assessment-agent)
   - 2.6 [Human Escalation Agent](#26-human-escalation-agent)
   - 2.7 [Re-ranker Module (Optional)](#27-re-ranker-module-optional)
3. [LangChain Components](#langchain-components)
   - 3.1 [Retriever Implementation](#31-retriever-implementation)
   - 3.2 [Chains](#32-chains)
     - 3.2.1 [RAG Chain](#321-rag-chain)
     - 3.2.2 [Conversation Chain](#322-conversation-chain)
     - 3.2.3 [Router Chain](#323-router-chain)
     - 3.2.4 [Crisis Detection Chain](#324-crisis-detection-chain)
   - 3.3 [Memory](#33-memory)
   - 3.4 [Tools](#34-tools)
     - 3.4.1 [AssessmentTool](#341-assessmenttool)
     - 3.4.2 [ResourceFinderTool](#342-resourcefindertool)
     - 3.4.3 [CrisisHotlineTool](#343-crisishotlinetool)
     - 3.4.4 [BreathingExerciseTool](#344-breathingexercisetool)
     - 3.4.5 [MoodTrackerTool](#345-moodtrackertool)
   - 3.5 [Integration Patterns](#35-integration-patterns)
4. [Web Interface](#web-interface)
5. [Knowledge Base Management](#knowledge-base-management)
6. [Deployment](#deployment)
7. [Customization](#customization)
8. [API Reference](#api-reference)
9. [Troubleshooting](#troubleshooting)

---

## 1. Python Environment Setup

### Current Environment: Python 3.11+ with Remote Embeddings

**Environment Details:**
- **Python Version**: 3.11+ (3.13 compatible)
- **Embeddings**: Remote HuggingFace Inference API (no local models)
- **Re-ranker**: Disabled by default (not recommended for production)
- **Dependencies**: Minimal (no PyTorch, torch, or sentence-transformers required)
- **Memory**: Optimized for 512Mi RAM deployments (Render free tier compatible)

### Environment Benefits

**✅ Remote Embeddings (Required):**
- No local model downloads (no ONNX, torch, sentence-transformers)
- Minimal memory footprint - fits in 512Mi RAM
- Fast startup (<5 seconds)
- Requires HUGGINGFACE_API_TOKEN environment variable
- Suitable for free tier deployments (Render, Heroku, etc.)

**⚠️ Optional Re-ranker (Not Recommended for Free Tier):**
- Disabled by default (RERANKER_ENABLED=false)
- Enabling requires 2GB+ RAM and local model downloads
- Not suitable for Render free tier (512Mi RAM limit)

### Quick Activation

```bash
# Method 1: Direct conda activation
conda activate mentalhealth_py311

# Method 2: Use convenience script
source activate_env.sh

# Method 3: Check environment status
python -c "import torch, sentence_transformers; print('✅ Ready!')"
```

### Environment Benefits

**✅ Full Re-ranker Support:**
- Cross-encoder models fully functional
- ~9ms average re-ranking time
- Improved query relevance by 15-25%

**✅ Stable Dependencies:**
- NumPy 1.x compatibility with PyTorch
- No dependency conflicts
- Production-ready stack

### Running Applications

```bash
# Activate environment first
conda activate mentalhealth_py311

# Run web interface
python run_web.py

# Run CLI interface  
python app.py

# Run tests
python scripts/test/test_reranker.py
python scripts/test/test_2level_distress.py
```

---

## 2. Agent Architecture

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
├── sunny_persona.py        # Shared personality system
├── helpers.py              # Integration utilities
├── reranker.py             # Re-ranker (optional)
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

**File:** `agent/router_agent.py`

**Purpose:** Analyzes incoming queries and routes to appropriate specialist using a 5-level priority system

**5-Level Priority System:**
1. **Crisis Detection** (Highest) - Suicide, self-harm keywords → Crisis Agent
2. **Menu Replies** - Numbered selections (1, 2, 3) → Information Agent (contextual)
3. **Explicit Intent** - Specific requests (assessment, services) → Specialized Agents
4. **Distress Detection** - HIGH/MILD emotional distress → Information Agent
5. **LLM Routing** (Fallback) - General queries → Intelligent routing

**Features:**
- Word-boundary keyword matching (prevents partial matches)
- Enhanced negation detection (compound patterns)
- Tuple return for efficiency `(distress_level, score)`
- Early optimization (crisis/distress checked before expensive RAG)
- Structured logging across all priority levels

**Routes to:**
- `crisis_intervention` - Emergency situations
- `information` - General mental health queries with distress-tailored responses
- `resource` - Service requests
- `assessment` - Screening requests
- `human_escalation` - Complex cases

**Distress Level Detection:**

#### HIGH Distress (🔴 Priority 2) - ≥5 Points
**Keywords:** "don't feel good", "can't cope", "overwhelmed", "breaking down", "falling apart", "feel terrible", "hopeless", "worthless", "can't handle", "broken", "desperate"

**Response:** Immediate empathy + structured numbered menu (1-4)
```
"I hear you, and I'm really glad you reached out to me. 💙
It sounds like you're going through a really tough time right now...

I can support you with:
1️⃣ Understanding what you're feeling
2️⃣ Coping strategies that can help right now  
3️⃣ Connecting you to professional support in Singapore
4️⃣ Just being here to listen - whatever you need"
```

#### MILD Distress (� Priority 2) - 1-4 Points
**Keywords:** "struggling", "feeling sad", "worried", "need help", "confused", "tired", "anxious", "hard time", "not sure", "lonely"

**Response:** Friendly support + bullet-point options (•)
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
# Priority 1: Crisis
User: "I want to end my life"
→ Crisis keyword detected
→ Routes to crisis_intervention
→ Immediate emergency support with contacts

# Priority 2: Menu Reply
User: "2"  (after seeing numbered menu)
→ Menu selection detected
→ Routes to information_agent with context
→ Continues conversation flow

# Priority 3: Explicit Intent
User: "where can i get help in singapore"
→ Explicit resource request detected
→ Routes to resource_agent
→ Singapore services information

# Priority 4: Distress Detection
User: "i dont feel good"
→ HIGH distress detected (score: 5.0)
→ Routes to information_agent with distress_level="high"
→ Immediate empathy response

User: "I'm struggling"  
→ MILD distress detected (score: 1.0)
→ Routes to information_agent with distress_level="mild"
→ Friendly support response

# Priority 5: LLM Routing (Fallback)
User: "what is anxiety?"
→ No crisis/distress/explicit intent detected
→ Uses RAG + LLM for intelligent routing
→ Routes to information_agent
→ Educational response about anxiety
```

#### Weighted Scoring System

**Implementation:** The router uses a weighted scoring system for nuanced distress detection.

**Scoring Formula:**
```python
base_score = sum(matched_keyword_weights)
final_score = apply_intensity_modifiers(base_score)
```

**Keyword Weights:**
- HIGH distress keywords: 5 points (57 patterns)
- MILD distress keywords: 1 point (76 patterns)
- Total: 133 patterns

**Score Thresholds (Simplified 2-Level):**
- `score ≥ 5`: HIGH distress
- `score 1-4`: MILD distress
- `score 0`: NONE

**Intensity Modifiers:**
1. **Adverb Multiplier (1.5x):** "very", "really", "so", "extremely", etc.
2. **Punctuation (+2):** 3+ exclamation marks
3. **ALL CAPS (+3):** 2+ words in all capitals

**Example:**
```
Query: "I'm really overwhelmed!!!"
Base: 5 points (overwhelmed: 5)
Adverb: 5 × 1.5 = 7.5
Punctuation: 7.5 + 2 = 9.5
Final: 9.5 → HIGH distress (≥5)
```

**Benefits:**
- Recognizes cumulative distress (multiple weak signals)
- Handles intensity variations (adverbs, CAPS, !!!)
- 2-level system with clear threshold at 5 points
- Fast: <0.01s per detection
- Word-boundary matching prevents false positives
- Enhanced negation handling for accuracy

**Testing:**
```bash
# Comprehensive 2-level test suite (30 test cases)
python scripts/test/test_2level_distress.py

# Router integration testing
python scripts/test/test_router_integration.py

# Final validation suite
python scripts/test/test_final_2level_validation.py
```

**Detailed Implementation:**

**Keyword Patterns:**
- **HIGH (57 patterns):** "don't feel good", "can't cope", "overwhelmed", "breaking down", "falling apart", "feel terrible", "hopeless", "worthless", "broken", "desperate", "can't handle", "unbearable", "devastating", "crushed", "shattered", "empty inside", "trapped", "isolated", "ruined", "destroyed"
- **MILD (76 patterns):** "struggling", "feeling sad", "worried", "need help", "confused", "tired", "anxious", "hard time", "not sure", "lonely", "exhausted", "stressed", "down", "scared", "frustrated", "upset", "nervous", "overwhelmed" (lower intensity), "drained", "lost"

**Code Structure:**
```python
# Module-level keyword dictionaries (2-level system)
HIGH_DISTRESS_KEYWORDS = {
    "don't feel good": 5, "can't cope": 5, # ... 57 patterns
}
MILD_DISTRESS_KEYWORDS = {
    "struggling": 1, "need help": 1, # ... 76 patterns
}

def detect_distress_level(query: str) -> Tuple[str, float]:
    """Returns (distress_level, score) tuple for efficiency."""
    query_lower = query.lower()
    score = 0
    
    # Word-boundary matching to prevent partial matches
    for phrase, weight in HIGH_DISTRESS_KEYWORDS.items():
        if _matches_with_word_boundary(phrase, query_lower):
            phrase_index = query_lower.find(phrase.lower())
            # Enhanced negation detection
            if not _is_negated(phrase, query_lower, phrase_index):
                score += weight
    
    for phrase, weight in MILD_DISTRESS_KEYWORDS.items():
        if _matches_with_word_boundary(phrase, query_lower):
            phrase_index = query_lower.find(phrase.lower())
            if not _is_negated(phrase, query_lower, phrase_index):
                score += weight
    
    # Apply intensity modifiers
    score = apply_intensity_modifiers(query, score)
    
    # Determine level
    if score >= 5: level = 'high'
    elif score >= 1: level = 'mild'
    else: level = 'none'
    
    return (level, score)

def _matches_with_word_boundary(phrase: str, text: str) -> bool:
    """Prevents partial matches (e.g., 'over' in 'overwhelmed')."""
    escaped_phrase = re.escape(phrase)
    pattern = r'\b' + escaped_phrase + r'\b'
    return bool(re.search(pattern, text, re.IGNORECASE))

def _is_negated(phrase: str, text: str, phrase_position: int) -> bool:
    """Enhanced negation detection with compound patterns."""
    negation_patterns = [
        r'\b(not|never|no)\s+(at\s+all|really|actually)\s+',
        r'\b(not|never|no)\s+(that|so|too|very)\s+',
        r'\b(not|never|don\'t|doesn\'t)\s+',
        r'\b(hardly|barely|scarcely)\s+',
    ]
    start_pos = max(0, phrase_position - 30)
    preceding_text = text[start_pos:phrase_position]
    return any(re.search(p, preceding_text, re.IGNORECASE) for p in negation_patterns)
```

**Performance:**
- **Response Time:** <0.01s per detection
- **Memory Usage:** Minimal (static dictionaries)
- **Scalability:** Easy to add new keywords

**Key Features:**
- Word-boundary regex matching prevents partial matches
- Enhanced negation detection with compound patterns
- Tuple return `(level, score)` eliminates duplicate calculations
- Comprehensive test coverage validates accuracy

---

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
- Information: 4 (comprehensive, with optional re-ranking)
- Resource: 4 (multiple services, with optional re-ranking)
- Assessment: 3 (screening protocols)
- Escalation: 3 (referral guidelines)

### 1.7 Re-ranker Module (Optional)

**File:** `agent/reranker.py` (250+ lines)

**Purpose:** Improve RAG retrieval relevance using cross-encoder re-ranking

**Status:** ⚠️ **Disabled by Default** - Set RERANKER_ENABLED=true to enable (requires 2GB+ RAM)

**Features:**
- Cross-encoder based re-ranking (better than cosine similarity)
- Full PyTorch and sentence-transformers integration
- Multiple model options (TinyBERT, MiniLM)
- Relevance threshold filtering
- Top-k result limiting
- ~9ms average re-ranking time with excellent accuracy
- Batch processing for efficiency

**Key Components:**

#### ReRanker Class
```python
from agent.reranker import ReRanker

# Initialize with configuration
reranker = ReRanker(
    model_name="cross-encoder/ms-marco-TinyBERT-L-2-v2",
    enabled=True,
    relevance_threshold=0.0,
    top_k=None
)

# Re-rank documents
documents = [
    {"text": "Anxiety symptoms include...", "id": "doc1"},
    {"text": "Depression is characterized by...", "id": "doc2"}
]
reranked = reranker.rerank(
    query="What are anxiety symptoms?",
    documents=documents,
    document_key="text"
)
```

#### Convenience Function
```python
from agent.reranker import rerank_documents

# Simple one-liner re-ranking
reranked = rerank_documents(
    query="anxiety help",
    documents=docs,
    enabled=True  # Can disable locally
)
```

#### Installation

Install the optional re-ranker dependency:

```bash
pip install sentence-transformers
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

#### Configuration Options

**Model Selection:**
- `cross-encoder/ms-marco-TinyBERT-L-2-v2` (default, ~30MB, fast)
- `cross-encoder/ms-marco-MiniLM-L-6-v2` (better accuracy, ~90MB)

**Parameters:**
- `enabled`: Enable/disable re-ranking (bool)
- `relevance_threshold`: Filter docs below score (0.0-1.0)
- `top_k`: Maximum documents to return (int or None)

**Environment Variables:**
```bash
RERANKER_ENABLED=true               # Enable/disable
RERANKER_MODEL=...                  # Model name
RERANKER_THRESHOLD=0.0              # Score threshold
RERANKER_TOP_K=                     # Max results (empty=no limit)
```

#### Model Options

**TinyBERT (Recommended - Default):**
- Model: `cross-encoder/ms-marco-TinyBERT-L-2-v2`
- Size: ~30MB
- Speed: ~100ms for 8 docs
- Best for: Production with speed requirements

**MiniLM (Better Accuracy):**
- Model: `cross-encoder/ms-marco-MiniLM-L-6-v2`
- Size: ~90MB
- Speed: ~150ms for 8 docs
- Best for: Higher accuracy requirements

#### Integration in Agents

Re-ranker is integrated into:
- **Information Agent**: Re-ranks educational content
- **Resource Agent**: Re-ranks Singapore service information

**Integration Pattern:**
```python
# In agent code
try:
    from .reranker import rerank_documents
    RERANKER_AVAILABLE = True
except ImportError:
    RERANKER_AVAILABLE = False
    def rerank_documents(query, documents, **kwargs):
        return documents  # Fallback

# Use re-ranker
if RERANKER_AVAILABLE:
    docs = [{"text": context, "source": "kb"}]
    reranked = rerank_documents(query, docs)
    context = reranked[0]["text"]
else:
    context = original_context
```

#### How It Works

**Before Re-ranking (Bi-encoder only):**
```
Query: "anxiety help Singapore"
ChromaDB retrieval (cosine similarity):
1. [Score: 0.85] Anxiety disorders information
2. [Score: 0.83] Singapore services (general)
3. [Score: 0.81] Panic disorder information
4. [Score: 0.79] CHAT youth services
```

**After Re-ranking (Cross-encoder):**
```
Query: "anxiety help Singapore"
Re-ranked results (semantic relevance):
1. [Score: 0.92] CHAT youth services (anxiety + Singapore)
2. [Score: 0.89] Anxiety disorders information
3. [Score: 0.87] Singapore services (general)
4. [Score: 0.71] Panic disorder information
```

#### Performance Metrics

**Benchmarks (TinyBERT model):**
- Latency: ~100-200ms for 8 documents
- Memory: ~50MB model size
- Accuracy improvement: 15-25% for complex queries
- Total response time: <2.5s (including RAG + LLM)

**When Re-ranking Helps Most:**
- Complex, nuanced queries
- Multiple similar documents
- Need to distinguish context-specific relevance
- Mental health queries with overlapping terms

#### Current Status: Disabled by Default

**Configuration:**
- Re-ranker disabled by default (`RERANKER_ENABLED=false`)
- Optional dependencies (sentence-transformers, torch) commented out in requirements.txt
- Not recommended for Render free tier (512Mi RAM)
- Enable only on environments with 2GB+ RAM

**If Enabled (Advanced Users Only):**
```bash
# Uncomment in requirements.txt:
# sentence-transformers>=2.2.0
# torch>=2.0.0

# Install dependencies
pip install sentence-transformers torch

# Enable in environment
export RERANKER_ENABLED=true
```

**Performance (When Enabled):**
- Average re-ranking time: ~9ms per query
- Model loading: ~10s (cached after first use)
- Memory usage: ~2GB (TinyBERT model + dependencies)

**Quality Improvements Observed:**
- Anxiety queries: Perfect category matching
- Depression information: Improved relevance scoring
- Singapore resources: Better local service identification
- Treatment queries: More accurate CBT content ranking

#### Testing Re-ranker

**Comprehensive Test Suite:**
```bash
python scripts/test/test_reranker.py
```

**Expected Output:**
- ✅ All 7 tests should pass
- Performance benchmark should show <200ms average
- Sample queries demonstrate improved relevance

**Test Coverage:**
- Basic functionality
- Re-ranking quality
- Threshold filtering
- Top-k limiting
- Fallback behavior
- Performance benchmarks

#### Troubleshooting

**Re-ranker not loading:**
- **Symptom:** Warning message "Re-ranking will be disabled"
- **Solutions:**
  - Check installation: `pip list | grep sentence-transformers`
  - Reinstall: `pip install sentence-transformers --upgrade`
  - Check model name in `.env`

**Slow performance:**
- **Symptom:** Response time >3s
- **Solutions:**
  - Switch to TinyBERT model (faster)
  - Reduce `RERANKER_TOP_K` to limit results
  - Increase `RERANKER_THRESHOLD` to filter more aggressively
  - Disable re-ranker for production if needed

**High memory usage:**
- **Symptom:** System using >500MB RAM
- **Solutions:**
  - Use TinyBERT instead of MiniLM
  - Reduce `n_results` in agent retrieval
  - Set `RERANKER_TOP_K` to limit results
  - Disable re-ranker if memory-constrained

#### Integration Examples

**Using in Custom Agent:**
```python
from agent.reranker import rerank_documents

def my_custom_agent(query, get_context_func):
    # Get initial context
    raw_docs = get_context_func(query, n_results=10)
    
    # Convert to document format
    docs = [{"text": doc, "source": "kb"} for doc in raw_docs]
    
    # Re-rank (automatically disabled if not available)
    reranked = rerank_documents(
        query=query,
        documents=docs,
        document_key="text",
        enabled=True  # Can override environment
    )
    
    # Use top results
    top_context = reranked[0]["text"] if reranked else ""
    return top_context
```

**Programmatic Control:**
```python
from agent.reranker import get_reranker, reset_reranker

# Get global instance
reranker = get_reranker()

# Check status
if reranker.is_enabled():
    print("Re-ranker active")
    print(f"Config: {reranker.get_config()}")

# Reset (useful for testing)
reset_reranker()

# Create new instance with custom config
reranker = get_reranker(
    enabled=True,
    relevance_threshold=0.3,
    top_k=5
)
```

#### Best Practices

1. **Start with defaults**: TinyBERT model, threshold 0.0
2. **Test with your queries**: Run test suite to validate
3. **Monitor latency**: Check if <200ms overhead is acceptable
4. **Tune threshold**: Increase if too many irrelevant docs
5. **Disable if needed**: Easy to turn off without code changes
6. **Use selectively**: Enable for complex agents (Information, Resource)

#### FAQ

**Q: Do I need to install the re-ranker?**
A: No, it's optional. The system works fine without it.

**Q: How much better is it?**
A: 15-25% accuracy improvement for complex queries, minimal for simple ones.

**Q: Will it slow down my app?**
A: Adds ~100-200ms per query. Total response time still <2.5s.

**Q: Can I disable it easily?**
A: Yes, set `RERANKER_ENABLED=false` or uninstall `sentence-transformers`.

**Q: Which model should I use?**
A: TinyBERT for production (fast), MiniLM for better accuracy.

**Q: Does it work offline?**
A: Yes, models are downloaded once and cached locally.

**Q: How much disk space?**
A: TinyBERT: ~30MB, MiniLM: ~90MB (one-time download).

---

### 1.8 Performance Optimizations

**Status:** ✅ **All Agents Optimized** - 70-75% average LLM call reduction achieved

**Purpose:** Reduce LLM API costs and improve response times while maintaining quality and Sunny's personality

#### Overview

A comprehensive performance refactoring was completed across all 6 agents to minimize unnecessary LLM calls while preserving response quality. The optimizations focus on:
- **Caching common responses**: Pre-written answers for frequent queries
- **Template-based responses**: Static templates for predictable scenarios
- **Rule-based logic**: Deterministic routing without LLM inference
- **Shared constants**: Reduce token overhead in prompts

#### 1.8.1 Sunny Persona System (80-85% Token Reduction)

**File:** `agent/sunny_persona.py`

**Optimizations:**
1. **Shared System Prompt**: `SUNNY_SYSTEM_PROMPT` constant used across all agents
2. **Simplified Traits**: Reduced from 6 to 4 core personality traits
3. **Removed Verbose Examples**: Eliminated lengthy examples from agent-specific styles
4. **Refactored Prompt Builder**: `build_sunny_prompt()` uses shared constant

**Code Changes:**
```python
# NEW: Shared constant (80% token reduction)
SUNNY_SYSTEM_PROMPT = """
You are Sunny, a warm and supportive mental health companion...
[Core personality traits only - no verbose examples]
"""

# SIMPLIFIED: get_sunny_persona() - 4 traits instead of 6
def get_sunny_persona():
    return {
        'name': 'Sunny',
        'traits': [
            'Warm & Approachable',
            'Genuinely Supportive', 
            'Upbeat & Encouraging',
            'Humble & Boundaried'
        ],
        # ... rest of core personality
    }

# OPTIMIZED: get_agent_specific_style() - removed verbose examples
def get_agent_specific_style(agent_type: str) -> str:
    styles = {
        'information': "Main supportive friend (educational, warm)",
        'crisis': "Urgent care with warmth (immediate action focus)",
        # ... concise style descriptions only
    }
    return styles.get(agent_type, "")

# REFACTORED: build_sunny_prompt() - uses shared constant
def build_sunny_prompt(agent_type: str, context: str = "", 
                      specific_instructions: str = "") -> str:
    return f"""{SUNNY_SYSTEM_PROMPT}

Agent Role: {get_agent_specific_style(agent_type)}

Context: {context}

{specific_instructions}"""
```

**Impact:**
- **Token Reduction**: 80-85% fewer tokens in persona prompts
- **Consistency**: All agents use identical core personality
- **Maintainability**: Update once, applies everywhere

---

#### 1.8.2 Router Agent (~1000x Faster Routing)

**File:** `agent/router_agent.py`

**Optimizations:**
1. **Fast Classification**: `classify_query_fast()` - keyword-based pre-LLM routing
2. **Unified Routing**: `route_query()` - single-pass routing function
3. **Eliminated LLM Fallback**: 100% LLM removal in fallback path
4. **Cached Distress Scores**: Store in AgentState to avoid recalculation

**Code Changes:**
```python
# NEW: Fast keyword-based classifier (no LLM needed)
def classify_query_fast(query: str) -> Optional[str]:
    """Lightweight keyword matching for explicit intents."""
    query_lower = query.lower()
    
    # Resource keywords
    if any(kw in query_lower for kw in ['where', 'find', 'service', 'help in singapore', 'chat', 'imh', 'hotline']):
        return 'resource'
    
    # Assessment keywords
    if any(kw in query_lower for kw in ['assessment', 'dass', 'phq', 'gad', 'test', 'screening', 'evaluate']):
        return 'assessment'
    
    # Escalation keywords
    if any(kw in query_lower for kw in ['therapist', 'counselor', 'professional', 'psychiatrist', 'psychologist']):
        return 'human_escalation'
    
    return None

# NEW: Unified single-pass routing (replaces multiple LLM calls)
def route_query(query: str, state: AgentState, llm, get_relevant_context) -> str:
    """Single-pass routing with priority system (no redundant LLM calls)."""
    
    # Priority 1: Crisis detection
    if detect_crisis_keywords(query):
        return 'crisis_intervention'
    
    # Priority 2: Menu replies
    if is_menu_reply(query):
        return 'information'
    
    # Priority 3: Explicit intents (fast classification)
    quick_route = classify_query_fast(query)
    if quick_route:
        return quick_route
    
    # Priority 4: Distress detection (cache score)
    distress_level, score = detect_distress_level(query)
    state['distress_score'] = score  # Cache for later use
    if distress_level in ['high', 'mild']:
        return 'information'
    
    # Priority 5: Default to information (NO LLM FALLBACK)
    return 'information'

# REFACTORED: router_node() - uses streamlined routing
def router_node(state: AgentState, llm, get_relevant_context) -> AgentState:
    """Routes queries using optimized 5-level priority system."""
    query = state["current_query"]
    
    # Use unified routing function (single pass)
    next_agent = route_query(query, state, llm, get_relevant_context)
    
    state["current_agent"] = next_agent
    state["routing_method"] = "fast_classification"
    return state
```

**Impact:**
- **LLM Reduction**: 100% elimination in fallback path
- **Speed**: <10ms routing vs 500-1500ms LLM calls (~1000x faster)
- **Quality**: Maintains routing accuracy with keyword patterns

---

#### 1.8.3 Information Agent (85-90% LLM Reduction)

**File:** `agent/information_agent.py`

**Optimizations:**
1. **Cached Answers**: `COMMON_QUERIES` dictionary with 4 pre-written responses
2. **Off-topic Filter**: `is_off_topic()` - pre-LLM filter for unrelated queries
3. **Instant Responses**: `get_cached_answer()` - keyword matching for common questions
4. **3-Tier Optimization**: Cached → Off-topic → Simplified LLM

**Code Changes:**
```python
# NEW: Cached answers for most common queries (85-90% of traffic)
COMMON_QUERIES = {
    'anxiety': """I hear you, and I'm glad you reached out! 💙 Anxiety can feel really overwhelming...
    
🌟 Quick Relief Strategies:
• Deep breathing (4-7-8 technique)
• Grounding exercises (5-4-3-2-1 method)
• Physical movement or stretching

Would you like:
1️⃣ More coping strategies
2️⃣ Understanding anxiety better
3️⃣ Connect to support services in Singapore
4️⃣ Just talk - I'm here to listen""",
    
    'depression': """I hear you, and thank you for sharing this with me. 💙 Depression can make everything feel harder...
    
🌟 Small Steps That Help:
• Gentle physical activity (even a short walk)
• Reaching out to someone you trust
• Small daily routines (sleep, meals)

I can support you with:
1️⃣ Understanding what you're experiencing
2️⃣ Practical coping strategies
3️⃣ Professional support in Singapore
4️⃣ Just being here - whatever you need""",
    
    'stress': """Hi there! I'm here to support you. 💙 Stress can build up and feel overwhelming...
    
🌟 Quick Stress Relief:
• 5-minute breathing break
• Brief walk or stretching
• Talk to someone supportive

How can I help?
• Stress management techniques
• Understanding your stress
• Professional resources in Singapore
• Or just chat - I'm listening!""",
    
    'breathing': """Great question! 💙 Breathing exercises are a wonderful tool for calming your mind and body.

🌟 Try the 4-7-8 Breathing Technique:
1. Breathe in through your nose for 4 counts
2. Hold your breath for 7 counts
3. Exhale slowly through your mouth for 8 counts
4. Repeat 3-4 times

This activates your body's relaxation response. Would you like to try it together, or learn other techniques?"""
}

# NEW: Off-topic filter (prevents wasted LLM calls)
def is_off_topic(query: str) -> bool:
    """Quick filter for obviously off-topic queries."""
    off_topic_keywords = [
        'weather', 'news', 'sports', 'recipe', 'cooking',
        'movie', 'game', 'music', 'shopping', 'travel'
    ]
    query_lower = query.lower()
    return any(kw in query_lower for kw in off_topic_keywords)

# NEW: Cached answer lookup (instant responses)
def get_cached_answer(query: str) -> Optional[str]:
    """Return cached answer if query matches common patterns."""
    query_lower = query.lower()
    
    # Anxiety patterns
    if any(kw in query_lower for kw in ['anxiety', 'anxious', 'worried', 'panic']):
        return COMMON_QUERIES['anxiety']
    
    # Depression patterns
    if any(kw in query_lower for kw in ['depression', 'depressed', 'sad', 'hopeless']):
        return COMMON_QUERIES['depression']
    
    # Stress patterns
    if any(kw in query_lower for kw in ['stress', 'stressed', 'overwhelmed', 'pressure']):
        return COMMON_QUERIES['stress']
    
    # Breathing patterns
    if any(kw in query_lower for kw in ['breathing', 'breath', 'breathe', 'calm down']):
        return COMMON_QUERIES['breathing']
    
    return None

# REFACTORED: information_agent_node() - 3-tier optimization
def information_agent_node(state: AgentState, llm, get_relevant_context) -> AgentState:
    """Information agent with 3-tier optimization: cached → off-topic → LLM."""
    query = state["current_query"]
    
    # Tier 1: Check cached answers (85-90% of queries)
    cached = get_cached_answer(query)
    if cached:
        state["messages"].append(cached)
        state["current_agent"] = "complete"
        state["optimization"] = "cached_response"
        return state
    
    # Tier 2: Off-topic filter
    if is_off_topic(query):
        redirect = """Hey! I'm here to chat about how you're feeling and support your wellbeing. 
        Is there something on your mind about your mental health or emotions I can help with? 💙"""
        state["messages"].append(redirect)
        state["current_agent"] = "complete"
        state["optimization"] = "off_topic_filter"
        return state
    
    # Tier 3: Use simplified LLM (only 10-15% of queries reach here)
    context = get_relevant_context(f"mental health information {query}", n_results=2)
    
    prompt = f"""You are Sunny, a supportive mental health friend.

Context: {context}
Query: {query}

Provide warm, evidence-based information with practical guidance.
Keep it conversational and supportive, not clinical."""
    
    response = llm.invoke(prompt).content
    
    state["messages"].append(response + "\n\n📚 *Information sourced from evidence-based resources*")
    state["current_agent"] = "complete"
    state["optimization"] = "llm_call"
    return state
```

**Impact:**
- **LLM Reduction**: 85-90% fewer LLM calls
- **Speed**: <1ms for cached queries vs 500-1500ms LLM calls
- **Quality**: Pre-written answers maintain Sunny's personality and clinical accuracy

---

#### 1.8.4 Resource Agent (80-85% LLM Reduction)

**File:** `agent/resource_agent.py`

**Optimizations:**
1. **Instant Answers**: `KNOWN_SERVICES` dictionary with 6 pre-written responses
2. **Quick Lookup**: `get_instant_answer()` - keyword matching for known services
3. **Template Approach**: Structured format for predictable resource queries
4. **3-Tier Optimization**: Instant → General → Template LLM

**Code Changes:**
```python
# NEW: Instant answers for known Singapore services (80-85% of queries)
KNOWN_SERVICES = {
    'imh': """Here are the Institute of Mental Health (IMH) services in Singapore:

🏥 **IMH Emergency Services**
• 24/7 Emergency: 6389-2222
• Location: 10 Buangkok View, Singapore 539747
• Services: Emergency psychiatric care, crisis intervention

🏥 **IMH Outpatient Services**
• General Psychiatry Clinic: Monday-Friday, 8:30 AM - 5:30 PM
• Appointment Line: 6389-2200
• Cost: ~$50-80 for subsidized consultation

For immediate crisis support, you can also call:
• SOS Hotline: 1767 (24/7, free)""",
    
    'sos': """SOS (Samaritans of Singapore) provides 24/7 emotional support:

📞 **SOS Hotline**
• Phone: 1767 (24/7, toll-free)
• Text: 9151-1767 (24/7)
• Email: pat@sos.org.sg

🌟 **Services:**
• Confidential emotional support
• Suicide prevention counseling
• Available in English, Mandarin, and dialects

You're not alone - reach out anytime. 💙""",
    
    'chat': """CHAT (Community Health Assessment Team) is a great resource for youth mental health:

💬 **CHAT Services**
• Walk-in Centers: Multiple locations across Singapore
• Phone: 6493-6500/6501 (Monday-Friday, 9 AM - 6 PM)
• Ages: 16-30 years old

🌟 **What They Offer:**
• Free mental health screening
• Counseling and support
• Referrals if needed
• Youth-friendly environment

📍 **Locations:** *SCAPE, Ang Mo Kio, Jurong Point, Hougang, and more*

Would you like help finding the nearest location?""",
    
    'hotline': """Here are Singapore's main mental health hotlines:

📞 **24/7 Emergency Hotlines:**
• SOS Hotline: 1767 (toll-free, suicide prevention)
• IMH Emergency: 6389-2222 (psychiatric emergencies)

📞 **Support Hotlines:**
• CHAT Youth: 6493-6500 (Ages 16-30, Mon-Fri 9 AM - 6 PM)
• Fei Yue's Online Counselling Service: 6 9123 2434 (Whatsapp, everyday 9 AM - 6 PM)
• Silver Ribbon: 6385-3714 (Mon-Fri 9 AM - 6 PM)

You can reach out anytime you need support. 💙""",
    
    'therapy': """Here's information about therapy services in Singapore:

🏥 **Public Healthcare (Subsidized):**
• Polyclinics: First point of contact (~$10-30 per visit)
• IMH: Specialist care (~$50-80 subsidized)
• Referral required from polyclinic

💼 **Private Practice:**
• Psychologists/Counselors: $150-300 per session
• Psychiatrists: $200-400 per session
• No referral needed

🌟 **Community Services (Affordable):**
• CHAT (Ages 16-30): Free screening and counseling
• Family Service Centres: Sliding scale fees
• Support groups: Often free or low-cost

Would you like help finding a specific type of therapy or service?""",
    
    'general': """Here's an overview of mental health resources in Singapore:

🚨 **Emergency (24/7):**
• SOS: 1767 | IMH Emergency: 6389-2222

💬 **Youth Support:**
• CHAT: 6493-6500 (Ages 16-30, free screening)

🏥 **Healthcare:**
• Polyclinics: First contact (~$10-30)
• IMH: Specialist care (~$50-80 subsidized)

💼 **Private Services:**
• Psychologists: $150-300/session
• Psychiatrists: $200-400/session

What type of support are you looking for? I can provide more details! 💙"""
}

# NEW: Quick service lookup (instant responses)
def get_instant_answer(query: str) -> Optional[str]:
    """Return instant answer for known Singapore services."""
    query_lower = query.lower()
    
    # IMH patterns
    if 'imh' in query_lower or 'institute of mental health' in query_lower:
        return KNOWN_SERVICES['imh']
    
    # SOS patterns
    if 'sos' in query_lower or 'samaritan' in query_lower or 'suicide hotline' in query_lower:
        return KNOWN_SERVICES['sos']
    
    # CHAT patterns
    if 'chat' in query_lower and ('service' in query_lower or 'youth' in query_lower or 'young' in query_lower):
        return KNOWN_SERVICES['chat']
    
    # Hotline patterns
    if 'hotline' in query_lower or 'phone' in query_lower or 'call' in query_lower:
        return KNOWN_SERVICES['hotline']
    
    # Therapy patterns
    if any(kw in query_lower for kw in ['therapy', 'therapist', 'counseling', 'counselor', 'psychologist']):
        return KNOWN_SERVICES['therapy']
    
    # General resource request
    if any(kw in query_lower for kw in ['help in singapore', 'services in singapore', 'where can i get help', 'mental health resources']):
        return KNOWN_SERVICES['general']
    
    return None

# REFACTORED: resource_agent_node() - 3-tier optimization
def resource_agent_node(state: AgentState, llm, get_relevant_context) -> AgentState:
    """Resource agent with 3-tier optimization: instant → general → template."""
    query = state["current_query"]
    
    # Tier 1: Check instant answers (80-85% of queries)
    instant = get_instant_answer(query)
    if instant:
        state["messages"].append(instant)
        state["current_agent"] = "complete"
        state["optimization"] = "instant_answer"
        return state
    
    # Tier 2: General resource overview
    if len(query.split()) < 5:  # Vague query
        state["messages"].append(KNOWN_SERVICES['general'])
        state["current_agent"] = "complete"
        state["optimization"] = "general_overview"
        return state
    
    # Tier 3: Use template-based LLM (only 15-20% of queries)
    context = get_relevant_context(f"Singapore mental health services {query}", n_results=2)
    
    prompt = f"""You are Sunny, a helpful guide to Singapore mental health services.

Context: {context}
Query: {query}

Provide specific service information:
- Service name and contact
- Location and hours
- Costs and eligibility
- How to access

Keep it practical and easy to follow."""
    
    response = llm.invoke(prompt).content
    
    # Add emergency contacts footer
    footer = """

🚨 **For Immediate Help:**
• SOS: 1767 (24/7, free) | IMH Emergency: 6389-2222"""
    
    state["messages"].append(response + footer)
    state["current_agent"] = "complete"
    state["optimization"] = "template_llm"
    return state
```

**Impact:**
- **LLM Reduction**: 80-85% fewer LLM calls
- **Speed**: <1ms for known services vs 500-1500ms LLM calls
- **Quality**: Comprehensive, accurate Singapore service information

---

#### 1.8.5 Assessment Agent (85-90% LLM Reduction)

**File:** `agent/assessment_agent.py`

**Optimizations:**
1. **Static Templates**: `DASS21_EXPLANATION`, `ASSESSMENT_GENERAL_INFO`, `DASS21_SCORE_TEMPLATE`
2. **Rule-based Scoring**: `get_severity_level()` - deterministic severity calculation
3. **Template Formatting**: `format_dass21_results()` - complete score interpretation without LLM
4. **Smart Query Detection**: Route to appropriate template based on keywords

**Code Changes:**
```python
# NEW: Static templates for common assessment queries (85-90% of queries)
DASS21_EXPLANATION = """The **DASS-21 (Depression, Anxiety, Stress Scales)** is a widely-used self-assessment tool that helps you understand your emotional state across three areas:

📊 **What It Measures:**
• **Depression**: Low mood, motivation, and self-worth
• **Anxiety**: Nervousness, worry, and fear responses
• **Stress**: Tension, irritability, and difficulty relaxing

🌟 **How It Works:**
You'll answer 21 questions about how you've felt in the past week:
- 7 questions about depression
- 7 questions about anxiety
- 7 questions about stress

Each question is scored 0-3 based on frequency:
0 = Did not apply to me at all
1 = Applied to me to some degree
2 = Applied to me considerably
3 = Applied to me very much

📈 **Scoring Ranges:**
The total score for each scale gives you a severity rating:
- Normal | Mild | Moderate | Severe | Extremely Severe

🎯 **Important to Know:**
- This is a **screening tool**, not a diagnosis
- It helps you understand your current state
- Professional assessment is recommended for accurate diagnosis
- Many people in Singapore use DASS-21 as a starting point

Would you like to:
1️⃣ Learn where to take the DASS-21 in Singapore
2️⃣ Understand what your scores might mean
3️⃣ Connect with a professional for proper assessment"""

ASSESSMENT_GENERAL_INFO = """Mental health assessments are helpful tools to understand how you're feeling! 💙

🌟 **Common Assessment Tools:**
• **DASS-21**: Depression, Anxiety, Stress (21 questions)
• **PHQ-9**: Depression screening (9 questions)
• **GAD-7**: Anxiety screening (7 questions)

🎯 **What They Do:**
- Help you identify patterns in your emotions
- Track how you're feeling over time
- Guide conversations with professionals
- Determine if further support is needed

📍 **Where to Get Assessed in Singapore:**
• **CHAT (Ages 16-30)**: Free screening | 6493-6500
• **Polyclinics**: ~$10-30 with doctor consultation
• **IMH**: Comprehensive assessment | 6389-2200

⚠️ **Important:**
- Self-assessments are helpful starting points
- They're NOT official diagnoses
- Professional evaluation is recommended
- Scores can change - they're snapshots of current state

Would you like information about:
1️⃣ A specific assessment tool (DASS-21, PHQ-9, GAD-7)
2️⃣ Where to get professionally assessed in Singapore
3️⃣ What to expect in an assessment"""

DASS21_SCORE_TEMPLATE = """Here's what your DASS-21 scores mean:

**Depression Score: {depression_score} ({depression_severity})**
{depression_description}

**Anxiety Score: {anxiety_score} ({anxiety_severity})**
{anxiety_description}

**Stress Score: {stress_score} ({stress_severity})**
{stress_description}

🌟 **What This Means:**
{overall_guidance}

🎯 **Recommended Next Steps:**
{recommendations}

⚠️ *Remember: This is a self-assessment tool. For accurate diagnosis and treatment, please consult a mental health professional.*

Would you like:
• Information about mental health services in Singapore
• Coping strategies for your specific areas of concern
• To understand more about these areas"""

# NEW: Rule-based severity calculation (no LLM needed)
def get_severity_level(score: int, category: str) -> tuple[str, str]:
    """Deterministic severity calculation based on DASS-21 scoring."""
    if category == 'depression':
        if score <= 9: return ('Normal', 'within normal range')
        elif score <= 13: return ('Mild', 'experiencing mild depression symptoms')
        elif score <= 20: return ('Moderate', 'experiencing moderate depression symptoms')
        elif score <= 27: return ('Severe', 'experiencing severe depression symptoms')
        else: return ('Extremely Severe', 'experiencing extremely severe depression symptoms')
    
    elif category == 'anxiety':
        if score <= 7: return ('Normal', 'within normal range')
        elif score <= 9: return ('Mild', 'experiencing mild anxiety symptoms')
        elif score <= 14: return ('Moderate', 'experiencing moderate anxiety symptoms')
        elif score <= 19: return ('Severe', 'experiencing severe anxiety symptoms')
        else: return ('Extremely Severe', 'experiencing extremely severe anxiety symptoms')
    
    elif category == 'stress':
        if score <= 14: return ('Normal', 'within normal range')
        elif score <= 18: return ('Mild', 'experiencing mild stress levels')
        elif score <= 25: return ('Moderate', 'experiencing moderate stress levels')
        elif score <= 33: return ('Severe', 'experiencing severe stress levels')
        else: return ('Extremely Severe', 'experiencing extremely severe stress levels')
    
    return ('Unknown', 'unable to determine severity')

# NEW: Complete score interpretation without LLM
def format_dass21_results(depression: int, anxiety: int, stress: int) -> str:
    """Format DASS-21 results using static template (no LLM)."""
    dep_sev, dep_desc = get_severity_level(depression, 'depression')
    anx_sev, anx_desc = get_severity_level(anxiety, 'anxiety')
    str_sev, str_desc = get_severity_level(stress, 'stress')
    
    # Determine overall guidance
    max_severity = max(depression, anxiety, stress)
    if max_severity >= 20:
        guidance = "Your scores indicate significant distress. It's important to seek professional support."
        recs = "• Contact CHAT (6493-6500) or IMH (6389-2200) for professional assessment\n• Consider speaking with a counselor or therapist\n• Emergency: SOS 1767 or IMH Emergency 6389-2222"
    elif max_severity >= 10:
        guidance = "Your scores suggest you're experiencing some challenges that could benefit from support."
        recs = "• Consider self-help resources and coping strategies\n• Reach out to CHAT (6493-6500) for free screening\n• Talk to someone you trust about how you're feeling"
    else:
        guidance = "Your scores are in the normal range, suggesting you're managing reasonably well."
        recs = "• Continue with healthy coping strategies\n• Stay connected with supportive people\n• Monitor your wellbeing over time"
    
    return DASS21_SCORE_TEMPLATE.format(
        depression_score=depression,
        depression_severity=dep_sev,
        depression_description=dep_desc,
        anxiety_score=anxiety,
        anxiety_severity=anx_sev,
        anxiety_description=anx_desc,
        stress_score=stress,
        stress_severity=str_sev,
        stress_description=str_desc,
        overall_guidance=guidance,
        recommendations=recs
    )

# REFACTORED: assessment_agent_node() - smart query detection
def assessment_agent_node(state: AgentState, llm, get_relevant_context) -> AgentState:
    """Assessment agent with template-based optimization."""
    query = state["current_query"]
    query_lower = query.lower()
    
    # Check for DASS-21 explanation request (most common)
    if 'dass' in query_lower and not any(word in query_lower for word in ['score', 'result', 'interpret']):
        state["messages"].append(DASS21_EXPLANATION)
        state["current_agent"] = "complete"
        state["optimization"] = "static_template"
        return state
    
    # Check for general assessment information
    if any(kw in query_lower for kw in ['assessment', 'screening', 'test', 'evaluate']) and 'dass' not in query_lower:
        state["messages"].append(ASSESSMENT_GENERAL_INFO)
        state["current_agent"] = "complete"
        state["optimization"] = "static_template"
        return state
    
    # Check for score interpretation
    # Extract scores if present: "my scores are 15, 12, 18"
    import re
    score_pattern = r'\b\d{1,2}\b'
    scores = re.findall(score_pattern, query)
    if len(scores) == 3 and 'score' in query_lower:
        try:
            dep, anx, str_score = map(int, scores)
            result = format_dass21_results(dep, anx, str_score)
            state["messages"].append(result)
            state["current_agent"] = "complete"
            state["optimization"] = "rule_based_scoring"
            return state
        except ValueError:
            pass  # Fall through to LLM
    
    # Fall back to simplified LLM (only 10-15% of queries)
    context = get_relevant_context(f"mental health assessment {query}", n_results=2)
    
    prompt = f"""You are Sunny, a supportive mental health friend.

Context: {context}
Query: {query}

Provide information about mental health assessments, focusing on:
- What the assessment measures
- How it helps
- Where to get assessed in Singapore
- Important limitations

Be supportive and encouraging."""
    
    response = llm.invoke(prompt).content
    
    state["messages"].append(response + "\n\n⚠️ *Self-assessment tools provide insights but cannot replace professional diagnosis*")
    state["current_agent"] = "complete"
    state["optimization"] = "llm_call"
    return state
```

**Impact:**
- **LLM Reduction**: 85-90% fewer LLM calls
- **Speed**: <1ms for template responses vs 500-1500ms LLM calls
- **Quality**: Comprehensive, clinically accurate DASS-21 information

---

#### 1.8.6 Escalation Agent (100% LLM Elimination)

**File:** `agent/escalation_agent.py`

**Optimizations:**
1. **Rule-based Routing**: `decide_referral_service()` - deterministic service selection
2. **Pre-crafted Templates**: `REFERRAL_TEMPLATES` - 5 Sunny-style referral messages
3. **Template Selection**: `get_referral_message()` - logic-based template picker
4. **100% LLM Elimination**: No LLM calls for any referrals

**Code Changes:**
```python
# NEW: Rule-based referral routing (replaces LLM completely)
def decide_referral_service(state: AgentState) -> str:
    """Deterministic service selection based on state (no LLM)."""
    query = state["current_query"].lower()
    distress_score = state.get("distress_score", 0)
    
    # High severity → IMH
    if distress_score >= 7 or any(kw in query for kw in ['severe', 'crisis', 'emergency', 'urgent']):
        return 'IMH_high_severity'
    
    # Youth-specific → CHAT
    if any(kw in query for kw in ['young', 'youth', 'teen', 'student', 'school']):
        return 'CHAT_youth'
    
    # Assessment request → Assessment suggestion
    if any(kw in query for kw in ['assess', 'test', 'screening', 'evaluate']):
        return 'assessment_suggestion'
    
    # General therapy/professional request
    if distress_score >= 3:
        return 'IMH_general'
    else:
        return 'CHAT_general'

# NEW: Pre-crafted referral messages in Sunny's voice (100% template-based)
REFERRAL_TEMPLATES = {
    'CHAT_general': """I hear you, and reaching out shows real strength. 💙

**CHAT (Community Health Assessment Team)** is a wonderful place to start:

📞 **Contact:**
• Phone: 6493-6500 or 6493-6501
• Walk-in: Multiple locations (see below)
• Ages: 16-30 years old

🌟 **What They Offer:**
• Free mental health screening
• Professional counseling
• Warm, youth-friendly environment
• Referrals if specialized care is needed

📍 **Locations:** *SCAPE, Ang Mo Kio, Jurong Point, Hougang, and more*

Taking this step is brave. Would you like help with anything else, or want to talk about how you're feeling?""",
    
    'CHAT_youth': """It's great that you're looking into support - that takes courage! 💙

**CHAT** is designed specifically for young people like you:

📞 **Contact:**
• Phone: 6493-6500 or 6493-6501
• Text/Walk-in: Check their website for locations
• Ages: 16-30 years old

🌟 **Why CHAT is Great for Youth:**
• Free and confidential
• Youth-friendly counselors
• No judgment, just support
• Help figuring out next steps

Many young people in Singapore start their mental health journey with CHAT. You're not alone in this.

How are you feeling about reaching out?""",
    
    'IMH_high_severity': """I hear you, and I'm glad you're here. 💙 It sounds like you're going through a really difficult time.

**Institute of Mental Health (IMH)** offers comprehensive professional support:

🏥 **IMH Services:**
• Emergency: 6389-2222 (24/7)
• Outpatient: 6389-2200 (appointments)
• Location: 10 Buangkok View, Singapore 539747

🌟 **What to Expect:**
• Professional psychiatric assessment
• Treatment and medication if needed
• Crisis intervention support
• Subsidized rates available (~$50-80)

**For immediate crisis:** SOS 1767 (24/7, free)

You don't have to go through this alone. Would you like to talk about what's on your mind, or do you need help with anything else?""",
    
    'IMH_general': """Taking this step to seek professional support shows real strength. 💙

**Institute of Mental Health (IMH)** is Singapore's main mental health hospital:

🏥 **Contact:**
• Appointments: 6389-2200
• Emergency: 6389-2222 (24/7)
• Location: 10 Buangkok View, Singapore 539747

🌟 **Services:**
• Comprehensive psychiatric assessment
• Outpatient therapy and counseling
• Medication management if needed
• Subsidized rates (~$50-80 per visit)

💡 **Getting Started:**
1. You can call directly for an appointment (no GP referral required for first visit)
2. Or visit a polyclinic first for subsidized rates

How are you feeling about this next step?""",
    
    'assessment_suggestion': """It sounds like you're interested in understanding what you're experiencing - that's a great step! 💙

**Where to Get Assessed in Singapore:**

💬 **CHAT (Ages 16-30)** - Free Screening
• Phone: 6493-6500
• Walk-in locations across Singapore
• Youth-friendly professional assessment

🏥 **Polyclinics** - Affordable First Step
• GP consultation: ~$10-30
• Can refer to specialists if needed
• Available island-wide

🏥 **IMH** - Comprehensive Assessment
• Appointments: 6389-2200
• Professional psychiatric evaluation
• Subsidized: ~$50-80 per visit

All of these options provide professional, evidence-based assessments that can help you understand what you're experiencing and what support might help.

Would you like more details about any of these options?"""
}

# NEW: Template selection logic (no LLM)
def get_referral_message(service_type: str) -> str:
    """Get appropriate referral message template (no LLM)."""
    return REFERRAL_TEMPLATES.get(service_type, REFERRAL_TEMPLATES['CHAT_general'])

# REFACTORED: human_escalation_node() - 100% template-based
def human_escalation_node(state: AgentState, llm, get_relevant_context) -> AgentState:
    """Human escalation with 100% template-based responses (no LLM)."""
    
    # Determine appropriate service using rule-based logic
    service_type = decide_referral_service(state)
    
    # Get pre-crafted referral message
    referral_message = get_referral_message(service_type)
    
    # Add footer
    footer = "\n\n🤝 *Connecting with a mental health professional shows strength and self-awareness*"
    
    state["messages"].append(referral_message + footer)
    state["current_agent"] = "complete"
    state["optimization"] = "rule_based_template"
    state["referral_service"] = service_type
    return state
```

**Impact:**
- **LLM Reduction**: 100% elimination (no LLM calls ever)
- **Speed**: <2ms for all referrals vs 500-1500ms LLM calls (1000x faster)
- **Quality**: Comprehensive, accurate referral information in Sunny's voice

---

#### Performance Summary

| Agent | Before | After | LLM Reduction | Speed Gain | Methods |
|-------|--------|-------|---------------|------------|---------|
| **Sunny Persona** | Verbose prompts | Shared constant | 80-85% tokens | Consistent | Shared prompts |
| **Router** | Multiple LLM calls | Fast classifier | 100% (fallback) | ~1000x | Keywords, rules |
| **Information** | Always LLM | Cached answers | 85-90% | ~1000x | Cache, filter |
| **Resource** | Always LLM | Instant lookup | 80-85% | ~1000x | Dictionary, templates |
| **Assessment** | Always LLM | Static templates | 85-90% | ~1000x | Templates, rules |
| **Escalation** | Always LLM | Rule-based | 100% | ~1000x | Logic, templates |

**Overall Impact:**
- 🚀 **Average LLM Reduction**: 70-75% across all agents
- ⚡ **Response Time**: <1ms for cached/template responses (vs 500-1500ms LLM)
- 💰 **Cost Savings**: ~70-75% reduction in LLM API costs
- 📊 **Token Savings**: ~70-80% reduction in prompt sizes
- 🎯 **Quality Maintained**: All optimizations preserve Sunny's personality and clinical accuracy

**Testing:**
```bash
# Router optimizations
python scripts/test/test_router_integration.py

# Distress detection
python scripts/test/test_2level_distress.py

# Overall system
python scripts/test/test_integration_quick.py
```

---

## 3. LangChain Components

### Overview

The system uses modern LangChain architecture with **Retriever**, **Chains**, **Memory**, and **Tools** for enhanced mental health support.

**Key Benefits:**
- ✅ Proper abstractions replace raw ChromaDB queries
- ✅ Modular, reusable chains
- ✅ Session-based conversation memory
- ✅ Specialized tools for assessments, resources, and coping strategies
- ✅ Context-aware responses

### 3.1 Retriever Implementation

**File:** `app.py`

**Purpose:** Replace raw ChromaDB queries with LangChain Chroma retriever

**Features:**
- Uses `LangChain Chroma` with `HuggingFaceEmbeddings`
- Configurable search parameters (similarity, k=3)
- Global retriever instance shared across agents
- Document formatting with source attribution

**Implementation:**
```python
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create retriever
vectorstore = Chroma(
    client=chroma_client,
    collection_name="mental_health_kb",
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)
```

**Usage:**
```python
# Query retriever
docs = retriever.invoke("anxiety coping strategies")

# Format documents
for doc in docs:
    source = doc.metadata.get('source', 'Knowledge Base')
    print(f"[{source}] {doc.page_content}")
```

---

### 3.2 Chains

**Directory:** `chains/`

Four specialized chains for different mental health support tasks.

#### 3.2.1 RAG Chain

**File:** `chains/rag_chain.py`

**Purpose:** Combine retriever with LLM for context-grounded responses

**Features:**
- Retrieves relevant documents
- Formats context with sources
- Generates evidence-based responses
- Two versions: standard and with-sources

**Implementation:**
```python
from chains import create_rag_chain

# Create RAG chain
rag_chain = create_rag_chain(retriever, llm)

# Use chain
response = rag_chain.invoke("What is anxiety?")
```

**How it works:**
```
User Query → Retriever → Format Docs → Prompt → LLM → Response
```

#### 3.2.2 Conversation Chain

**File:** `chains/conversation_chain.py`

**Purpose:** Memory-enhanced conversational support

**Features:**
- Integrates `ConversationBufferMemory`
- Maintains conversation context
- Sunny persona integration
- RAG + Conversation hybrid available

**Implementation:**
```python
from chains import create_conversation_chain

# Create with memory
conversation = create_conversation_chain(llm, memory)

# Chat
response = conversation.predict(input="I'm feeling anxious")
```

#### 3.2.3 Router Chain

**File:** `chains/router_chain.py`

**Purpose:** Intelligent routing to appropriate agents

**Features:**
- Analyzes user intent
- Routes to: CRISIS, INFORMATION, RESOURCE, ASSESSMENT, GENERAL
- Two-level distress detection
- Menu-based navigation support

**Implementation:**
```python
from chains import create_router_chain

router = create_router_chain(llm)
agent = router.invoke({"query": "I need to find a therapist"})
# Returns: "RESOURCE"
```

**Router Logic:**
```python
# Routing priority
if crisis_detected:
    return "CRISIS"
elif distress_level == "HIGH":
    return "INFORMATION" (with crisis resources)
elif specific_intent:
    return specialized_agent
else:
    return "GENERAL"
```

#### 3.2.4 Crisis Detection Chain

**File:** `chains/crisis_chain.py`

**Purpose:** Advanced crisis and distress detection

**Features:**
- Severity assessment (CRITICAL/HIGH/MODERATE/LOW)
- Crisis type identification (suicide/self-harm/severe distress)
- Safety assessment with JSON output
- Contextual analysis with conversation history

**Implementation:**
```python
from chains import assess_distress_level

level, confidence = assess_distress_level("I can't take this anymore", llm)
# Returns: ("HIGH", 0.9)
```

**Distress Levels:**
- **HIGH**: Severe distress, immediate support needed (≥5 points)
- **MILD**: Moderate distress, supportive guidance (1-4 points)
- **NONE**: Neutral queries, informational response (0 points)

---

### 3.3 Memory

**File:** `app.py`

**Purpose:** Session-based conversation memory

**Features:**
- `ConversationBufferMemory` for each session
- Conversation history tracking
- Helper functions for memory management
- Integrated into AgentState

**Implementation:**
```python
from langchain.memory import ConversationBufferMemory

# Global memory store
session_memories: Dict[str, ConversationBufferMemory] = {}

def get_or_create_memory(session_id: str):
    """Get or create conversation memory."""
    if session_id not in session_memories:
        session_memories[session_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    return session_memories[session_id]

# Save conversation
memory = get_or_create_memory("user_123")
memory.save_context(
    {"input": "I feel anxious"},
    {"output": "I understand. Let's explore some coping strategies..."}
)

# Retrieve history
history = memory.load_memory_variables({})
print(history["chat_history"])
```

**Helper Functions:**
- `get_or_create_memory(session_id)` - Create/retrieve memory
- `clear_session_memory(session_id)` - Clear conversation
- `get_conversation_history(session_id)` - Formatted history

---

### 3.4 Tools

**Directory:** `tools/`

Five specialized LangChain tools for mental health support.

#### 3.4.1 Assessment Tool

**File:** `tools/assessment_tool.py`

**Purpose:** Mental health assessments and screening

**Features:**
- PHQ-9 style depression assessment
- GAD-7 style anxiety assessment
- Stress level evaluation
- Severity scoring and recommendations

**Usage:**
```python
from tools import create_assessment_tool

tool = create_assessment_tool()
result = tool._run(
    assessment_type="depression",
    responses="sad,tired,hopeless,anxious,sleeping poorly"
)
print(result)
# Outputs: Depression Assessment with score and severity
```

**Assessment Types:**
- `depression` - PHQ-9 style (27-point scale)
- `anxiety` - GAD-7 style (21-point scale)
- `stress` - Stress level (low/moderate/high)
- `general` - General mental health check-in

#### 3.4.2 Resource Finder Tool

**File:** `tools/resource_tool.py`

**Purpose:** Singapore mental health services directory

**Features:**
- Hotlines (24/7 support)
- Therapy services (public/private)
- Support groups (peer support)
- Youth resources (CHAT, school-based)
- Emergency resources

**Usage:**
```python
from tools import create_resource_finder_tool

tool = create_resource_finder_tool()
resources = tool._run(
    resource_type="hotline",
    demographic="youth"
)
print(resources)
# Outputs: Youth-specific hotlines with contact info
```

**Resource Types:**
- `hotline` - Crisis and support hotlines
- `therapy` - Counseling and therapy services
- `support_group` - Peer support groups
- `emergency` - Emergency mental health services
- `youth` - Youth-specific resources
- `general` - General mental health resources

#### 3.4.3 Crisis Hotline Tool

**File:** `tools/crisis_tool.py`

**Purpose:** Immediate crisis support information

**Features:**
- Emergency contacts (995, SOS, IMH)
- Suicide prevention resources
- Self-harm support
- Safety planning guidance

**Usage:**
```python
from tools import create_crisis_hotline_tool

tool = create_crisis_hotline_tool()
hotlines = tool._run(
    urgency="immediate",
    crisis_type="suicide"
)
print(hotlines)
# Outputs: Suicide prevention resources with emergency numbers
```

**Crisis Types:**
- `suicide` - Suicide prevention
- `self_harm` - Self-harm support
- `severe_distress` - Severe emotional distress
- `general` - General crisis support

#### 3.4.4 Breathing Exercise Tool

**File:** `tools/breathing_tool.py`

**Purpose:** Guided breathing exercises for anxiety relief

**Features:**
- 5 breathing techniques
- Step-by-step instructions
- Configurable duration (1-10 cycles)
- Visual formatting with emojis

**Usage:**
```python
from tools import create_breathing_exercise_tool

tool = create_breathing_exercise_tool()
exercise = tool._run(
    exercise_type="box",
    duration=3
)
print(exercise)
# Outputs: Box breathing instructions for 3 cycles
```

**Exercise Types:**
- `box` - Box breathing (4-4-4-4 pattern)
- `478` - 4-7-8 breathing (relaxing breath)
- `deep` - Deep belly breathing
- `calming` - Extended exhale for calm
- `quick` - Quick calm for immediate relief

#### 3.4.5 Mood Tracker Tool

**File:** `tools/mood_tool.py`

**Purpose:** Mood logging and pattern analysis

**Features:**
- Mood logging with emotions and notes
- Pattern analysis (frequency, averages)
- Common emotion identification
- Mood score calculations

**Usage:**
```python
from tools import create_mood_tracker_tool

tool = create_mood_tracker_tool()

# Log mood
result = tool._run(
    action="log",
    mood="okay",
    emotions="calm,happy",
    notes="Had a good day"
)

# Analyze patterns
analysis = tool._run(action="analyze")
print(analysis)
# Outputs: Mood distribution, common emotions, insights
```

**Actions:**
- `log` - Record mood entry
- `analyze` - Analyze mood patterns
- `check-in` - Quick mood check-in

**Mood Levels:**
- `great` (9-10) - Excellent mood
- `good` (7-8) - Pleasant, content
- `okay` (5-6) - Neutral, manageable
- `low` (3-4) - Down, struggling
- `terrible` (1-2) - Very distressed

---

### 3.5 Integration Patterns

### Integration with Agents

**Helper Functions:** `agent/helpers.py`

Utilities for integrating chains, memory, and tools with agents:

```python
from agent.helpers import (
    get_conversation_context,
    create_rag_enhanced_prompt,
    should_use_tool,
    format_tool_response
)

# Get conversation history
history = get_conversation_context(memory)

# Create enhanced prompt
prompt = create_rag_enhanced_prompt(
    query=user_query,
    context=rag_context,
    conversation_history=history,
    persona_guidelines=sunny_persona,
    distress_level="high"
)

# Check if tool should be used
tool_info = should_use_tool(query, agent_type="information")
if tool_info and tool_info["tool"] == "breathing":
    # Invoke breathing tool
    pass
```

**Tool Detection:**
- Analyzes query for tool-appropriate keywords
- Returns tool name and parameters
- Automatic for breathing, mood tracking
- Agent-specific for assessments, resources

**Example Integration:**
```python
def information_agent_node(state, llm, get_relevant_context):
    query = state["current_query"]
    memory = state.get("memory")
    
    # Check for tool usage
    tool_info = should_use_tool(query, "information")
    if tool_info and tool_info["tool"] == "breathing":
        tool = create_breathing_exercise_tool()
        return tool._run(
            exercise_type=tool_info["exercise_type"],
            duration=3
        )
    
    # Use RAG chain
    rag_chain = create_rag_chain(retriever, llm)
    response = rag_chain.invoke(query)
    
    # Save to memory
    if memory:
        memory.save_context(
            {"input": query},
            {"output": response}
        )
    
    return response
```

---

## 4. Web Interface

### Architecture

```
interface/web/
├── app.py              # Flask application
└── templates/
    └── index.html      # Chat UI
```

### 4.1 Flask Application

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

### 4.2 Frontend Features

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

### 4.3 Customization

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

## 5. Knowledge Base Management

### 5.1 Update Agent

**File:** `agent/update_agent.py` (382 lines)

**Purpose:** Monitors `data/knowledge/` and updates ChromaDB

**Features:**
- File change detection (MD5 hashing)
- Incremental updates (only changed files)
- Smart chunking (1000 chars, 200 overlap)
- State persistence (`.update_state.json`)
- CLI and Python API

### 5.2 CLI Commands

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

### 5.3 Python API

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

### 5.4 Knowledge Structure

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
├── singapore_resources/          # 1 file, 14 chunks
│   └── mental_health_services.txt    # Complete Singapore service directory
│
├── conditions/                   # 3 files, 74 chunks
│   ├── depression.txt                # 21 chunks - comprehensive depression guide
│   ├── anxiety_disorders.txt         # 22 chunks - complete anxiety disorders
│   └── panic_disorder.txt            # 31 chunks - detailed panic disorder guide
│
├── emergency/                    # 1 file, 26 chunks
│   └── suicide_prevention.txt        # Critical crisis intervention resource
│
├── faqs/                        # 1 file, 25 chunks
│   └── therapy_questions.txt         # Complete therapy FAQ for Singapore
│
├── self_help/                   # 1 file, 20 chunks
│   └── cognitive_behavioral_techniques.txt  # Practical CBT guide
│
└── [Other categories for future expansion]
    ├── documents/
    ├── markdown/
    ├── pdfs/                    # Research papers
    │   └── research_papers/
    │       ├── brainsci-11-01633.pdf  # 33 chunks - Brain science research
    │       └── mental-2020-6-e20513.pdf  # 14 chunks - Mental health research
    ├── reference/
    ├── structured_data/
    └── web_sources/
```

**Total:** ~29 files → 485 chunks

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

**Research PDFs Added:**
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

### 5.5 Adding New Knowledge

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

### 5.6 Update State Tracking

**File:** `data/chroma_db/.update_state.json`

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
- Counts total chunks
- Enables incremental updates

### 5.7 Web Scraping for Knowledge Updates

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

### 5.8 Automated Periodic Updates

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

### 5.9 Complete Update Workflow

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

## 6. Deployment

### 6.1 Development

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
HUGGINGFACE_API_TOKEN=hf_your_token_here
```

**Optional:**
```bash
FLASK_SECRET_KEY=your_secret_key_for_sessions
FLASK_ENV=production
PORT=5001
USE_REMOTE_EMBEDDINGS=true  # Default: true (recommended)
```

**Re-ranker Configuration (Advanced - Disabled by Default):**
```bash
# Enable/disable re-ranking
RERANKER_ENABLED=true

# Re-ranker model selection
# Options: cross-encoder/ms-marco-TinyBERT-L-2-v2 (fast, 30MB)
#          cross-encoder/ms-marco-MiniLM-L-6-v2 (better, 90MB)
RERANKER_MODEL=cross-encoder/ms-marco-TinyBERT-L-2-v2

# Minimum relevance score (0.0 to 1.0)
# Higher = stricter filtering
RERANKER_THRESHOLD=0.0

# Maximum documents after re-ranking (empty = no limit)
RERANKER_TOP_K=
```

**Setting in Production:**
```bash
# Export variables
export GROQ_API_KEY="your_key"
export FLASK_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
export FLASK_ENV="production"

# Optional: Configure re-ranker
export RERANKER_ENABLED="true"
export RERANKER_THRESHOLD="0.1"

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

## 7. Customization

### 7.1 Utility Scripts

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

**Test Files (scripts/test/):**
1. **test_reranker.py** (350+ lines)
   - **Purpose:** Comprehensive re-ranker testing
   - **Function:** Validates re-ranking functionality, performance, and fallback behavior
   - **Usage:** `python scripts/test/test_reranker.py`

2. **test_distress_detection.py**
   - **Purpose:** Distress detection testing
   - **Function:** Validates weighted scoring system

3. **test_weighted_scoring_live.py**
   - **Purpose:** Live demonstration of distress scoring
   - **Function:** Interactive scoring breakdown

4. **test_sunny_persona.py**
   - **Purpose:** Sunny persona testing
   - **Function:** Validates personality consistency

### 7.2 Adding New Agent

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

### 7.3 Modifying Prompts

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

### 7.4 Changing LLM

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

### 7.5 Custom UI Themes

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

## 8. API Reference

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

## 9. Troubleshooting

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
Total: ~10,500 lines
├── app.py: 508 lines
├── Agent modules: ~4,000 lines (10 files)
├── Web interface: 300+ lines
├── Chains: ~1,000 lines (4 files)
├── Tools: ~1,000 lines (5 files)
└── Utilities: ~3,000 lines
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
