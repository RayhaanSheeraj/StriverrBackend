from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from api.jwt_authorize import token_required  # Assuming this is your JWT middleware
import requests
from datetime import datetime
from __init__ import db
from model.quotes import create  # type: ignore # Import the create function from the model

# Define the Blueprint for Quotes API
quotes_api = Blueprint('quotes_api', __name__, url_prefix='/api')
api = Api(quotes_api)

# API configuration
API_URL = 'https://api.api-ninjas.com/v1/quotes'
API_KEY = 'your-api-key'  # Replace with your actual API key


class QuotesAPI:
    """
    Define the API CRUD endpoints for the Quotes service.
    """

    class _Single(Resource):
        @token_required()
        def get(self):
            """
            Retrieve a single quote by category or default and save it to the database.
            """
            category = request.args.get('category', None)
            headers = {'X-Api-Key': API_KEY}
            url = f"{API_URL}?category={category}" if category else API_URL

            try:
                # Fetch quote from external API
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()[0]  # Assuming the API returns a list of quotes
                    text = data['quote']
                    author = data['author']

                    # Save the quote to the database
                    quote = create(text=text, author=author, category=category)

                    # Return the saved quote
                    return jsonify({
                        "message": "Quote fetched and saved successfully",
                        "quote": {
                            "id": quote.id,
                            "text": quote.text,
                            "author": quote.author,
                            "category": quote.category,
                            "fetched_at": quote.fetched_at.isoformat()
                        }
                    })
                else:
                    return {
                        "error": f"API request failed with status {response.status_code}",
                        "details": response.text
                    }, response.status_code
            except Exception as e:
                return {"error": "An error occurred", "details": str(e)}, 500

    class _Bulk(Resource):
        def get(self):
            """
            Retrieve multiple quotes in bulk and save them to the database.
            """
            category = request.args.get('category', None)
            count = int(request.args.get('count', 5))  # Default to 5 quotes
            headers = {'X-Api-Key': API_KEY}
            saved_quotes = []

            try:
                for _ in range(count):
                    url = f"{API_URL}?category={category}" if category else API_URL
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        data = response.json()[0]  # Assuming the API returns a list of quotes
                        text = data['quote']
                        author = data['author']

                        # Save each quote to the database
                        quote = create(text=text, author=author, category=category)
                        saved_quotes.append({
                            "id": quote.id,
                            "text": quote.text,
                            "author": quote.author,
                            "category": quote.category,
                            "fetched_at": quote.fetched_at.isoformat()
                        })
                    else:
                        return {
                            "error": f"API request failed with status {response.status_code}",
                            "details": response.text
                        }, response.status_code

                return jsonify({
                    "message": f"{len(saved_quotes)} quotes fetched and saved successfully",
                    "quotes": saved_quotes
                })
            except Exception as e:
                return {"error": "An error occurred", "details": str(e)}, 500


# Register the endpoints
api.add_resource(QuotesAPI._Single, '/quote')  # Single quote endpoint
api.add_resource(QuotesAPI._Bulk, '/quotes')  # Bulk quotes endpoint
