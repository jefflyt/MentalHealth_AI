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

def build_assessment_context(assessment_results):
    """Build context string from assessment results for Sunny to use."""
    if not assessment_results:
        return ""
    
    assessment_type = assessment_results.get('assessmentType', 'unknown')
    timestamp = assessment_results.get('timestamp', 'recently')
    
    context_parts = [f"User recently completed a {assessment_type} assessment on {timestamp[:10]}. Key findings:"]
    
    if assessment_type == 'dass21':
        scores = assessment_results.get('scores', {})
        elevated_areas = []
        normal_areas = []
        
        for category, data in scores.items():
            level = data.get('level', 'unknown')
            score = data.get('score', 0)
            context_parts.append(f"- {category.title()}: {level} level (score: {score})")
            
            if level not in ['normal', 'minimal']:
                elevated_areas.append(category)
            else:
                normal_areas.append(category)
        
        # Add suggestions based on results
        if elevated_areas:
            context_parts.append(f"\nElevated areas needing support: {', '.join(elevated_areas)}")
            context_parts.append("Suggestions to offer:")
            
            if 'depression' in elevated_areas:
                context_parts.append("- Depression: Suggest gentle activities, social connection, and professional support if needed")
            if 'anxiety' in elevated_areas:
                context_parts.append("- Anxiety: Recommend breathing exercises, grounding techniques, and mindfulness")
            if 'stress' in elevated_areas:
                context_parts.append("- Stress: Suggest time management, relaxation techniques, and boundary setting")
        
        if normal_areas:
            context_parts.append(f"\nStrengths/healthy areas: {', '.join(normal_areas)}")
    
    elif assessment_type == 'mood':
        avg_score = assessment_results.get('averageScore', 'unknown')
        context_parts.append(f"- Overall mood score: {avg_score}/5.0")
        
        if float(avg_score) < 2.0:
            context_parts.append("Suggestions: Focus on basic self-care, gentle activities, and emotional support")
        elif float(avg_score) < 3.0:
            context_parts.append("Suggestions: Mood-boosting activities, social connection, and stress reduction")
        else:
            context_parts.append("Suggestions: Maintain positive habits and continue what's working")
        
    elif assessment_type == 'stress':
        level = assessment_results.get('level', 'unknown')
        percentage = assessment_results.get('percentage', 'unknown')
        context_parts.append(f"- Stress level: {level} ({percentage}%)")
        
        if level in ['high', 'very high']:
            context_parts.append("Suggestions: Urgent stress management, breathing exercises, and time management")
        elif level == 'moderate':
            context_parts.append("Suggestions: Regular stress-relief practices and boundary setting")
        else:
            context_parts.append("Suggestions: Continue current stress management and prevention strategies")
    
    context_parts.append("\nInstructions for Sunny: Be empathetic and acknowledge their courage in taking the assessment. Provide a gentle overview and practical suggestions. Don't mention specific scores unless relevant.")
    
    return " ".join(context_parts)

def is_vague_response(message):
    """Check if user response is vague and lacks specific information."""
    message_lower = message.lower().strip()
    
    # Single word vague responses
    single_word_vague = [
        'ok', 'okay', 'okie', 'yes', 'no', 'maybe', 'sure', 'fine', 'good', 'bad',
        'yeah', 'yep', 'nah', 'whatever', 'nothing', 'dunno', 'idk', 'hmm', 'um', 'uh'
    ]
    
    if message_lower in single_word_vague:
        return True
    
    # Short vague responses (under 15 characters)
    if len(message_lower) < 15:
        vague_patterns = [
            'i guess', 'not sure', 'don\'t know', 'nothing much', 'not really',
            'kinda', 'sorta', 'meh', 'blah', 'eh', 'alright', 'decent'
        ]
        return any(pattern in message_lower for pattern in vague_patterns)
    
    # Longer vague responses
    vague_indicators = [
        'i don\'t know', 'not sure', 'maybe', 'i guess', 'whatever',
        'nothing specific', 'just feeling', 'kind of', 'sort of',
        'not really sure', 'hard to explain', 'can\'t say', 'don\'t feel like',
        'everything', 'stuff', 'things', 'just tired',
        'just stressed', 'just sad', 'just okay', 'just fine'
    ]
    
    # Check if message contains vague indicators
    vague_count = sum(1 for indicator in vague_indicators if indicator in message_lower)
    
    # Consider it vague if it has vague indicators and is relatively short
    return vague_count > 0 and len(message_lower) < 50

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
        
        # Track vague responses for assessment suggestion
        if 'vague_response_count' not in session:
            session['vague_response_count'] = 0
        
        # Check if user response is vague or if they explicitly request assessment
        if user_message.lower().strip() == "suggest assessment":
            # Manual trigger for testing
            session['vague_response_count'] = 2
        elif is_vague_response(user_message):
            session['vague_response_count'] += 1
        else:
            session['vague_response_count'] = 0  # Reset on meaningful response
        
        # Build context with assessment results if available
        context = ""
        if 'assessment_results' in session:
            assessment = session['assessment_results']
            context = build_assessment_context(assessment)
            print(f"🧠 Assessment context added: {assessment.get('assessmentType', 'unknown')}")
        
        # Add assessment suggestion context if user has been vague
        suggest_assessment = False
        if session['vague_response_count'] >= 2:
            # For testing: suggest assessment even if there are recent results
            # In production, you might want to check for older results only
            suggest_assessment = True
        
        if suggest_assessment:
            # Make assessment suggestion the primary context, not secondary
            assessment_suggestion = "ASSESSMENT_SUGGESTION: The user has given vague responses. Gently suggest they take a self-assessment to better understand their mental state and provide more targeted support. Mention specific assessment options: DASS-21 for comprehensive screening, Quick Mood Check, or Stress Level Assessment."
            
            # Put assessment suggestion first if we have one
            if context:
                context = assessment_suggestion + " " + context
            else:
                context = assessment_suggestion
        
        # Debug logging
        print(f"🎯 Vague response count: {session['vague_response_count']}")
        print(f"🧠 Has assessment results: {'assessment_results' in session}")
        print(f"💡 Suggesting assessment: {suggest_assessment}")

        
        # Create initial state for the agent
        initial_state = AgentState(
            current_query=user_message,
            messages=[],
            current_agent="",
            crisis_detected=False,
            context=context,
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
        
        # Clear assessment results and vague response counter when starting new conversation
        if 'assessment_results' in session:
            del session['assessment_results']
            print("🧠 Cleared assessment results for new conversation")
        
        if 'vague_response_count' in session:
            del session['vague_response_count']
            print("🔄 Reset vague response counter for new conversation")
        
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
        
        # Clear assessment results even if reload fails
        if 'assessment_results' in session:
            del session['assessment_results']
        
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

@app.route('/store-assessment-results', methods=['POST'])
def store_assessment_results():
    """Store assessment results in session for Sunny's context."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No assessment data provided'}), 400
        
        # Store results in session
        session['assessment_results'] = data
        
        # Reset vague response counter when new assessment is completed
        session['vague_response_count'] = 0
        
        print(f"🧠 Stored {data.get('assessmentType', 'unknown')} assessment results for session")
        
        # Generate proactive conversation starter based on results
        conversation_starter = generate_assessment_conversation_starter(data)
        
        return jsonify({
            'success': True,
            'message': 'Assessment results stored successfully',
            'conversation_starter': conversation_starter,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error storing assessment results: {e}")
        return jsonify({
            'error': 'An error occurred storing assessment results'
        }), 500

def generate_assessment_conversation_starter(assessment_data):
    """Generate a proactive conversation starter based on assessment results."""
    assessment_type = assessment_data.get('assessmentType', 'assessment')
    
    if assessment_type == 'dass21':
        # Check for highest concern areas
        depression_level = assessment_data.get('depression', {}).get('level', 'normal')
        anxiety_level = assessment_data.get('anxiety', {}).get('level', 'normal')
        stress_level = assessment_data.get('stress', {}).get('level', 'normal')
        
        concerns = []
        if depression_level not in ['normal', 'minimal']:
            concerns.append('depression')
        if anxiety_level not in ['normal', 'minimal']:
            concerns.append('anxiety')
        if stress_level not in ['normal', 'minimal']:
            concerns.append('stress')
        
        if concerns:
            concern_text = ', '.join(concerns[:-1]) + (' and ' + concerns[-1] if len(concerns) > 1 else concerns[0])
            return f"Hi! I see you've completed the DASS-21 assessment and it shows some elevated {concern_text} levels. I'm here to support you - would you like to talk about what's been on your mind lately? 💙"
        else:
            return "Hi! Thanks for completing the DASS-21 assessment. It's great that your scores are in healthy ranges! I'm still here if you'd like to chat about anything on your mind. How are you feeling today? 😊"
    
    elif assessment_type == 'mood':
        avg_score = assessment_data.get('averageScore', 2.5)
        if avg_score < 2.0:
            return "Hi! I noticed from your mood check that you might be going through a tough time right now. I'm here to listen and support you. What's been weighing on your heart lately? 💙"
        elif avg_score < 3.0:
            return "Hi! Your mood check shows you're managing but there might be some challenges. I'm here to chat about whatever's on your mind. How has your day been? 💜"
        else:
            return "Hi! I'm glad to see from your mood check that you're doing well! I'm here if you'd like to share what's been going right for you, or if there's anything else you'd like to talk about. 😊"
    
    elif assessment_type == 'stress':
        stress_level = assessment_data.get('level', 'moderate')
        if stress_level in ['high', 'very high']:
            return "Hi! Your stress assessment shows you're dealing with quite a bit of stress right now. That must feel overwhelming. I'm here to help - would you like to talk about what's been most stressful for you lately? 💙"
        elif stress_level == 'moderate':
            return "Hi! I see you're experiencing some stress from your assessment. That's completely normal, and I'm here to support you. What's been on your mind that's causing you stress? 💜"
        else:
            return "Hi! It's wonderful that your stress levels are manageable right now! I'm here if you'd like to share what's been helping you stay balanced, or if there's anything else you'd like to discuss. 😊"
    
    return "Hi! Thanks for completing the assessment. I'm here to support you based on your results. How are you feeling right now? 💙"

@app.route('/get-conversation-starter', methods=['GET'])
def get_conversation_starter():
    """Get a conversation starter based on assessment results."""
    try:
        if 'assessment_results' not in session:
            return jsonify({'has_starter': False})
        
        assessment_data = session['assessment_results']
        conversation_starter = generate_assessment_conversation_starter(assessment_data)
        
        return jsonify({
            'has_starter': True,
            'message': conversation_starter,
            'assessment_type': assessment_data.get('assessmentType', 'assessment')
        })
        
    except Exception as e:
        print(f"Error getting conversation starter: {e}")
        return jsonify({'has_starter': False})

@app.route('/api/resources', methods=['GET'])
def get_resources():
    """Get organized mental health resources API endpoint."""
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

@app.route('/chat', methods=['GET'])
def chat_page():
    """Serve the chat interface template."""
    return render_template('chat.html')

@app.route('/assessment', methods=['GET'])
def assessment_page():
    """Serve the assessment interface template."""
    return render_template('assessment.html')

@app.route('/resources', methods=['GET'])
def resources_page():
    """Serve the resources interface template."""
    return render_template('resources.html')

@app.route('/tools', methods=['GET'])
def tools_page():
    """Serve the tools interface template."""
    return render_template('tools.html')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        return jsonify({
            "status": "healthy",
            "agent_system": "operational",
            "reranker_enabled": False,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
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
