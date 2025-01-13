import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.user import User

hobby_api = Blueprint('hobby_api', __name__, url_prefix='/api')
api = Api(hobby_api)

hobby_data = {
    "general": ["Reading", "Writing", "Cooking", "Gardening"],
    "sports": ["Football", "Basketball", "Tennis", "Swimming"],
    "arts": ["Painting", "Drawing", "Photography", "Pottery"]
}

class Hobby(Resource):
    def get(self):
        category = request.args.get('category', 'general')
        if category in hobby_data:
            return jsonify({"category": category, "hobbies": hobby_data[category]})
        else:
            return jsonify({"message": "Category not found"}), 404
    
    def post(self):
        data = request.get_json()
        if not data or not data.get('name') or not data.get('category'):
            return jsonify({"message": "Hobby name and category are required"}), 400
        
        category = data['category']
        hobby_name = data['name']
        
        # Add hobby to the respective category
        if category in hobby_data:
            hobby_data[category].append(hobby_name)
        else:
            hobby_data[category] = [hobby_name]
        
        return jsonify({"message": "Hobby created", "hobby": hobby_name, "category": category})

    # Update an existing hobby
    def put(self):
        data = request.get_json()
        if not data or not data.get('name') or not data.get('category'):
            return jsonify({"message": "Hobby name and category are required to update"}), 400
        
        category = data['category']
        old_hobby_name = data['old_name']
        new_hobby_name = data['name']

        # Check if the category exists
        if category not in hobby_data:
            return jsonify({"message": "Category not found"}), 404
        
        # Check if the old hobby exists
        if old_hobby_name not in hobby_data[category]:
            return jsonify({"message": "Old hobby not found in this category"}), 404
        
        # Update hobby in the category
        index = hobby_data[category].index(old_hobby_name)
        hobby_data[category][index] = new_hobby_name
        
        return jsonify({"message": "Hobby updated", "old_name": old_hobby_name, "new_name": new_hobby_name})

    # Delete a hobby
    def delete(self):
        data = request.get_json()
        if not data or not data.get('name') or not data.get('category'):
            return jsonify({"message": "Hobby name and category are required to delete"}), 400
        
        category = data['category']
        hobby_name = data['name']
        
        # Check if the category exists
        if category not in hobby_data:
            return jsonify({"message": "Category not found"}), 404
        
        # Check if the hobby exists in the category
        if hobby_name not in hobby_data[category]:
            return jsonify({"message": "Hobby not found in this category"}), 404
        
        # Remove hobby from the category
        hobby_data[category].remove(hobby_name)
        
        return jsonify({"message": "Hobby deleted", "name": hobby_name})

api.add_resource(Hobby, '/hobby')