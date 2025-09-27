from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = [message.to_dict() for message in Message.query.all()]

        return make_response(
            jsonify(messages),
            200
        )
    
    elif request.method == "POST":
        request_body = request.get_json()
        message = Message(
            body=request_body["body"],
            username=request_body["username"]
        )

        db.session.add(message)
        db.session.commit()

        return make_response(
            jsonify(message.to_dict()),
            200
        )

@app.route('/messages/<int:id>', methods=["PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    if request.method == "PATCH":
        for column, value in request.get_json().items():
            if value != None:
                setattr(message, column, value)

        db.session.commit()

        return make_response(
            jsonify(message.to_dict()),
            200
        )
    
    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "msg": "message deleted"
        }

        return make_response(
            jsonify(response_body),
            200
        )

if __name__ == '__main__':
    app.run(port=5555)