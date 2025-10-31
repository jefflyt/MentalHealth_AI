# AI Mental Health Agent - Complete Project Implementation

## Project Overview
This repository contains a complete implementation of an AI-powered mental health support system using LangGraph multi-agent architecture, designed specifically for Singapore's mental health landscape.

## Core Technology Stack
- **LLM**: Groq with Llama 3.3 70B (fast, cost-effective inference)
- **Embeddings**: HuggingFace all-mpnet-base-v2 (768-dimensional sentence embeddings)
- **Vector Database**: Chroma (persistent vector storage with built-in collections)
- **Framework**: LangGraph (multi-agent workflow orchestration)
- **RAG**: Retrieval-Augmented Generation for grounded responses

## Project Structure

```
MentalHealth_AI/
├── 📖 README.md                   # Project overview and setup guide
├── 🧠 app.py                      # Main AI agent with ChromaDB
├── 🤖 update_agent.py             # Smart update agent for Knowledge management
├── 📦 requirements.txt            # Python dependencies (ChromaDB compatible)
├── � .env                        # Environment variables (API keys)
├── 🚫 .gitignore                  # Git ignore patterns
├── 📄 AI-MH-Agent-Final.md        # Master project documentation
├── 📋 AI-MH-Agent-PSD.md          # Project Specification Document
├── 📘 UPDATE_AGENT_GUIDE.md       # Smart update agent documentation
├── �️ data/                       # Application data
│   ├── chroma_db/                 # ChromaDB persistent storage (auto-created)
│   └── knowledge/                 # Mental health knowledge base
│       ├── mental_health_info/    # Depression, anxiety, stress information
│       ├── singapore_resources/   # IMH, CHAT, and local services
│       ├── coping_strategies/     # Breathing, mindfulness, CBT techniques
│       ├── dass21_guidelines/     # Clinical assessment tools
│       └── crisis_protocols/      # Emergency intervention procedures
└── 🐍 venv/                       # Python virtual environment
```

## System Architecture

### Multi-Agent Design
The system uses 5 specialized agents orchestrated by LangGraph:

1. **Router Agent**: Classifies incoming queries and routes to appropriate agent
2. **Crisis Intervention Agent**: Handles emergency mental health situations
3. **Information Agent**: Provides educational content about mental health
4. **Resource Agent**: Connects users with Singapore mental health services
5. **Assessment Agent**: Guides users through DASS-21 screening
6. **Human Escalation**: Routes complex cases to human professionals

### Knowledge Base Categories
- **Mental Health Information**: Depression, anxiety, stress management
- **Singapore Resources**: IMH, CHAT, Samaritans, local services
- **Coping Strategies**: Evidence-based self-help techniques
- **DASS-21 Guidelines**: Clinical assessment framework
- **Crisis Protocols**: Emergency intervention procedures

## Quick Start

### 🚀 **Simple Setup**
```bash
# Clone and setup
git clone <repository-url>
cd MentalHealth_AI

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your API key to .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env

# Start the agent (ChromaDB initializes automatically)
python app.py
```
```

#### Option B: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install PyTorch first (recommended for stability)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install all dependencies
pip install -r requirements.txt
```

#### Troubleshooting Import Errors
If you encounter `ModuleNotFoundError: No module named 'langchain'`:

1. **Python 3.13 Compatibility Issue** (Most Common):
   Python 3.13 is very new and some packages (like PyTorch) don't have wheels yet. Use the minimal requirements:
   ```bash
   pip install -r requirements-minimal.txt
   ```

2. **Ensure virtual environment is activated**:
   ```bash
   source venv/bin/activate  # You should see (venv) in your prompt
   ```

3. **Verify Python version** (requires Python 3.8+, but 3.9-3.12 recommended):
   ```bash
   python --version
   ```

4. **For Python 3.13 users**: Use the minimal installation first:
   ```bash
   # Install core functionality without PyTorch dependencies
   pip install -r requirements-minimal.txt
   
   # Then try to add embeddings support (may not work on Python 3.13)
   pip install sentence-transformers --no-deps  # Optional
   ```

5. **If you need full functionality**: Consider using Python 3.11 or 3.12:
   ```bash
   # Create new environment with older Python
   python3.11 -m venv venv-py311  # or python3.12
   source venv-py311/bin/activate
   pip install -r requirements.txt
   ```

