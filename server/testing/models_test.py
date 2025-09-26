from datetime import datetime
from app import app
from models import db, Message

class TestMessage:

    with app.app_context():
        messages = Message.query.filter(
            Message.body == "Hello 👋",
            Message.username == "Liza"
        ).all()
        for m in messages:
            db.session.delete(m)
        db.session.commit()

    def test_has_correct_columns(self):
        with app.app_context():
            m = Message(body="Hello 👋", username="Liza")
            db.session.add(m)
            db.session.commit()

            assert m.body == "Hello 👋"
            assert m.username == "Liza"
            assert type(m.created_at) == datetime

            db.session.delete(m)
            db.session.commit()
