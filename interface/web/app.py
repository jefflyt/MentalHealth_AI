#!/usr/bin/env python3
"""
Flask Web Interface for AI Mental Health Support Agent
Provides a user-friendly web GUI for interacting with the multi-agent system
"""

import os
# Disable tokenizers parallelism warning for forked processes
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from flask import Flask, render_template, request, jsonify, session
import sys
from datetime import datetime
from dotenv import load_dotenv
import uuid

# Add parent directory to path to import agent system
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

# Import the agent system
from app import create_workflow, initialize_chroma, check_for_data_updates
from app import AgentState

# Load environment
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-in-production')

# Initialize the agent workflow
print("🔧 Initializing AI Mental Health Agent...")
check_for_data_updates()  # Check for data updates
initialize_chroma()  # Initialize ChromaDB
workflow = create_workflow()
print("✅ Agent system ready!")

# Store conversation history (in production, use a database)
conversations = {}

@app.route('/')
def index():
    """Main chat interface."""
    # Create new session ID if not exists
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        conversations[session['session_id']] = []
    
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages."""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        print(f"\n📝 User query: {user_message}")  # Debug log
        
        # Get or create session
        session_id = session.get('session_id', str(uuid.uuid4()))
        if session_id not in conversations:
            conversations[session_id] = []
        
        # Store user message
        conversations[session_id].append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Create initial state for the agent
        initial_state = AgentState(
            current_query=user_message,
            messages=[],
            current_agent="",
            crisis_detected=False,
            context="",
            distress_level="none"
        )
        
        # Run the workflow
        result = workflow.invoke(initial_state)
        
        # Extract agent response
        agent_messages = result.get('messages', [])
        agent_response = '\n\n'.join(agent_messages) if agent_messages else "I'm here to help. Could you tell me more?"
        
        print(f"🤖 Agent: {result.get('current_agent')}")  # Debug log
        print(f"💬 Response length: {len(agent_response)} chars")  # Debug log
        
        # Detect if crisis was handled
        crisis_detected = result.get('crisis_detected', False)
        
        # Store agent response
        conversations[session_id].append({
            'role': 'agent',
            'content': agent_response,
            'timestamp': datetime.now().isoformat(),
            'crisis': crisis_detected
        })
        
        return jsonify({
            'response': agent_response,
            'crisis': crisis_detected,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error in chat: {e}")
        import traceback
        traceback.print_exc()  # Full error trace
        return jsonify({
            'error': 'An error occurred processing your message',
            'response': "I'm sorry, I encountered an error. Please try again or contact support if the issue persists."
        }), 500

@app.route('/new-conversation', methods=['POST'])
def new_conversation():
    """Start a new conversation and reload agent modules."""
    global workflow
    
    try:
        # Create new session ID
        new_session_id = str(uuid.uuid4())
        session['session_id'] = new_session_id
        conversations[new_session_id] = []
        
        # Force reload of agent modules by clearing cache
        print("\n🔄 Reloading agent modules...")
        
        # Clear module cache for agent modules
        import importlib
        modules_to_reload = [
            'agent.information_agent',
            'agent.router_agent',
            'agent.crisis_agent',
            'agent.resource_agent',
            'agent.assessment_agent',
            'agent.escalation_agent'
        ]
        
        for module_name in modules_to_reload:
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
        
        # Reload main app module
        if 'app' in sys.modules:
            importlib.reload(sys.modules['app'])
        
        # Recreate workflow with fresh modules
        from app import create_workflow
        workflow = create_workflow()
        
        print("✅ Agent modules reloaded!")
        
        return jsonify({
            'message': 'New conversation started',
            'session_id': new_session_id,
            'modules_reloaded': True
        })
        
    except Exception as e:
        print(f"⚠️  Module reload error: {e}")
        # Still create new conversation even if reload fails
        new_session_id = str(uuid.uuid4())
        session['session_id'] = new_session_id
        conversations[new_session_id] = []
        
        return jsonify({
            'message': 'New conversation started',
            'session_id': new_session_id,
            'modules_reloaded': False
        })

@app.route('/history', methods=['GET'])
def get_history():
    """Get conversation history."""
    session_id = session.get('session_id')
    if not session_id or session_id not in conversations:
        return jsonify({'history': []})
    
    return jsonify({'history': conversations[session_id]})

@app.route('/assessment/<assessment_type>', methods=['POST'])
def start_assessment(assessment_type):
    """Handle self-assessment requests."""
    try:
        # Here you would integrate with your assessment agent
        # For now, return a placeholder response
        
        assessment_responses = {
            'dass21': {
                'title': 'DASS-21 Assessment Started',
                'message': 'I\'m here to guide you through a gentle mental health screening. Remember, this is just a helpful tool - not a diagnosis.',
                'questions': [
                    'Over the past week, how often have you felt down, depressed, or hopeless?',
                    'How often have you had trouble relaxing?',
                    'How often have you felt that you were pretty worthless?'
                ]
            },
            'mood': {
                'title': 'Quick Mood Check',
                'message': 'Let\'s take a moment to check in with how you\'re feeling right now.',
                'questions': [
                    'On a scale of 1-10, how would you rate your current mood?',
                    'How would you describe your energy level today?',
                    'What\'s one word that captures how you\'re feeling?'
                ]
            },
            'stress': {
                'title': 'Stress Level Check',
                'message': 'Stress is normal, but let\'s see how we can help you manage it.',
                'questions': [
                    'How overwhelmed do you feel by your current responsibilities?',
                    'How well are you sleeping lately?',
                    'What coping strategies have you tried recently?'
                ]
            }
        }
        
        if assessment_type in assessment_responses:
            response = assessment_responses[assessment_type]
            return jsonify({
                'success': True,
                'assessment': response,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'error': 'Assessment type not found',
                'available_types': list(assessment_responses.keys())
            }), 404
            
    except Exception as e:
        print(f"Error in assessment: {e}")
        return jsonify({
            'error': 'An error occurred starting the assessment'
        }), 500

@app.route('/tool/<tool_name>', methods=['GET'])
def get_tool(tool_name):
    """Provide tool content and exercises."""
    try:
        tools_content = {
            'breathing': {
                'title': '🫁 Breathing Exercises',
                'exercises': [
                    {
                        'name': '4-7-8 Breathing',
                        'description': 'Inhale for 4 counts, hold for 7, exhale for 8',
                        'benefits': 'Reduces anxiety and helps you sleep'
                    },
                    {
                        'name': 'Box Breathing',
                        'description': 'Inhale 4, hold 4, exhale 4, hold 4',
                        'benefits': 'Calms the nervous system'
                    }
                ]
            },
            'gratitude': {
                'title': '🙏 Gratitude Practice',
                'prompts': [
                    'What are 3 things you\'re grateful for today?',
                    'Who in your life are you thankful for?',
                    'What small wins did you have today?'
                ]
            },
            'affirmations': {
                'title': '💪 Positive Affirmations',
                'affirmations': [
                    'I am worthy of love and care',
                    'I am doing my best each day',
                    'My feelings are valid and important',
                    'I am stronger than I realize'
                ]
            }
        }
        
        if tool_name in tools_content:
            return jsonify({
                'success': True,
                'tool': tools_content[tool_name],
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'error': 'Tool not found',
                'available_tools': list(tools_content.keys())
            }), 404
            
    except Exception as e:
        print(f"Error getting tool: {e}")
        return jsonify({
            'error': 'An error occurred loading the tool'
        }), 500

@app.route('/resources', methods=['GET'])
def get_resources():
    """Get organized mental health resources."""
    try:
        resources = {
            'emergency': [
                {
                    'name': 'SOS Helpline',
                    'description': '24/7 emotional support',
                    'contact': '1767',
                    'type': 'phone'
                },
                {
                    'name': 'IMH Emergency',
                    'description': 'Psychiatric emergency services',
                    'contact': '6389-2222',
                    'type': 'phone'
                }
            ],
            'counseling': [
                {
                    'name': 'CHAT (Youth 16-30)',
                    'description': 'Free mental health assessment and counseling',
                    'contact': '6493-6500',
                    'website': 'https://www.chat.mentalhealth.sg/',
                    'type': 'phone'
                },
                {
                    'name': 'SAMH Counseling',
                    'description': 'Professional counseling services',
                    'website': 'https://www.samhealth.org.sg/',
                    'type': 'website'
                }
            ],
            'educational': [
                {
                    'name': 'HealthHub Mental Wellness',
                    'description': 'Government health information portal',
                    'website': 'https://www.healthhub.sg/live-healthy/mental_well-being',
                    'type': 'website'
                },
                {
                    'name': 'WHO Mental Health',
                    'description': 'Global mental health information',
                    'website': 'https://www.who.int/health-topics/mental-health',
                    'type': 'website'
                }
            ]
        }
        
        return jsonify({
            'success': True,
            'resources': resources,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error getting resources: {e}")
        return jsonify({
            'error': 'An error occurred loading resources'
        }), 500

if __name__ == '__main__':
    # Run the Flask app
    print("\n" + "="*60)
    print("🌐 AI Mental Health Support Agent - Web Interface")
    print("="*60)
    print("📍 Starting server at http://localhost:5001")
    print("🔧 Press CTRL+C to stop the server")
    print("="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )
