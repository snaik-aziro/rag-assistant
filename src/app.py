#!/usr/bin/env python3
"""
Flask Web Server for RAG Chatbot UI
"""

import os
import sys
from pathlib import Path

# Add src directory to path
src_dir = Path(__file__).parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from chatbot import LocalChatbot

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)

# Initialize chatbot instance
chatbot_instance = None

def get_chatbot():
    """Get or create chatbot instance"""
    global chatbot_instance
    if chatbot_instance is None:
        chatbot_instance = LocalChatbot(
            model_name=os.getenv('OLLAMA_MODEL', 'llama2'),
            ollama_host=os.getenv('OLLAMA_HOST', 'http://localhost:11434'),
            use_rag=True
        )
        
        # Initialize Ollama if needed
        if not chatbot_instance.check_ollama_running():
            chatbot_instance.start_ollama_service()
        
        # Check and pull model
        chatbot_instance.check_and_pull_model()
    
    return chatbot_instance

@app.route('/')
def index():
    """Serve the main UI page"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        chatbot = get_chatbot()
        response = chatbot.generate_response(user_message)
        
        if response:
            return jsonify({
                'success': True,
                'response': response,
                'model': chatbot.model_name,
                'rag_enabled': chatbot.use_rag
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to generate response. Please ensure Ollama is running.'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    try:
        chatbot = get_chatbot()
        chatbot.conversation_history = []
        return jsonify({'success': True, 'message': 'History cleared'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def status():
    """Get chatbot status"""
    try:
        chatbot = get_chatbot()
        ollama_running = chatbot.check_ollama_running()
        
        return jsonify({
            'success': True,
            'ollama_running': ollama_running,
            'model': chatbot.model_name,
            'rag_enabled': chatbot.use_rag
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting RAG Chatbot Web Server...")
    print("📱 Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5002)

