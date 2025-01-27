from flask import Blueprint, request, jsonify, current_app, g
from flask_restful import Api, Resource
from api.jwt_authorize import token_required  # Assuming this is your JWT middleware
import requests

# Define the Blueprint for Quotes API
quotes_api = Blueprint('quotes_api', __name__, url_prefix='/api')
api = Api(quotes_api)

# API configuration
API_URL = 'https://api.api-ninjas.com/v1/quotes'
API_KEY = 'dsH4Bmo4W7wv5SVKvjbSRQ==mRJPmT9DcU5oqtI7'


class QuotesAPI:
    """
    Define the API CRUD endpoints for the Quotes service.
    """

    class _Single(Resource):
        @token_required()
        def get(self):
            """
            Retrieve a single quote by category or default.
            """
            # Extract query parameters from the request
            category = request.args.get('category', None)
            headers = {'X-Api-Key': API_KEY}
            
            # Construct the URL for the external API
            url = f"{API_URL}?category={category}" if category else API_URL

            try:
                # Fetch data from the external API
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    # Return the quote in JSON format
                    return jsonify(response.json())
                else:
                    # Return an error if the external API fails
                    return {
                        "error": f"API request failed with status {response.status_code}",
                        "details": response.text
                    }, response.status_code
            except Exception as e:
                # Handle any unexpected errors
                return {"error": "An error occurred", "details": str(e)}, 500

    class _Bulk(Resource):
        def get(self):
            """
            Retrieve multiple quotes in bulk.
            """
            # Extract query parameters for bulk filtering
            category = request.args.get('category', None)
            count = int(request.args.get('count', 5))  # Default to 5 quotes
            headers = {'X-Api-Key': API_KEY}
            quotes = []

            try:
                # Fetch multiple quotes by sending multiple requests
                for _ in range(count):
                    url = f"{API_URL}?category={category}" if category else API_URL
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        quotes.extend(response.json())
                    else:
                        return {
                            "error": f"API request failed with status {response.status_code}",
                            "details": response.text
                        }, response.status_code

                return jsonify(quotes)
            except Exception as e:
                # Handle unexpected errors
                return {"error": "An error occurred", "details": str(e)}, 500

    class _Filter(Resource):
        @token_required()
        def post(self):
            """
            Filter quotes based on specific criteria.
            """
            data = request.get_json()
            if not data or 'category' not in data:
                return {'message': 'Category is required'}, 400

            category = data['category']
            headers = {'X-Api-Key': API_KEY}
            url = f"{API_URL}?category={category}"

            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    return jsonify(response.json())
                else:
                    return {
                        "error": f"API request failed with status {response.status_code}",
                        "details": response.text
                    }, response.status_code
            except Exception as e:
                return {"error": "An error occurred", "details": str(e)}, 500

    """
    Map the _Single, _Bulk, and _Filter classes to their respective endpoints.
    """
    api.add_resource(_Single, '/quote')
    api.add_resource(_Bulk, '/quotes')
    api.add_resource(_Filter, '/quotes/filter')
