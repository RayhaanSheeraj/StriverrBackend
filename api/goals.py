import logging  # Add this import
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # Used for REST API building
from __init__ import app, db  # Ensure __init__.py initializes your Flask app
from api.jwt_authorize import token_required
from model.goals import StriverGoals
# Blueprint for the API
goals_api = Blueprint('goals_api', __name__, url_prefix='/api')

api = Api(goals_api)  # Attach Flask-RESTful API to the Blueprint

class GoalsAPI:
    """
    Define the API CRUD endpoints for the Post model.
    There are four operations that correspond to common HTTP methods:
    - post: create a new post
    - get: read posts
    - put: update a post
    - delete: delete a post
    """
    class _CRUD(Resource):
        @token_required()
        def get(self):
            # Obtain the current user
            # current_user = g.current_user
            # Find all the posts by the current user
            posts = StriverGoals.query.all()
            # Prepare a JSON list of all the posts, uses for loop shortcut called list comprehension
            json_ready = [post.read() for post in posts]
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)
        @token_required()
        def post(self):
            data = request.get_json()
            post = StriverGoals(getgoals=data['getgoals'], goaloutput=data['goaloutput'], progress=data.get('progress'))
            post.create()
            return jsonify(post.read())
        @token_required()
        def put(self):
            data = request.get_json()
            post = StriverGoals.query.get(data['id'])
            if post:
                try:
                    post.progress = data.get('progress')
                    db.session.commit()  # Directly commit the session
                    return jsonify(post.read())
                except Exception as e:
                    logging.error(f"Error updating post: {e}")
                    return jsonify({"error": "An error occurred while updating the post"}), 500
            return jsonify({"message": "Post not found"}), 404
        @token_required()
        def get(self):
            try:
                # Query all entries in the BinaryHistory table
                entries = StriverGoals.query.all()
                # Convert the entries to a list of dictionaries
                results = [entry.read() for entry in entries]
                # Return the list of results in JSON format
                return jsonify(results)
            except Exception as e:
                # Return an error message in case of failure
                return jsonify({"error": str(e)}), 500
        @token_required()
        def delete(self):
            data = request.get_json()
            post = StriverGoals.query.get(data['id'])
            if post:
                post.delete()
                return jsonify({"message": "Post deleted"})
            return jsonify({"message": "Post not found"}), 404
    """
    Map the _CRUD class to the API endpoints for /post.
    - The API resource class inherits from flask_restful.Resource.
    - The _CRUD class defines the HTTP methods for the API.
    """
    api.add_resource(_CRUD, '/goals')