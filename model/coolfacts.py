from sqlite3 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from __init__ import app, db
import logging
# coolfacts DATABASE
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
    def update(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except IntegrityError as e:
            logging.error(f"Error creating hobby: {e}")
            db.session.rollback()
            return False
    def delete(self):
        """
        Deletes the quiz from the database and commits the transaction.
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except IntegrityError as e:
            logging.error(f"Error deleting hobby: {e}")
            db.session.rollback()
            return False
   # @staticmethod
   # def restore(data):
   #     """
   #     Restore the database with the data provided.
   #     """
   #     for fact in data:
   #         _ = fact.pop('id', None)  # removes id
   #         event = CoolFacts.query.filter_by(coolfacts=fact['coolfacts'], age=fact['age']).first()  # retrieves the event by coolfacts
   #         if event:
   #             event.update(fact)
   #         else:
   #             event = CoolFacts(**fact)
   #             event.create()
    @staticmethod
    def restore(data):
        with app.app_context():
            db.session.query(CoolFacts).delete()
            db.session.commit()

            restored_facts = {}
            for fact_data in data:
                fact = CoolFacts(
                    coolfacts=fact_data['coolfacts'],
                    age=fact_data['age']
                )
                fact.create()
                restored_facts[fact_data['id']] = fact

            return restored_facts
def initCoolFacts():
    """
    Initializes the QuizCreation table and inserts test data for development purposes.
    """
    with app.app_context():
        db.create_all()  # Create the database and tables
        # Sample test data
        quizzes = [
            CoolFacts(coolfacts="Elon Musk saved Tesla from bankruptcy", age="37"),
            CoolFacts(coolfacts="Messi moved to Barcelona, Spain to play soccer and recieve proper medical treatment", age="13"),
            CoolFacts(coolfacts="Lebron James was scouted by the Cleveland Cavaliers and played his first NBA game there", age="18")
        ]
        for quiz in quizzes:
            try:
                quiz.create()
                print(f"Created quiz: {repr(quiz)}")
            except IntegrityError as e:
                db.session.rollback()
                print(f"Record already exists or error occurred: {str(e)}")