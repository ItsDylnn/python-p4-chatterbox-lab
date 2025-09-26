from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Message

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatterbox.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/messages", methods=["GET"])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages]), 200

@app.route("/messages", methods=["POST"])
def create_message():
    data = request.get_json()
    if not data.get("body") or not data.get("username"):
        return jsonify({"error": "Missing body or username"}), 400

    message = Message(body=data["body"], username=data["username"])
    db.session.add(message)
    db.session.commit()
    return jsonify(message.to_dict()), 201

@app.route("/messages/<int:id>", methods=["PATCH"])
def update_message(id):
    data = request.get_json()
    message = Message.query.get_or_404(id)
    if "body" in data:
        message.body = data["body"]
    db.session.commit()
    return jsonify(message.to_dict()), 200

@app.route("/messages/<int:id>", methods=["DELETE"])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
