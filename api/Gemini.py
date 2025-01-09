import random
import string
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db = SQLAlchemy(app)

def generate_user_id(length=7):
    return ''.join(random.choices(string.digits, k=length))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(200), nullable=False)

@app.route('/store_message', methods=['POST'])
def store_message():
    data = request.get_json()
    user_id = data.get('userId')
    message = data.get('message')
    
    if not user_id or not message:
        return jsonify({'error': 'userId and message are required'}), 400
    
    new_message = Message(user_id=user_id, message=message)
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify({'message': 'Message stored successfully'}), 201

@app.route('/get_message/<user_id>', methods=['GET'])
def get_message(user_id):
    message = Message.query.filter_by(user_id=user_id).first()
    if not message:
        return jsonify({'error': 'No message found for this user'}), 404
    
    return jsonify({'id': message.id, 'user_id': message.user_id, 'message': message.message}), 200

@app.route('/generate_user_id', methods=['GET'])
def generate_user_id_endpoint():
    user_id = generate_user_id()
    return jsonify({'userId': user_id}), 200

# ...existing code...

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
