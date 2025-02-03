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

    def clear(self):
        """
        Clears the mood entry by deleting the row from the database.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


def get(self):
    """
    Retrieve all mood entries by user ID.
    """
    # Extract user_id from query parameters
    user_id = request.args.get('user_id')
    if not user_id:
        return {'message': 'User ID is required'}, 400
    # Query all mood entries for the given user_id
    moods = Mood.query.filter_by(user_id=user_id).all()
    if not moods:
        return {'message': 'No mood entries found for this user'}, 404
    # Return the list of mood entries in JSON format
    return jsonify([mood.read() for mood in moods])
