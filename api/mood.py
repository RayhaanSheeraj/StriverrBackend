import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
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
        def post(self):
            """
            Add or update a mood entry for the authenticated user.
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
                    # Create a new mood entry
                    new_mood = Mood(mood=mood, user_id=current_user.id)
                    new_mood.create()
                    return jsonify({'message': 'Mood added successfully', 'mood': new_mood.read()})
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
                    existing_mood.mood = None  # Erase mood column
                    existing_mood.create()
                    return jsonify({'message': 'Mood erased successfully'})
                return jsonify({'message': 'No mood entry found'}), 404
            except Exception as e:
                return {'message': 'Failed to erase mood', 'error': str(e)}, 500

# Register the API resources with the Blueprint
api.add_resource(MoodAPI._Mood, '/mood')
api.add_resource(MoodAPI._RestoreMood, '/mood/restore')