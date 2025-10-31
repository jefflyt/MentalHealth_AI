# Flask Web Interface Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file with:
```bash
GROQ_API_KEY=your_groq_api_key_here
FLASK_SECRET_KEY=your_secret_key_here  # Optional, will auto-generate if not set
```

### 3. Run the Web Application
```bash
python run_web.py
```

The web interface will be available at: **http://localhost:5001**

## Features

### 🎨 User Interface
- **Clean, modern chat interface** with gradient design
- **Real-time messaging** with typing indicators
- **Crisis detection** with visual alerts
- **Mobile responsive** design
- **Conversation management** (start new conversations)

### 🤖 AI Agent Integration
- **Automatic routing** to appropriate specialist agents
- **RAG-enhanced responses** using ChromaDB knowledge base
- **Crisis intervention** with immediate alerts
- **Singapore-specific** mental health resources
- **Multi-turn conversations** with context retention

### 🔒 Security Features
- **Session management** for conversation privacy
- **CORS protection** enabled by default
- **Secret key** for session encryption
- **Error handling** with graceful fallbacks

## API Endpoints

### GET `/`
- Main chat interface (HTML page)

### POST `/chat`
- Send a message to the AI agent
- **Request body:**
  ```json
  {
    "message": "Your message here"
  }
  ```
- **Response:**
  ```json
  {
    "response": "Agent response",
    "crisis": false,
    "timestamp": "2025-10-31T..."
  }
  ```

### POST `/new-conversation`
- Start a new conversation (clears history)
- **Response:**
  ```json
  {
    "message": "New conversation started",
    "session_id": "uuid"
  }
  ```

### GET `/history`
- Get conversation history for current session
- **Response:**
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

### GET `/health`
- Health check endpoint
- **Response:**
  ```json
  {
    "status": "healthy",
    "agent_system": "operational",
    "timestamp": "2025-10-31T..."
  }
  ```

## File Structure

```
MentalHealth_AI/
├── run_web.py              # Launch script for web interface
├── interface/
│   └── web/
│       ├── app.py          # Flask application
│       ├── templates/
│       │   └── index.html  # Main chat interface
│       └── static/         # Static assets (CSS, JS, images)
├── app.py                  # Agent system (backend)
├── agent/                  # Agent modules
│   ├── router_agent.py
│   ├── crisis_agent.py
│   ├── information_agent.py
│   ├── resource_agent.py
│   ├── assessment_agent.py
│   ├── escalation_agent.py
│   └── update_agent.py
└── data/
    ├── knowledge/          # Knowledge base
    └── chroma_db/          # Vector database
```

## Development

### Running in Development Mode
```bash
# Already configured in run_web.py
python run_web.py
```

### Running in Production
```bash
# Use a production WSGI server like Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 "interface.web.app:app"
```

### Environment Variables
```bash
# Required
GROQ_API_KEY=your_api_key

# Optional
FLASK_SECRET_KEY=your_secret_key
FLASK_ENV=production
```

## Customization

### Change Port
Edit `run_web.py`:
```python
app.run(port=8080)  # Change from 5001 to 8080
```

Or edit `interface/web/app.py` if running directly.

### Modify UI Colors
Edit `interface/web/templates/index.html` CSS:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
/* Change to your preferred colors */
```

### Add Custom Routes
In `interface/web/app.py`:
```python
@app.route('/custom-endpoint')
def custom_function():
    return jsonify({'message': 'Custom response'})
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use a different port in web_app.py
```

### ChromaDB Issues
```bash
# Update ChromaDB
python agent/update_agent.py auto
```

### API Key Issues
```bash
# Check .env file exists
cat .env

# Verify GROQ_API_KEY is set
echo $GROQ_API_KEY
```

## Testing

### Manual Testing
1. Open browser: http://localhost:5000
2. Try different queries:
   - "I'm feeling anxious"
   - "Where can I get help in Singapore?"
   - "Tell me about DASS-21"
   - "I'm having thoughts of self-harm" (crisis test)

### API Testing with curl
```bash
# Health check
curl http://localhost:5000/health

# Send a message
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 web_app:app
```

### Using Docker
Create `Dockerfile`:
```dockerfile
FROM python:3.13
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "web_app.py"]
```

### Environment Configuration
Set these in your hosting platform:
- `GROQ_API_KEY` (required)
- `FLASK_SECRET_KEY` (recommended)
- `FLASK_ENV=production`

## Support

For issues or questions:
1. Check the main README.md
2. Review AGENT_STRUCTURE.md for agent details
3. Check logs in terminal for error messages
