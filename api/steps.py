import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.steps import Steps

# Create a Blueprint for the steps API
steps_api = Blueprint('steps_api', __name__, url_prefix='/api')

# Create an Api object and associate it with the Blueprint
api = Api(steps_api)

class StepsAPI:
    class _Steps(Resource):
        """
        API operations for managing steps entries.
        """

        @token_required()
        def post(self):
            """
            Add a new steps entry for the authenticated user.
            """
            current_user = g.current_user
            body = request.get_json()

            # Validate steps
            steps = body.get('steps')
            if steps is None or not isinstance(steps, int) or steps < 0:
                return {'message': 'Invalid steps provided'}, 400

            try:
                # Ensure no existing entry exists
                existing_steps = Steps.query.filter_by(user=current_user.uid).first()
                if existing_steps:
                    return {'message': 'Steps entry already exists'}, 400

                # Create a new steps entry
                new_steps = Steps(user=current_user.uid, steps=steps)
                new_steps.create()
                return jsonify({'message': 'Steps added successfully', 'steps': new_steps.read()})
            except Exception as e:
                return {'message': 'Failed to create steps', 'error': str(e)}, 500

        @token_required()
        def put(self):
            """
            Update an existing steps entry for the authenticated user.
            """
            current_user = g.current_user
            body = request.get_json()

            # Validate steps
            steps = body.get('steps')
            if steps is None or not isinstance(steps, int) or steps < 0:
                return {'message': 'Invalid steps provided'}, 400

            try:
                # Fetch and update the user's steps entry
                steps_entry = Steps.query.filter_by(user=current_user.uid).first()
                if not steps_entry:
                    return {'message': 'No steps entry found to update'}, 404

                steps_entry.steps = steps
                steps_entry.create()  # Save changes to the database
                return jsonify({'message': 'Steps updated successfully', 'steps': steps_entry.read()})
            except Exception as e:
                return {'message': 'Failed to update steps', 'error': str(e)}, 500

        @token_required()
        def get(self):
            """
            Get the current user's steps entry.
            """
            current_user = g.current_user

            try:
                steps_entry = Steps.query.filter_by(user=current_user.uid).first()
                if steps_entry:
                    return jsonify({'message': 'Steps retrieved successfully', 'steps': steps_entry.read()})
                else:
                    return {'message': 'No steps entry found for the user'}, 404
            except Exception as e:
                return {'message': 'Failed to retrieve steps', 'error': str(e)}, 500
        @token_required()
        def delete(self):
            """
            Delete an existing steps entry for the authenticated user.
            """
            current_user = g.current_user

            try:
                # Fetch and delete the user's steps entry
                steps_entry = Steps.query.filter_by(user=current_user.uid).first()
                if not steps_entry:
                    return {'message': 'No steps entry found to delete'}, 404

                steps_entry.delete()  # Delete the entry from the database
                return jsonify({'message': 'Steps entry deleted successfully'})
            except Exception as e:
                return {'message': 'Failed to delete steps entry', 'error': str(e)}, 500
# Register the API resources with the Blueprint
api.add_resource(StepsAPI._Steps, '/steps')