
from __init__ import db, app

class bucket_list(db.Model):
    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), nullable=False, default="Pending")
    user = db.Column(db.Integer, nullable=False)

    def __init__(self, title, description, status, user):
        self.title = title
        self.description = description
        self.status = status
        self.user = user

    def __repr__(self):
        return f"bucket_list(id={self.id}, title={self.title}, description={self.description}, status={self.status}, user={self.user})"

    def create(self):
        """
        Add the bucket list item to the database and commit the transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return self

    def read(self):
        """
        Retrieve the bucket list item's data as a dictionary.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "user": self.user
        }

    def update(self, title=None, description=None, status=None):
        """
        Update the bucket list item with new data.
        """
        if title:
            self.title = title
        if description:
            self.description = description
        if status:
            self.status = status
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """
        Remove the bucket list item from the database and commit the transaction.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def restore(data):
        """
        Restore bucket lists from a list of dictionaries.
        """
        restored_bucketlists = {}
        for bucketlist_data in data:
            try:
                _ = bucketlist_data.pop('id', None)  # Remove 'id' from bucketlist_data
                title = bucketlist_data.get("title")
                user = bucketlist_data.get("user")
                if not title or not user:
                    raise ValueError("Missing required fields: title or user.")
                # Generate a unique key using the bucketlist title and user
                bucketlist_key = f"{title} - {user}"
                # Check if a bucketlist with the same title and user exists
                bucketlist = bucket_list.query.filter_by(title=title, user=user).first()
                if bucketlist:
                    # Update the existing bucketlist's data
                    bucketlist.update(**bucketlist_data)
                else:
                    # Create a new bucketlist if not found
                    bucketlist = bucket_list(**bucketlist_data)
                    bucketlist.create()
                # Add the bucketlist to the restored_bucketlists dictionary
                restored_bucketlists[bucketlist_key] = bucketlist
            except Exception as e:
                print(f"Error processing bucketlist data: {bucketlist_data} - {e}")
                continue

        return restored_bucketlists

def initBucketlists():
    """
    Initialize the Bucketlist table with default data.
    """
    with app.app_context():
        db.create_all()
        
        bucketlists = [
            bucket_list(title='Skydiving', description='Experience freefall from an airplane.', status='Pending', user=1),
            bucket_list(title='Visit the Eiffel Tower', description='Travel to Paris and see the Eiffel Tower.', status='Pending', user=2),
            bucket_list(title='Learn a New Language', description='Master Spanish within a year.', status='In Progress', user=3),
            bucket_list(title='Run a Marathon', description='Complete a 26.2-mile marathon.', status='Pending', user=4),
            bucket_list(title='Publish a Book', description='Write and publish my first novel.', status='Completed', user=5),
        ]
        for bucketlist in bucketlists:
            try:
                bucketlist.create()
                print(f"Added Bucketlist: {bucketlist.title}")
            except Exception as e:
                db.session.remove()
                print(f"Error adding {bucketlist.title}: {e}")