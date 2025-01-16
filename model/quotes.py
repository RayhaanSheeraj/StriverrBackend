from flask import Blueprint, request, jsonify, g
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
    There are three operations that correspond to HTTP methods:
    - GET (Single): Retrieve a single quote by category or default.
    - GET (Bulk): Retrieve multiple quotes in bulk.
    - POST (Filter): Filter quotes based on specific criteria.
    """

    class _CRUD(Resource):
        @token_required()
        def get(self):
            """
            Retrieve a single quote by category or default.
            """
            category = request.args.get('category', None)
            headers = {'X-Api-Key': API_KEY}
            url = f"{API_URL}?category={category}" if category else API_URL

            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    return jsonify(response.json())
                return {
                    "error": f"API request failed with status {response.status_code}",
                    "details": response.text
                }, response.status_code
            except Exception as e:
                return {"error": "An error occurred", "details": str(e)}, 500

        def post(self):
            """
            Retrieve multiple quotes in bulk or filter quotes.
            """
            data = request.get_json()
            category = data.get('category', None)
            count = int(data.get('count', 5))
            headers = {'X-Api-Key': API_KEY}
            quotes = []

            try:
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
                return {"error": "An error occurred", "details": str(e)}, 500

        @token_required()
        def delete(self):
            """
            Clear the user's quote history or simulate deletion.
            """
            return {"message": "Quote history cleared or simulated deletion successful."}, 200

api.add_resource(QuotesAPI._CRUD, '/quotes')

if __name__ == '__main__':
    from __init__ import app
    app.register_blueprint(quotes_api)
    app.run(debug=True)
