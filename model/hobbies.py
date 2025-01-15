from __init__ import app, db
from sqlalchemy.exc import IntegrityError
import logging

class Hobby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)

    def create(self):
        """
        Create a new hobby in the database.
        
        Returns:
            bool: True if the hobby was successfully created, False otherwise.
        """
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except IntegrityError as e:
            logging.error(f"Error creating hobby: {e}")
            return False

    def update(self):
        """
        Update an existing hobby in the database.
        
        Returns:
            bool: True if the hobby was successfully updated, False otherwise.
        """
        try:
            db.session.commit()
            return True
        except IntegrityError as e:
            logging.error(f"Error updating hobby: {e}")
            return False

    def delete(self):
        """
        Delete an existing hobby from the database.
        
        Returns:
            bool: True if the hobby was successfully deleted, False otherwise.
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except IntegrityError as e:
            logging.error(f"Error deleting hobby: {e}")
            return False