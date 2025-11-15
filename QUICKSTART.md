# ⚡ Quick Start Guide

Get the AI Mental Health Support Agent running in 5 minutes!

## 🎯 Prerequisites

- **Miniconda/Anaconda (recommended)** – the included `activate_env.sh` script uses `conda` to manage a `mentalhealth_py311` environment with Python 3.11.13 so that `torch>=2.0.0` installs correctly
- **Python 3.11.13** (installed automatically by the script)
- **Git** (for cloning)
- **Groq API Key** ([Get one free](https://console.groq.com/))

## 🚀 3-Step Setup

### Step 1: Prepare the Python 3.11 Environment

```bash
# Clone the repository (if not already)
git clone <your-repo-url>
cd MentalHealth_AI

# Run the helper script (creates + activates conda env, installs requirements)
source activate_env.sh
```

If you prefer not to use `activate_env.sh`, you can still create a Python 3.11 virtual environment manually, but make sure `torch>=2.0.0` and `sentence-transformers>=2.2.0` install on that interpreter.

### Step 2: Configure API Key

```bash
# Create .env file
echo "GROQ_API_KEY=your_actual_groq_api_key_here" > .env
```

**Get your Groq API key:**
1. Go to https://console.groq.com/
2. Sign up (free!)
3. Create an API key
4. Copy and paste it into `.env`

### Step 3: Launch the App

**Important:** Make sure your virtual environment is activated!

```bash
# Activate venv first (if not already)
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Run the app
python run_web.py
```

**Alternative:** Use the full path to venv Python:
```bash
./venv/bin/python run_web.py  # macOS/Linux
# OR
venv\Scripts\python run_web.py  # Windows
```

**That's it!** Open your browser and go to:
```
http://localhost:5001
```

## 🎉 You're Ready!

You should see a beautiful chat interface. Try asking:
- "I'm feeling anxious"
- "Where can I get help in Singapore?"
- "Tell me about stress management"

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'chromadb'" or similar

**Cause:** You're using the system Python instead of the virtual environment.

**Solution:**
```bash
# Make sure venv is activated (you should see (venv) in terminal)
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Verify you're using venv Python
which python  # Should show path to venv/bin/python

# If still having issues, reinstall dependencies
pip install -r requirements.txt
```

**Alternative:** Use the full path:
```bash
./venv/bin/python run_web.py  # macOS/Linux
```

### "Port 5001 is already in use"

**Solution 1 - Use different port:**
Edit `run_web.py` and change:
```python
port=5001,  # Change to 5002 or any available port
```

**Solution 2 - Kill the process:**
```bash
# Find what's using port 5001
lsof -i :5001

# Kill it (replace PID with actual number)
kill -9 <PID>
```

### "GROQ_API_KEY not found"

**Solution:**
```bash
# Check if .env exists
cat .env

# Should show: GROQ_API_KEY=gsk_...
# If not, create it:
echo "GROQ_API_KEY=your_key_here" > .env
```

### "ChromaDB initialization failed"

**Solution:**
```bash
# Check for updates
python agent/update_agent.py auto

# Or force rebuild
python agent/update_agent.py force
```

### Python 3.13 Compatibility

All dependencies are compatible with Python 3.13! If you have issues:

```bash
# Verify Python version
python --version

# Should show 3.9.x through 3.13.x
# If older, upgrade Python first
```

---

## 📱 Using the Web Interface

### Main Features

1. **Chat Box** - Type your message
2. **Send Button** - Submit query
3. **New Conversation** - Clear history and start fresh
4. **Crisis Banner** - Shows if crisis is detected

### Sample Conversations

**🔴 HIGH Distress (immediate structured support):**
```
You: i dont feel good
Bot: I hear you, and I'm really glad you reached out to me. 💙
It sounds like you're going through a really tough time right now...

I can support you with:
1️⃣ Understanding what you're feeling
2️⃣ Coping strategies that can help right now
3️⃣ Connecting you to professional support in Singapore
4️⃣ Just being here to listen - whatever you need
```

**🟡 MODERATE Distress (warm support menu):**
```
You: I'm feeling really anxious
Bot: Hey there, I'm Sunny, and I'm here for you. 💙
I can help with whatever you're going through.

I can help with:
1️⃣ Understanding your feelings
2️⃣ Coping strategies and techniques
3️⃣ Finding support services in Singapore
4️⃣ Just someone to talk to - I'm a good listener!
```

**🟢 MILD Distress (friendly welcome):**
```
You: i need help
Bot: Hi there! I'm Sunny, and I'm here to support you. 💙 😊

What would you like help with?
• Understanding emotions
• Coping strategies
• Support services in Singapore
• Or just talk - I'm a good listener!

What's on your mind today?
```

**Assessment Suggestion (after vague responses):**
```
You: ok (repeated 2+ times)
Bot: I hear you, and I'm here to support you. I've noticed you've given...
[Longer response suggesting self-assessment with DASS-21 options]
```

**Resource Request:**
```
You: Where can I get help in Singapore?
Bot: [Lists CHAT services, IMH, contact details]
```

**Crisis Detection:**
```
You: I'm having thoughts of self-harm
Bot: 🚨 [Immediate crisis support + emergency contacts]
```

---

## 🔧 Advanced Options

### Update Knowledge Base

```bash
# Check for new/modified files
python agent/update_agent.py check

# Auto-update if changes detected
python agent/update_agent.py auto

# View current state
python agent/update_agent.py status

# Force full rebuild
python agent/update_agent.py force
```

### Run in Production

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn (better performance)
gunicorn -w 4 -b 0.0.0.0:5001 "interface.web.app:app"
```

### Custom Port

Edit `run_web.py`:
```python
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8080,  # Change this
        debug=True
    )
```

### Add New Knowledge

**Supported File Formats:**
- 📄 `.txt` - Plain text (always supported)
- 📝 `.md` - Markdown files (always supported)
- 📋 `.pdf` - PDF documents (requires PyPDF2)
- 📄 `.docx` - Word documents (requires python-docx)
- 🌐 `.html/.htm` - HTML files (requires beautifulsoup4 - already installed)
- 📊 `.csv` - CSV data (requires pandas)
- 🔧 `.json` - JSON data (always supported)

**Adding New Content:**

1. **Basic Text Files** (no extra setup needed):
   ```bash
   # Add .txt or .md files to appropriate category
   echo "Content here" > data/knowledge/mental_health_info/new_topic.txt
   ```

2. **PDF/DOCX Files** (requires optional libraries):
   ```bash
   # First, install format support
   pip install PyPDF2 python-docx pandas openpyxl
   
   # Then add files to knowledge folder
   cp clinical_guidelines.pdf data/knowledge/clinical_guidelines/
   cp treatment_protocol.docx data/knowledge/crisis_protocols/
   ```

3. **Structured Data** (CSV/JSON):
   ```bash
   # Add resource lists or FAQs
   cp singapore_resources.csv data/knowledge/singapore_resources/
   cp faqs.json data/knowledge/faqs/
   ```

4. **Update ChromaDB:**
   ```bash
   python agent/update_agent.py auto
   ```

5. **Restart app:**
   ```bash
   python run_web.py
   ```

**Best Practices:**
- **PDFs:** Great for clinical guidelines, research papers
- **Word Docs:** Good for structured protocols, reports
- **CSV:** Perfect for resource directories, contact lists
- **JSON:** Ideal for FAQ databases, structured Q&A
- **Markdown:** Best for formatted documentation
- **Plain Text:** Simple, reliable, always works

**Format Support Status:**

When you run the UpdateAgent, you'll see:
```
📁 Multi-Format Support Status:
  ✅ Plain Text (.txt, .md)
  ✅ PDF Documents (.pdf) [if PyPDF2 installed]
  ✅ Word Documents (.docx) [if python-docx installed]
  ✅ HTML Files (.html, .htm)
  ✅ CSV Data (.csv) [if pandas installed]
  ✅ JSON Data (.json)
```

---

## 📊 System Check

### Verify Installation

```bash
# Test imports
python -c "from interface.web.app import app; print('✅ Flask OK')"

# Test agents
python -c "from agent import router_node; print('✅ Agents OK')"

# Check ChromaDB
python agent/update_agent.py status
```

**Should see:**
```
✅ Flask OK
✅ Agents OK
📚 Current ChromaDB State:
   Collection: mental_health_kb
   Total chunks: 168
   ...
```

### Health Check Endpoint

```bash
# While app is running
curl http://localhost:5001/health
```

**Should return:**
```json
{
  "status": "healthy",
  "agent_system": "operational",
  "timestamp": "2025-10-31T..."
}
```

---

## 🎓 Next Steps

### Learn More
- **[README.md](README.md)** - Project overview
- **[GUIDE.md](GUIDE.md)** - Complete technical guide

### Customize
- Modify agents in `agent/` folder
- Update UI in `interface/web/templates/index.html`
- Add knowledge in `data/knowledge/`

### Deploy
- See [GUIDE.md](GUIDE.md) → Deployment section
- Use Gunicorn for production
- Set environment variables properly

---

## ✅ Quick Reference

### Start App (Choose One)
```bash
# Option 1: With activated venv (recommended)
source venv/bin/activate
python run_web.py

# Option 2: Direct path to venv Python
./venv/bin/python run_web.py  # macOS/Linux
venv\Scripts\python run_web.py  # Windows
```

### Update Knowledge
```bash
# With activated venv
python agent/update_agent.py auto

# OR with full path
./venv/bin/python agent/update_agent.py auto
```

### Check Status
```bash
# With activated venv
python agent/update_agent.py status
curl http://localhost:5001/health

# OR with full path
./venv/bin/python agent/update_agent.py status
```

### Stop App
```
Press CTRL+C in terminal
```

---

## 🆘 Need Help?

1. **Most common issue:** Not using virtual environment
   - Make sure you see `(venv)` in your terminal prompt
   - Or use full path: `./venv/bin/python run_web.py`
2. **Check troubleshooting** section above
3. **Read [GUIDE.md](GUIDE.md)** for details
4. **Check terminal** for error messages
5. **Verify `.env` file** has API key
6. **Test your setup:**
   ```bash
   # Verify venv Python has dependencies
   ./venv/bin/python -c "import chromadb; print('✅ OK')"
   ```

---

**Ready to go?** 

1. **Activate venv:** `source venv/bin/activate`
2. **Run app:** `python run_web.py`
3. **Open browser:** http://localhost:5001

🎉 Enjoy!
