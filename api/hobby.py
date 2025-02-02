import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource
from datetime import datetime
from __init__ import app, db
from api.jwt_authorize import token_required
from model.hobbies import Hobby

hobby_api = Blueprint('hobby_api', __name__, url_prefix='/api')
api = Api(hobby_api)

class HobbyResource(Resource):
    def get(self):
        category = request.args.get('category', 'general')
        hobbies = Hobby.query.filter_by(category=category).all()
        if hobbies:
            return jsonify({"category": category, "hobbies": [hobby.name for hobby in hobbies]})
        else:
            return jsonify({"message": "Category not found"}), 404
    
    def post(self):
        data = request.get_json()
        if not data or not data.get('name') or not data.get('category'):
            return jsonify({"message": "Hobby name and category are required"}), 400
        
        hobby = Hobby(name=data['name'], category=data['category'])
        if hobby.create():
            return jsonify({"message": "Hobby created", "hobby": hobby.name, "category": hobby.category})
        else:
            return jsonify({"message": "Error creating hobby"}), 500

    def put(self):
        data = request.get_json()
        if not data or not data.get('name') or not data.get('category') or not data.get('old_name'):
            return jsonify({"message": "Hobby name, old name, and category are required to update"}), 400
        
        hobby = Hobby.query.filter_by(name=data['old_name'], category=data['category']).first()
        if not hobby:
            return jsonify({"message": "Hobby not found"}), 404
        
        hobby.name = data['name']
        if hobby.update():
            return jsonify({"message": "Hobby updated", "old_name": data['old_name'], "new_name": hobby.name})
        else:
            return jsonify({"message": "Error updating hobby"}), 500

    def delete(self):
        data = request.get_json()
        if not data or not data.get('name') or not data.get('category'):
            return jsonify({"message": "Hobby name and category are required to delete"}), 400
        
        hobby = Hobby.query.filter_by(name=data['name'], category=data['category']).first()
        if not hobby:
            return jsonify({"message": "Hobby not found"}), 404
        
        if hobby.delete():
            return jsonify({"message": "Hobby deleted", "name": hobby.name})
        else:
            return jsonify({"message": "Error deleting hobby"}), 500

api.add_resource(HobbyResource, '/hobby')