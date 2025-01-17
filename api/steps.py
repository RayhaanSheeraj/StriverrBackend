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
        API operation for managing steps entries.
        """

        @token_required()
        def post(self):
            """
            Add or update a steps entry for the authenticated user.
            """
            current_user = g.current_user
            body = request.get_json()

            # Validate steps
            steps = body.get('steps')
            if steps is None or not isinstance(steps, int) or steps < 0:
                return {'message': 'Invalid steps provided'}, 400

            try:
                # Check if the user already has an existing steps entry
                existing_steps = Steps.query.filter_by(user=current_user.uid).first()

                if existing_steps:
                    # Update the existing steps entry
                    existing_steps.steps = steps
                    existing_steps.create()  # Save changes to the database
                    return jsonify({'message': 'Steps updated successfully', 'steps': existing_steps.read()})
                else:
                    # Create a new steps entry
                    new_steps = Steps(user=current_user.uid, steps=steps)
                    new_steps.create()
                    return jsonify({'message': 'Steps added successfully', 'steps': new_steps.read()})
            except Exception as e:
                return {'message': 'Failed to process steps', 'error': str(e)}, 500

# Register the API resources with the Blueprint
api.add_resource(StepsAPI._Steps, '/steps')
