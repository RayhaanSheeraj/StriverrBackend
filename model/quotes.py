from __init__ import app, db
from sqlalchemy.exc import IntegrityError
import logging

class Quote(db.Model):
    __tablename__ = 'quote'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)

    def __init__(self, name, category):
        self.name = name
        self.category = category

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except IntegrityError as e:
            logging.error(f"Error creating quote: {e}")
            db.session.rollback()
            return False

    def update(self):
        try:
            db.session.commit()
            return True
        except IntegrityError as e:
            logging.error(f"Error updating quote: {e}")
            db.session.rollback()
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except IntegrityError as e:
            logging.error(f"Error deleting quote: {e}")
            db.session.rollback()
            return False

    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category
        }

    @staticmethod
    def restore(data):
        with app.app_context():
            db.session.query(Quote).delete()
            db.session.commit()

            restored_quotes = {}
            for quote_data in data:
                quote = Quote(
                    name=quote_data['name'],
                    category=quote_data['category']
                )
                quote.create()
                restored_quotes[quote_data['id']] = quote

            return restored_quotes

def init_quotes():
    with app.app_context():
        db.create_all()
        
        quotes = [
            {"name": "Quote 1", "category": "1"},
            {"name": "Quote 2", "category": "2"},
            {"name": "Quote 3", "category": "3"},
            {"name": "Quote 4", "category": "4"},
            {"name": "Quote 5", "category": "5"},
            {"name": "Quote 6", "category": "6"},
        ]

        for quote_data in quotes:
            quote = Quote(name=quote_data["name"], category=quote_data["category"])
            try:
                db.session.add(quote)
                db.session.commit()
            except IntegrityError as e:
                logging.error(f"Error creating quote: {e}")
                db.session.rollback()

        print("Database has been initialized and populated with initial quote data.")