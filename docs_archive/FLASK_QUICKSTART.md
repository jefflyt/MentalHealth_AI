# 🌐 Flask Web Interface - Quick Start

## ✨ What's New

Your AI Mental Health Support Agent now has a **beautiful web interface**! No more command-line interaction - just open your browser and chat.

## 🚀 Getting Started (3 Steps)

### 1. Install Dependencies (if not already done)
```bash
pip install -r requirements.txt
```

### 2. Make sure your `.env` file has your API key
```bash
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Start the Web Server
```bash
python run_web.py
```

**That's it!** Open your browser and go to: **http://localhost:5001**

## 🎨 Features

### Beautiful Chat Interface
- 💬 Modern, gradient-themed design
- 📱 Mobile-responsive (works on phones/tablets)
- ⚡ Real-time messaging with typing indicators
- 🚨 Crisis detection with visual alerts
- 🔄 Start new conversations anytime

### Smart AI Integration
- 🤖 All 6 specialized agents working together
- 📚 RAG-enhanced responses from knowledge base
- 🇸🇬 Singapore-specific mental health resources
- 💭 Multi-turn conversations with context
- 🎯 Automatic routing to the right specialist

## 📸 What It Looks Like

```
┌─────────────────────────────────────────┐
│  🧠 AI Mental Health Support            │
│  A safe space for mental health         │
│  support and resources in Singapore     │
│  [🔄 New Conversation]                  │
├─────────────────────────────────────────┤
│                                         │
│  Welcome! How can I help you today?     │
│                                         │
│  I'm here to provide mental health      │
│  information, Singapore resources,      │
│  and support...                         │
│                                         │
├─────────────────────────────────────────┤
│ [Type your message here...    ] [Send] │
└─────────────────────────────────────────┘
```

## 🧪 Try These Sample Queries

1. **General Information:**
   - "I'm feeling anxious lately"
   - "What is depression?"
   - "Tell me about stress management"

2. **Singapore Resources:**
   - "Where can I get help in Singapore?"
   - "Tell me about CHAT services"
   - "Mental health clinics near me"

3. **Assessment:**
   - "How do I know if I have anxiety?"
   - "Tell me about DASS-21"
   - "Mental health screening"

4. **Coping Strategies:**
   - "Breathing exercises for anxiety"
   - "Mindfulness techniques"
   - "How to manage stress"

## 🔧 Configuration

### Change Port
Edit `web_app.py` line 105:
```python
port=5001,  # Change to any available port
```

### Customize Colors
Edit `templates/index.html` CSS (around line 12):
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## 📊 Architecture

```
User Browser
    ↓ HTTP Request
Flask Server (web_app.py)
    ↓ Message
Agent Router (agent/router_agent.py)
    ↓ Routes to appropriate agent
Specialized Agents (crisis/info/resource/assessment/escalation)
    ↓ Query ChromaDB
RAG Context Retrieval
    ↓ Context + Query
LLM (Groq Llama 3.3 70B)
    ↓ Response
Back to User Browser
```

## 🛡️ Security Features

- ✅ Session-based conversation management
- ✅ Secret key encryption for sessions
- ✅ CORS protection enabled
- ✅ Error handling with graceful fallbacks
- ✅ Crisis detection and alerts

## 📱 Mobile Support

The interface is fully responsive and works great on:
- 📱 iPhones and Android phones
- 📲 Tablets
- 💻 Desktop browsers
- 🖥️ Large monitors

## 🐛 Troubleshooting

### Port 5001 is Already in Use
```bash
# Option 1: Find and stop the process
lsof -i :5001
kill -9 <PID>

# Option 2: Use a different port in web_app.py
```

### Can't Connect to Server
```bash
# Check if server is running
curl http://localhost:5001/health

# Should return: {"status": "healthy", ...}
```

### Agent Not Responding
```bash
# Check if ChromaDB is updated
python agent/update_agent.py status

# Update if needed
python agent/update_agent.py auto
```

### API Key Issues
```bash
# Verify .env file
cat .env | grep GROQ_API_KEY

# Should show: GROQ_API_KEY=gsk_...
```

## 🎯 Development vs Production

### Development (Current Setup)
```bash
python run_web.py
# Good for testing, includes debugging
```

### Production Deployment
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn (better performance)
gunicorn -w 4 -b 0.0.0.0:5001 "interface.web.app:app"
```

## 📚 Documentation

- `WEB_INTERFACE_GUIDE.md` - Detailed technical guide
- `AGENT_STRUCTURE.md` - Agent architecture
- `README.md` - Project overview

## ⚡ Performance Tips

1. **First load is slow** - ChromaDB initializes (normal)
2. **Subsequent queries** - Much faster, cache is warm
3. **Multiple users** - Consider using Gunicorn with workers
4. **Large knowledge base** - Update agent handles it efficiently

## 🎉 You're All Set!

Your AI Mental Health Support Agent is now running with a beautiful web interface. Just:

1. Open http://localhost:5001 in your browser
2. Start chatting!
3. The AI will automatically route to the right specialist
4. Get Singapore-specific mental health support

**Enjoy your new web interface!** 🚀
