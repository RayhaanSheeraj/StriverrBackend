from sqlite3 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError # Fix this part of the Goals API model code.
from __init__ import app, db
import logging

class StriverGoals(db.Model):
    """
    StriverGoals Model
    Represents a getgoals -> goaloutput conversion record.
    """
    __tablename__ = 'striverGoals'
    id = db.Column(db.Integer, primary_key=True)
    getgoals = db.Column(db.String(255), nullable=False)
    goaloutput = db.Column(db.String(255), nullable=False)
    progress = db.Column(db.String(255), nullable=True)
    
    def __init__(self, getgoals, goaloutput, progress=None):
        """
        Constructor for StriverGoals.
        """
        self.getgoals= getgoals
        self.goaloutput = goaloutput
        self.progress = progress
    
    def __repr__(self):
        """
        Represents the StriverGoals object as a string for debugging.
        """
        return f"<StriverGoals(id={self.id}, getgoals='{self.getgoals}', goaloutput='{self.goaloutput}', progress='{self.progress}')>"
    
    def create(self):
        """
        Adds the record to the database and commits the transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    def read(self):
        """
        Returns the binary-to-decimal conversion details as a dictionary.
        """
        return {
            "id": self.id,
            "getgoals": self.getgoals,
            "goaloutput": self.goaloutput,
            "progress": self.progress,
        }
    
    def update(self, data):
        """
        Updates the record with new data and commits the changes.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"Error updating record: {e}")
            raise e
    
    def delete(self):
        """
        Deletes the record from the database and commits the transaction.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def restore(data):
        existing_sections = {section.id: section for section in StriverGoals.query.all()}
        for section_data in data:
            _ = section_data.pop('id', None)  # Remove 'id' from section_data
            getgoals = section_data.get("getgoals", None)
            section = existing_sections.pop(getgoals, None)
            if section:
                section.update(section_data)
            else:
                section = StriverGoals(**section_data)
                section.create()
        # Remove any extra data that is not in the backup
        for section in existing_sections.values():
            db.session.delete(section)
        db.session.commit()
        return existing_sections

def initGoals():
    """
    Initializes the StriverGoals table and inserts test data for development purposes.
    """
    with app.app_context():
        db.create_all()  # Create the database and tables
        # Sample test data
        quizzes = [
            StriverGoals(getgoals="Retrieve1", goaloutput="Read 3 books in 1 month", progress="Not Started"),
            StriverGoals(getgoals="Retrieve2", goaloutput="Go outside for 45 minutes every day", progress="Not Started"),
            StriverGoals(getgoals="Retrieve3", goaloutput="Exercise for 30 minutes daily", progress="Not Started"),
            StriverGoals(getgoals="Retrieve4", goaloutput="Meditate for 10 minutes each morning", progress="Not Started"),
            StriverGoals(getgoals="Retrieve5", goaloutput="Practice a new language for 20 minutes daily", progress="Not Started"),
            StriverGoals(getgoals="Retrieve6", goaloutput="Write in a journal for 15 minutes every day", progress="Not Started"),
            StriverGoals(getgoals="Retrieve7", goaloutput="Drink 8 glasses of water every day", progress="Not Started"),
            StriverGoals(getgoals="Retrieve8", goaloutput="Learn one new recipe every week", progress="Not Started"),
            StriverGoals(getgoals="Retrieve9", goaloutput="Listen to an educational podcast for 30 minutes daily", progress="Not Started"),
            StriverGoals(getgoals="Retrieve10", goaloutput="Spend 30 minutes on a creative hobby each day", progress="Not Started"),
            StriverGoals(getgoals="Retrieve11", goaloutput="Take a 20-minute walk during your lunch break every day", progress="Not Started"),
        ]
        for quiz in quizzes:
            try:
                quiz.create()
                print(f"Created quiz: {quiz}")
            except IntegrityError:
                db.session.rollback()
                print(f"Record already exists or error occurred: {quiz}")