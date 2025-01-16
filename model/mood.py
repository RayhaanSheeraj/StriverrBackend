from sqlite3 import IntegrityError
from __init__ import app, db
from model.user import User

class Mood(db.Model):
    __tablename__ = 'mood'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mood = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, mood, user_id):
        self.mood = mood
        self.user_id = user_id

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        return {
            'id': self.id,
            'mood': self.mood,
            'user_id': self.user_id,
        }
