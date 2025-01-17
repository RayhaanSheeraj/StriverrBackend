from datetime import datetime
from __init__ import db

class Quote(db.Model):
    """
    Quote Model

    Represents a single quote retrieved from the external API.

    Attributes:
        id (db.Column): Primary key, a unique identifier for the quote.
        text (db.Column): The text of the quote.
        author (db.Column): The author of the quote.
        category (db.Column): The category of the quote, if provided.
        fetched_at (db.Column): Timestamp of when the quote was fetched.
    """
    __tablename__ = 'quotes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    fetched_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, text, author, category, fetched_at):
        self.text = text
        self.author = author
        self.category = category
        self.fetched_at = fetched_at


def create(text, author, category):
    """
    Save a new quote to the database.

    Args:
        text (str): The text of the quote.
        author (str): The author of the quote.
        category (str): The category of the quote.

    Returns:
        Quote: The saved quote instance.
    """
    quote = Quote(
        text=text,
        author=author,
        category=category,
        fetched_at=datetime.utcnow()
    )
    try:
        db.session.add(quote)
        db.session.commit()
        return quote
    except Exception as e:
        db.session.rollback()
        raise e
