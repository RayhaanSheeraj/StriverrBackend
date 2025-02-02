from sqlite3 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from __init__ import app, db

class CoolFacts (db.Model):
    """
    CoolFacts Model
    """
    __tablename__ = 'coolFacts'
    id = db.Column(db.Integer, primary_key=True)
    coolfacts = db.Column(db.String(255), nullable=False)
    age = db.Column(db.String(255), nullable=False)
    def __init__(self, coolfacts, age, ):
        """
        Constructor for Binary.
        """
        self.coolfacts = coolfacts
        self.age = age
    def __repr__(self):
        """
        Represents the QuizCreation object as a string for debugging.
        """
        return f"<Coolfacts(id={self.id}, coolfacts='{self.coolfacts}', age='{self.age})>"
    def create(self):
        """
        Adds the quiz to the database and commits the transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    def read(self):
        """
        Returns the quiz details as a dictionary.
        """
        return {
            "id": self.id,
            "coolfacts": self.coolfacts,
            "age": self.age,
        }
    def update(self, data):
        """
        Updates the quiz with new data and commits the changes.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    def delete(self):
        """
        Deletes the quiz from the database and commits the transaction.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    @staticmethod
    def restore(data):
        existing_sections = {section.id: section for section in CoolFacts.query.all()}
        for section_data in data:
            age = section_data.pop('age', None)  # Remove 'id' from section_data
            coolfacts = section_data.get("coolfacts", None)
            section = existing_sections.pop(coolfacts, None)
            if section:
                section.update(section_data)
            else:
                section = CoolFacts(**section_data)
                section.create()
        # Remove any extra data that is not in the backup
        for section in existing_sections.values():
            db.session.delete(section)
        db.session.commit()
        return existing_sections
def initCoolFacts():
    """
    Initializes the QuizCreation table and inserts test data for development purposes.
    """
    with app.app_context():
        db.create_all()  # Create the database and tables
        # Sample test data
        quizzes = [
            CoolFacts(coolfacts="I was born in 2009", age="16"),
            CoolFacts(coolfacts="Nikith was born in 2008", age="24"),
            CoolFacts(coolfacts="I am not entirely sure what to put here", age="32")
        ]
        for quiz in quizzes:
            try:
                quiz.create()
                print(f"Created quiz: {repr(quiz)}")
            except IntegrityError as e:
                db.session.rollback()
                print(f"Record already exists or error occurred: {str(e)}")


