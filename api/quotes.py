import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource
from datetime import datetime
from __init__ import app, db
from api.jwt_authorize import token_required
from model.quotes import Quote

quotes_api = Blueprint('quote_api', __name__, url_prefix='/api')
api = Api(quotes_api)

class QuotesAPI():


    class _CRUD(Resource):

        @token_required()
        def get(self):
            try:
                # Query all entries in the BinaryHistory table
                entries = Quote.query.all()
                # Convert the entries to a list of dictionaries
                results = [entry.read() for entry in entries]
                # Return the list of results in JSON format
                return jsonify(results)
            except Exception as e:
                # Return an error message in case of failure
                return jsonify({"error": str(e)}), 500
            
        @token_required()
        def post(self):
            data = request.get_json()
            if not data or not data.get('name') or not data.get('category'):
                return jsonify({"message": "Quote name and category are required"}), 400
            
            quote = Quote(name=data['name'], category=data['category'])
            if quote.create():
                return jsonify({"message": "Quote created", "quote": quote.name, "category": quote.category})
            else:
                return jsonify({"message": "Error creating quote"}), 500
        @token_required()

        def put(self):
            data = request.get_json()
            if not data or not data.get('name') or not data.get('category') or not data.get('old_name'):
                return jsonify({"message": "Quote name, old name, and category are required to update"}), 400
            
            quote = Quote.query.filter_by(name=data['old_name'], category=data['category']).first()
            if not quote:
                return jsonify({"message": "Quote not found"}), 404
            
            quote.name = data['name']
            if quote.update():
                return jsonify({"message": "Quote updated", "old_name": data['old_name'], "new_name": quote.name})
            else:
                return jsonify({"message": "Error updating quote"}), 500
        @token_required()

        def delete(self):
            data = request.get_json()
            if not data or not data.get('name') or not data.get('category'):
                return jsonify({"message": "Quote name and category are required to delete"}), 400
            
            quote = Quote.query.filter_by(name=data['name'], category=data['category']).first()
            if not quote:
                return jsonify({"message": "Quote not found"}), 404
            
            if quote.delete():
                return jsonify({"message": "Quote deleted", "name": quote.name})
            else:
                return jsonify({"message": "Error deleting quote"}), 500

    api.add_resource(_CRUD, '/quotes')
if __name__ == '__main__':
    app.run(debug=True)