from datetime import datetime
from app import app
from models import db, Message

class TestApp:

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

    def test_returns_list_of_json_objects_for_all_messages_in_database(self):
        with app.app_context():
            response = app.test_client().get('/messages')
            records = Message.query.all()
            for message in response.json:
                assert message['id'] in [r.id for r in records]
                assert message['body'] in [r.body for r in records]

    def test_creates_new_message_in_the_database(self):
        with app.app_context():
            app.test_client().post(
                '/messages',
                json={"body":"Hello 👋","username":"Liza"}
            )
            h = Message.query.filter_by(body="Hello 👋").first()
            assert h

            db.session.delete(h)
            db.session.commit()

    def test_returns_data_for_newly_created_message_as_json(self):
        with app.app_context():
            response = app.test_client().post(
                '/messages',
                json={"body":"Hello 👋","username":"Liza"}
            )
            assert response.content_type == 'application/json'
            assert response.json["body"] == "Hello 👋"
            assert response.json["username"] == "Liza"

            h = Message.query.filter_by(body="Hello 👋").first()
            db.session.delete(h)
            db.session.commit()

    def test_updates_body_of_message_in_database(self):
        with app.app_context():
            m = Message(body="Temp Message", username="Liza")
            db.session.add(m)
            db.session.commit()

            id = m.id
            app.test_client().patch(f'/messages/{id}', json={"body":"Updated Message"})

            g = Message.query.filter_by(body="Updated Message").first()
            assert g

            db.session.delete(g)
            db.session.commit()

    def test_returns_data_for_updated_message_as_json(self):
        with app.app_context():
            m = Message(body="Temp Message", username="Liza")
            db.session.add(m)
            db.session.commit()

            id = m.id
            response = app.test_client().patch(f'/messages/{id}', json={"body":"Updated Message"})
            assert response.content_type == 'application/json'
            assert response.json["body"] == "Updated Message"

            db.session.delete(m)
            db.session.commit()

    def test_deletes_message_from_database(self):
        with app.app_context():
            m = Message(body="To Delete", username="Liza")
            db.session.add(m)
            db.session.commit()

            app.test_client().delete(f'/messages/{m.id}')
            h = Message.query.filter_by(body="To Delete").first()
            assert not h
