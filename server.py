from flask import Flask, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
import uuid
import json
from dotenv import load_dotenv
from os import environ
import llm

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Chat(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # Unique chat ID
    messages = db.Column(db.Text, default='[]')  # Stores chat history as JSON

# Initialize database
with app.app_context():
    db.create_all()

@app.route('/new', methods=['POST'])
def new_chat():
    """Creates a new chat session and returns its ID."""
    chat_id = str(uuid.uuid4())  # Generate a unique chat ID
    new_chat = Chat(id=chat_id, messages=json.dumps([]))
    db.session.add(new_chat)
    db.session.commit()
    return jsonify({'chat_id': chat_id, 'url': url_for('get_chat', chat_id=chat_id, _external=True)}), 201

@app.route('/chat/<chat_id>', methods=['GET'])
def get_chat(chat_id):
    """Retrieves previous messages of a chat session."""
    chat = db.session.get(Chat, chat_id)
    if not chat:
        return jsonify({'error': 'Chat not found'}), 404
    return jsonify({'chat_id': chat_id, 'messages': json.loads(chat.messages)})

@app.route('/chat/<chat_id>', methods=['POST'])
def send_message(chat_id):
    """Stores a new message and returns an AI-generated response."""
    chat = db.session.get(Chat, chat_id)
    if not chat:
        return jsonify({'error': 'Chat not found'}), 404
    
    data = request.get_json()
    if 'message' not in data:
        return jsonify({'error': 'Message is required'}), 400
    
    # Store user message
    messages = json.loads(chat.messages)
    messages.append({'role': 'user', 'content': data['message']})

    # Get AI responset
    try:
        ai_response = llm.get_response(messages=messages)
        messages.append({'role': 'assistant', 'content': ai_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    # Save back to DB
    chat.messages = json.dumps(messages)
    db.session.commit()

    return jsonify({'chat_id': chat_id, 'messages': messages, 'response': ai_response})

if __name__ == '__main__':
    app.run(debug=environ.get('DEBUG'))