### 2. Configure Environment Variables
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your API keys
GROQ_API_KEY=your_groq_api_key_here
HUGGINGFACE_API_TOKEN=your_hf_token_here  # Optional for local embeddings
```

### 3. Initialize Knowledge Base
```bash
# Run the ingestion pipeline
python ingestion.py

# This will:
# - Load all documents from data/ directories
# - Generate embeddings using HuggingFace model
# - Create Chroma vector database
# - Persist database to chroma_db/ folder
```

### 4. Start the Application
```bash
# Run the AI Mental Health Agent
python app.py

# The LangGraph workflow will be compiled and ready to handle queries
```

### 5. Test the System
```bash
# Run the test suite
python -m pytest tests/ -v

# Or test individual components
python -m pytest tests/test_router.py -v
python -m pytest tests/test_crisis_detection.py -v
```

## Key Features

### Crisis Detection System
- Zero false negative policy for safety
- Comprehensive keyword matching
- Immediate emergency resource provision
- Integration with Singapore crisis services

### RAG-Enhanced Responses
- Context-aware information retrieval
- Evidence-based mental health content
- Singapore-specific resource matching
- Culturally appropriate guidance

### DASS-21 Integration
- Standardized depression/anxiety/stress screening
- Clinical interpretation guidelines
- Automated scoring and recommendations
- Professional referral protocols

### Singapore Mental Health Resources
- Institute of Mental Health (IMH) services
- Community Health Assessment Team (CHAT)
- Samaritans of Singapore crisis support
- Polyclinic and private practice referrals

## Sample Interactions

### General Mental Health Query
```
User: "I've been feeling really down lately and having trouble sleeping"
System: → Router Agent → Information Agent → Retrieval → Depression + Sleep info
Response: Evidence-based information about depression symptoms with local resources
```

### Crisis Detection
```
User: "I don't want to live anymore"
System: → Router Agent → Crisis Agent → Immediate Safety Protocol
Response: Immediate crisis resources, safety planning, emergency contacts
```

### Resource Request
```
User: "Where can I get mental health help in Singapore?"
System: → Router Agent → Resource Agent → Singapore Services Retrieval
Response: IMH, CHAT, polyclinics, private options with contact details
```

### Assessment Request
```
User: "Can you help me assess my mental health?"
System: → Router Agent → Assessment Agent → DASS-21 Protocol
Response: Guided DASS-21 questionnaire with interpretation
```

## Development Guidelines

### Adding New Content
1. Create appropriate files in `data/` subdirectories
2. Run `python ingestion.py` to update vector database
3. Test retrieval with relevant queries

### Modifying Agents
1. Update agent logic in `app.py`
2. Modify state schema if needed
3. Test agent routing and responses
4. Update tests in `tests/` directory

### Enhancing Crisis Detection
1. Update keyword lists in `utils/crisis_detection.py`
2. Add new detection patterns
3. Test thoroughly to avoid false negatives
4. Document changes for safety audit

## Safety Considerations

### Crisis Response Protocol
- Immediate identification of high-risk users
- Provision of emergency contact information
- Clear escalation pathways to human support
- Documentation of all crisis interactions

### Data Privacy
- No personal data persistence
- Session-based interaction only
- Secure API key management
- Compliance with healthcare privacy standards

### Clinical Limitations
- AI system provides support, not diagnosis
- Clear boundaries on clinical advice
- Emphasis on professional consultation
- Regular updates to clinical content

## Monitoring and Maintenance

### System Health Checks
- Monitor API response times
- Track vector database performance  
- Validate crisis detection accuracy
- Review user interaction patterns

### Content Updates
- Regular review of mental health information
- Updates to Singapore resource listings
- Validation of crisis contact information
- Integration of new evidence-based practices

## Documentation

- **AI-MH-Agent-Final.md**: Complete project documentation and implementation guide
- **AI-MH-Agent-PSD.md**: Project Specification Document with technical requirements
- Individual component documentation in respective files

## Testing

The test suite covers:
- Router agent classification accuracy
- Crisis detection sensitivity and specificity
- RAG retrieval relevance and accuracy
- Integration between system components

## Troubleshooting

### Common Issues and Solutions

#### `ModuleNotFoundError: No module named 'langchain'`
**Solution:**
1. Ensure virtual environment is activated: `source venv/bin/activate`
2. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
3. Try manual installation: `pip install langchain langgraph langchain-groq`

#### `ImportError: No module named 'sentence_transformers'`
**Solution:**
1. Install PyTorch first: `pip install torch`
2. Then install sentence-transformers: `pip install sentence-transformers`

#### `GROQ_API_KEY not found` Error
**Solution:**
1. Copy environment template: `cp .env.example .env`
2. Edit `.env` file and add your Groq API key
3. Get API key from: https://console.groq.com/

#### Vector database initialization fails
**Solution:**
1. Ensure `chroma_db/` directory exists: `mkdir -p chroma_db`
2. Run ingestion pipeline: `python ingestion.py`
3. Check file permissions in the project directory

#### Import errors with transformers/torch
**Solution:**
1. Install PyTorch separately: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu`
2. Then install transformers: `pip install transformers sentence-transformers`

