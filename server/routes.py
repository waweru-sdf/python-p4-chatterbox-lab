from flask import Blueprint, request, jsonify
from models import db, Message

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([msg.to_dict() for msg in messages]), 200

@messages_bp.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    username = data.get('username')
    body = data.get('body')
    if not username or not body:
        return jsonify({'error': 'Username and body are required'}), 400
    message = Message(username=username, body=body)
    db.session.add(message)
    db.session.commit()
    return jsonify(message.to_dict()), 201

@messages_bp.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = db.session.get(Message, id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    data = request.get_json()
    body = data.get('body')
    if body is not None:
        message.body = body
        db.session.commit()
    return jsonify(message.to_dict()), 200

@messages_bp.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    db.session.delete(message)
    db.session.commit()
    return '', 204