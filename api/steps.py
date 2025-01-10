import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.user import User

steps_api = Blueprint('steps_api', __name__, url_prefix='/api')

# Create an Api object and associate it with the Blueprint
api = Api(steps_api)

class StepsAPI:
    class steps(Resource):
        @token_required()
        def post(self):
            """
            Update the user's steps.
            """
            current_user = g.current_user
            body = request.get_json()

            # Validate steps
            steps = body.get('steps')
            if steps is None or not isinstance(steps, int):
                return {'message': 'Invalid steps provided. Steps must be an integer.'}, 400

            try:
                # Update steps directly
                current_user.steps = steps  # Assuming steps is a column in the User model
                current_user.update({'steps': steps})  # Update the database
                return jsonify({'message': 'Steps updated successfully', 'steps': current_user.steps})
            except Exception as e:
                return {'message': 'Failed to update steps', 'error': str(e)}, 500

        @token_required()
        def get(self):
            """
            Get the current user's steps.
            """
            current_user = g.current_user

            try:
                # Return the current user's steps
                return jsonify({'steps': current_user.steps})
            except Exception as e:
                return {'message': 'Failed to retrieve steps', 'error': str(e)}, 500

api.add_resource(StepsAPI.steps, '/steps')