### System Requirements
- **Python**: 3.8 or higher (3.9-3.12 recommended, 3.13 has compatibility issues)
- **Memory**: Minimum 4GB RAM (8GB recommended for full functionality)
- **Storage**: ~1GB for basic functionality, ~2GB for full vector database
- **OS**: macOS, Linux, or Windows with WSL

### Python 3.13 Users
If you're using Python 3.13, some dependencies (like PyTorch) may not have wheels available yet. Use the simplified version:

1. **Install core dependencies**: `pip install -r requirements-minimal.txt`
3. **Run the app**: `python app.py` (works without embeddings)
3. **Test system**: `python test_core.py`

For full functionality, consider using Python 3.11 or 3.12.

### Getting Help
1. Check the troubleshooting section above
2. Verify all dependencies are installed correctly
3. Ensure API keys are properly configured
4. Review error logs for specific issues

## Contributing

1. Review the Project Specification Document (AI-MH-Agent-PSD.md)
2. Follow coding standards and documentation requirements
3. Ensure all tests pass before submitting changes
4. Prioritize safety in crisis detection modifications

## License and Disclaimer

This system is designed for educational and research purposes. It should not replace professional mental health services. Users experiencing mental health crises should contact appropriate emergency services or mental health professionals immediately.

Singapore Emergency: 995
Singapore Crisis Support: SOS 1767, IMH 6389-2222

## ✅ ChromaDB Integration Active

### 🎉 **ChromaDB is Now Fully Integrated with Smart Updates!**

The application now uses **ChromaDB with semantic search** and **automatic update detection**:

#### 🚀 **What's Working:**
- ✅ **ChromaDB persistent storage** in `chroma_db/` directory
- ✅ **Automatic embeddings** using all-MiniLM-L6-v2 (works with Python 3.13!)
- ✅ **5 knowledge collections** automatically populated from `data/` directory
- ✅ **Semantic search** for relevant mental health information
- ✅ **RAG (Retrieval-Augmented Generation)** for context-aware responses
- ✅ **Smart Update Agent** - Automatically detects new/modified files!

#### 🤖 **Smart Update Agent:**
The app now includes an intelligent agent that monitors `data/knowledge/` folder:
- **Auto-detects** new `.txt` files
- **Tracks changes** via file hashing
- **Smart updates** - only processes new/modified content
- **Integrated** - Runs automatically when you start the app

**Manual update commands:**
```bash
python update_agent.py check    # Check for new data
python update_agent.py auto     # Smart update if needed
python update_agent.py status   # View current state
```

See [UPDATE_AGENT_GUIDE.md](UPDATE_AGENT_GUIDE.md) for complete documentation.

#### 📊 **ChromaDB Collections:**
```
data/chroma_db/
├── mental_health_info/      # 12 documents: Depression, anxiety, stress
├── singapore_resources/     # 9 documents: IMH, CHAT services
├── coping_strategies/       # 23 documents: Breathing, mindfulness, CBT
├── dass21_guidelines/       # 21 documents: Assessment tools
└── crisis_protocols/        # 21 documents: Emergency procedures
```

#### 💡 **How It Works:**
1. **First Run**: Automatically creates collections and populates from `data/knowledge/` directory
2. **Subsequent Runs**: Loads existing collections instantly
3. **User Queries**: Uses semantic search to find relevant context
4. **AI Responses**: Enhanced with retrieved knowledge base information

#### 🔍 **Technical Details:**
- **Embedding Model**: all-MiniLM-L6-v2 (384 dimensions, fast, works without PyTorch)
- **Text Chunking**: 1000 chars with 200 char overlap for optimal retrieval
- **Storage**: Persistent SQLite database with automatic indexing
- **Query**: Top-3 relevant documents retrieved for each user question

---

For detailed technical specifications, implementation guidance, and clinical considerations, refer to the comprehensive documentation files included in this repository.