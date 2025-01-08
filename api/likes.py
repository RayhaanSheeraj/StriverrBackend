import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.channel import Channel
from model.group import Group
from model.user import User

"""
This Blueprint object is used to define APIs for the Channel model.
- Blueprint is used to modularize application files.
- This Blueprint is registered to the Flask app in main.py.
"""
channel_api = Blueprint('channel_api', __name__, url_prefix='/api')

"""
The Api object is connected to the Blueprint object to define the API endpoints.
- The API object is used to add resources to the API.
- The objects added are mapped to code that contains the actions for the API.
- For more information, refer to the API docs: https://flask-restful.readthedocs.io/en/latest/api.html
"""
api = Api(channel_api)

class LikesAPI:
    """
    Define the API CRUD endpoints for the Channel model.
    There are four operations that correspond to common HTTP methods:
    - post: create a new channel
    - get: read channels
    - put: update a channel
    - delete: delete a channel
    """
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create a new channel.
            """
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            
            # Validate the presence of required keys
            if not data:
                return {'message': 'No input data provided'}, 400
            if 'name' not in data:
                return {'message': 'Channel name is required'}, 400
            if 'group_id' not in data:
                return {'message': 'Group ID is required'}, 400
            if 'attributes' not in data:
                data['attributes'] = {}
                
            # Create a new channel object using the data from the request
            likes = Channel(data['name'], data['group_id'], data.get('attributes', {}))
            # Save the channel object using the Object Relational Mapper (ORM) method defined in the model
            likes.create()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(likes.read())

        @token_required()
        def get(self):
            """
            Retrieve a single channel by ID.
            """
            # Obtain and validate the request data sent by the RESTful client API
            data = request.get_json()
            if data is None:
                return {'message': 'Channel data not found'}, 400
            if 'id' not in data:
                return {'message': 'Channel ID not found'}, 400
            # Find the channel to read
            channel = Channel.query.get(data['id'])
            if channel is None:
                return {'message': 'Channel not found'}, 404
            # Convert Python object to JSON format 
            json_ready = channel.read()
            # Return a JSON restful response to the client
            return jsonify(json_ready)

        @token_required()
        def put(self):
            """
            Update a channel.
            """
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Find the channel to update
            channel = Channel.query.get(data['id'])
            if channel is None:
                return {'message': 'Channel not found'}, 404
            # Update the channel object using the data from the request
            channel._name = data['name']
            channel._group_id = data['group_id']
            channel._attributes = data.get('attributes', {})
            # Save the channel object using the Object Relational Mapper (ORM) method defined in the model
            channel.update()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(channel.read())

        @token_required()
        def delete(self):
            """
            Delete a channel.
            """
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Find the channel to delete
            channel = Channel.query.get(data['id'])
            if channel is None:
                return {'message': 'Channel not found'}, 404
            # Delete the channel object using the Object Relational Mapper (ORM) method defined in the model
            channel.delete()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify({'message': 'Channel deleted'})