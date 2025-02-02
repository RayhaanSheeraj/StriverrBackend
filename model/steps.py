# steps.py
from sqlalchemy import Integer
from __init__ import app, db

class Steps(db.Model):
    """
    Steps Model
    
    The Steps class represents the walking steps data for a user.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the record.
        user (db.Column): A string representing the username associated with the steps.
        steps (db.Column): An integer representing the number of steps taken by the user.
    """
    __tablename__ = 'steps'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(255), nullable=False)
    steps = db.Column(db.Integer, nullable=False)

    def __init__(self, user, steps):
        """
        Constructor, initializes a Steps object.
        
        Args:
            user (str): The username associated with the steps.
            steps (int): The number of steps taken by the user.
        """
        self.user = user
        self.steps = steps

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr() built-in function.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"Steps(id={self.id}, user={self.user}, steps={self.steps})"
    
    def create(self):
        """
        The create method adds the object to the database and commits the transaction.
        
        Uses:
            The db ORM methods to add and commit the transaction.
        
        Raises:
            Exception: An error occurred when adding the object to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    def delete(self):
        """
        Deletes the chat message from the database.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    def read(self):
        """
        The read method retrieves the object data from the object's attributes and returns it as a dictionary.
        
        Returns:
            dict: A dictionary containing the steps data.
        """
        return {
            'id': self.id,
            'user': self.user,
            'steps': self.steps
        }
    def update(self):
        """
        Update an existing hobby in the database.
        
        Returns:
            bool: True if the hobby was successfully updated, False otherwise.
        """
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
    @staticmethod
    def restore(data):
        """
        Restore steps from a list of dictionaries, replacing existing entries.

        Args:
            data (list): List of dictionaries containing steps data.

        Returns:
            dict: Dictionary of restored Steps objects.
        """
        with app.app_context():
            # Clear the existing table
            db.session.query(Steps).delete()
            db.session.commit()

            restored_steps = {}
            for steps_data in data:
                steps = Steps(
                    user=steps_data['user'],
                    steps=steps_data['steps']
                )
                steps.create()
                restored_steps[steps_data['id']] = steps

            return restored_steps
def initSteps():
    """
    The initSteps function creates the Steps table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        Steps objects with tester data.
    
    Raises:
        Exception: An error occurred when adding the tester data to the table.
    """
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        tester_data = [
            Steps(user='user1', steps=5000),
            Steps(user='user2', steps=7500),
            Steps(user='user3', steps=12000)
        ]
        
        for data in tester_data:
            try:
                db.session.add(data)
                db.session.commit()
                print(f"Record created: {repr(data)}")
            except Exception as e:
                db.session.rollback()
                print(f"Error creating record for user {data.user}: {e}")