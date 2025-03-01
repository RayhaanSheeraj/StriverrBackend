import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app, db
from api.jwt_authorize import token_required
from model.mood import Mood

# Create a Blueprint for the mood API
mood_api = Blueprint('mood_api', __name__, url_prefix='/api')

# Create an Api object and associate it with the Blueprint
api = Api(mood_api)

class MoodAPI:
    class _Mood(Resource):
        """
        API operation for managing mood entries.
        """

        @token_required()
        def get(self):
            """
            Get the current user's mood entry.
            """
            current_user = g.current_user

            try:
                mood_entry = Mood.query.filter_by(user_id=current_user.id).first()
                if mood_entry:
                    return jsonify({'message': 'Mood retrieved successfully', 'mood': mood_entry.read()})
                else:
                    return {'message': 'No mood entry found for the user'}, 404
            except Exception as e:
                return {'message': 'Failed to retrieve mood', 'error': str(e)}, 500

        @token_required()
        def post(self):
            """
            Create a new mood entry for the authenticated user.
            """
            current_user = g.current_user
            body = request.get_json()

            # Validate mood
            mood = body.get('mood')
            if mood is None or not isinstance(mood, str) or mood.strip() == "":
                return {'message': 'Invalid mood provided'}, 400

            try:
                # Check if the user already has an existing mood entry
                existing_mood = Mood.query.filter_by(user_id=current_user.id).first()

                if existing_mood:
                    return {'message': 'Mood entry already exists. Use PUT to update.'}, 400
                else:
                    # Create a new mood entry
                    new_mood = Mood(mood=mood, user_id=current_user.id)
                    new_mood.create()
                    return jsonify({'message': 'Mood created successfully', 'mood': new_mood.read()})
            except Exception as e:
                return {'message': 'Failed to create mood', 'error': str(e)}, 500

        @token_required()
        def put(self):
            """
            Update an existing mood entry for the authenticated user.
            """
            current_user = g.current_user
            body = request.get_json()

            # Validate mood
            mood = body.get('mood')
            if mood is None or not isinstance(mood, str) or mood.strip() == "":
                return {'message': 'Invalid mood provided'}, 400

            try:
                # Check if the user already has an existing mood entry
                existing_mood = Mood.query.filter_by(user_id=current_user.id).first()

                if existing_mood:
                    # Update the existing mood entry
                    existing_mood.mood = mood
                    existing_mood.create()  # Save changes to the database
                    return jsonify({'message': 'Mood updated successfully', 'mood': existing_mood.read()})
                else:
                    return {'message': 'No existing mood entry found. Use POST to create one.'}, 404
            except Exception as e:
                return {'message': 'Failed to update mood', 'error': str(e)}, 500

        @token_required()
        def delete(self):
            current_user = g.current_user
            
            try:
                # Check if the user already has an existing mood entry
                existing_mood = Mood.query.filter_by(user_id=current_user.id).first()
                
                if existing_mood:
                    db.session.delete(existing_mood)
                    db.session.commit()
                    return jsonify({'message': 'Mood deleted successfully'})
                else:
                    return {'message': 'No mood entry found to delete'}, 404
                
            except Exception as e:
                return {'message': 'Failed to process mood', 'error': str(e)}, 500

    class _RestoreMood(Resource):
        """
        API operation for restoring (erasing) the mood entry.
        """
        @token_required()
        def post(self):
            current_user = g.current_user
            try:
                existing_mood = Mood.query.filter_by(user_id=current_user.id).first()
                
                if existing_mood:
                    existing_mood.mood = "neutral"
                    existing_mood.create()
                    return jsonify({'message': 'Mood erased successfully'})
                else:
                    return {'message': 'No mood entry found to erase'}, 404
            except Exception as e:
                return {'message': 'Failed to erase mood', 'error': str(e)}, 500

# Register the API resources with the Blueprint
api.add_resource(MoodAPI._Mood, '/mood', methods=['GET', 'POST', 'PUT', 'DELETE'])
api.add_resource(MoodAPI._RestoreMood, '/mood/restore', methods=['POST'])
