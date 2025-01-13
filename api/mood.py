import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.user import User

# Create a Blueprint for the user API
mood_api = Blueprint('mood_api', __name__, url_prefix='/api')

# Create an Api object and associate it with the Blueprint
# API docs: https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(mood_api)

class MoodAPI:
    class _Mood(Resource):
        """
        User-specific API operation for updating mood.
        """

        @token_required()
        def post(self):
            """
            Update the user's mood.
            """
            current_user = g.current_user
            body = request.get_json()

            # Validate mood
            mood = body.get('mood')
            if mood is None or not isinstance(mood, str) or mood.strip() == "":
                return {'message': 'Invalid mood provided'}, 400

            # Update mood
            try:
                current_user.mood = mood  # Assuming `mood` is a column in the User model
                current_user.update({'mood': mood})  # Update the database
                return jsonify({'message': 'Mood updated successfully', 'mood': current_user.mood})
            except Exception as e:
                return {'message': 'Failed to update mood', 'error': str(e)}, 500


# Register the API resources with the Blueprint
api.add_resource(MoodAPI._Mood, '/mood')

