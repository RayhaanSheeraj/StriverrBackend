import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource
from datetime import datetime
from __init__ import app, db
from api.jwt_authorize import token_required
from model.quotes import Quote

quotes_api = Blueprint('quote_api', __name__, url_prefix='/api')
api = Api(quotes_api)

class quoteResource:
    class _CRUD(Resource):
        @token_required
        def get(self):
            try:
                category = request.args.get('category', 'general')
                quotes = Quote.query.filter_by(category=category).all()
                if quotes:
                    return jsonify({"category": category, "quotes": [quote.name for quote in quotes]})
                else:
                    return jsonify({"message": "Category not found"}), 404
            except Exception as e:
                return jsonify({"message": "Internal server error", "error": str(e)}), 500
        @token_required
        def post(self):
            data = request.get_json()
            if not data or not data.get('name') or not data.get('category'):
                return jsonify({"message": "quote name and category are required"}), 400
        
            quote = quote(name=data['name'], category=data['category'])
            if quote.create():
                return jsonify({"message": "quote created", "quote": quote.name, "category": quote.category})
            else:
                return jsonify({"message": "Error creating quote"}), 500
        @token_required
        def put(self):
            data = request.get_json()
            if not data or not data.get('name') or not data.get('category') or not data.get('old_name'):
                return jsonify({"message": "quote name, old name, and category are required to update"}), 400
        
            quote = quote.query.filter_by(name=data['old_name'], category=data['category']).first()
            if not quote:
                return jsonify({"message": "quote not found"}), 404
        
            quote.name = data['name']
            if quote.update():
                return jsonify({"message": "quote updated", "old_name": data['old_name'], "new_name": quote.name})
            else:
                return jsonify({"message": "Error updating quote"}), 500
        @token_required
        def delete(self):
            data = request.get_json()
            if not data or not data.get('name') or not data.get('category'):
                return jsonify({"message": "quote name and category are required to delete"}), 400
        
            quote = quote.query.filter_by(name=data['name'], category=data['category']).first()
            if not quote:
                return jsonify({"message": "quote not found"}), 404
        
            if quote.delete():
                return jsonify({"message": "quote deleted", "name": quote.name})
            else:
                return jsonify({"message": "Error deleting quote"}), 500

    api.add_resource(_CRUD, '/quote')