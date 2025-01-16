from __init__ import app, db
from sqlalchemy.exc import IntegrityError
import logging
import json

class Hobby(db.Model):
    
    __tablename__ = 'hobby'
    
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
def initHobbies():
    """
    The initHobbies function creates the Hobby table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        Hobby objects with tester data.
    
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """
with app.app_context():
    """Create database and tables"""
    db.create_all()
        
    """Tester data for Hobby table"""
    hobbies = [
        {"name": "Reading", "category": "general"},
        {"name": "Writing", "category": "general"},
        {"name": "Football", "category": "sports"},
        {"name": "Basketball", "category": "sports"},
        {"name": "Painting", "category": "arts"},
        {"name": "Drawing", "category": "arts"},
        ]

    for hobby_data in hobbies:
        hobby = Hobby(name=hobby_data["name"], category=hobby_data["category"])
        try:
            db.session.add(hobby)
            db.session.commit()
        except IntegrityError as e:
            logging.error(f"Error creating hobby: {e}")
            db.session.rollback()