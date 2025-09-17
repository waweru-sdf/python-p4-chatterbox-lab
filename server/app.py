from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Message

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages]), 200

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    if not data.get("body") or not data.get("username"):
        return jsonify({"error": "Missing body or username"}), 400

    new_msg = Message(body=data["body"], username=data["username"])
    db.session.add(new_msg)
    db.session.commit()
    return jsonify(new_msg.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    msg = db.session.get(Message, id)
    if not msg:
        return jsonify({"error": f"Message {id} not found"}), 404

    data = request.get_json()
    if "body" in data:
        msg.body = data["body"]
    db.session.commit()
    return jsonify(msg.to_dict()), 200

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    msg = db.session.get(Message, id)
    if not msg:
        return jsonify({"error": f"Message {id} not found"}), 404

    db.session.delete(msg)
    db.session.commit()
    return '', 204

if __name__ == '__main__':  
    app.run(port=5555, debug=True)  