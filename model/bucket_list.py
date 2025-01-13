from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from __init__ import app, db
from api.jwt_authorize import token_required
# from model.bucket_list import BucketList  # Assuming you have a BucketList model

bucket_list_api = Blueprint('bucket_list_api', __name__, url_prefix='/api')
api = Api(bucket_list_api)

class BucketListAPI:
    """
    Define the API CRUD endpoints for the BucketList model.
    There are four operations that correspond to common HTTP methods:
    - post: create a new bucket list item
    - get: read bucket list items
    - put: update a bucket list item
    - delete: delete a bucket list item
    """
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create a new bucket list item.
            """
            current_user = g.current_user
            data = request.get_json()
            bucket_list_item = BucketList(data['title'], data['description'], current_user.id)
            bucket_list_item.create()
            return jsonify(bucket_list_item.read())

        @token_required()
        def get(self):
            """
            Retrieve all bucket list items.
            """
            bucket_list_items = BucketList.query.all()
            all_items = [item.read() for item in bucket_list_items]
            return jsonify(all_items)

        @token_required()
        def put(self):
            """
            Update a bucket list item.
            """
            data = request.get_json()
            bucket_list_item = BucketList.query.get(data['id'])
            if bucket_list_item:
                bucket_list_item.update(data['title'], data['description'])
                return jsonify(bucket_list_item.read())
            return {'message': 'Item not found'}, 404

        @token_required()
        def delete(self):
            """
            Delete a bucket list item.
            """
            data = request.get_json()
            bucket_list_item = BucketList.query.get(data['id'])
            if bucket_list_item:
                bucket_list_item.delete()
                return {'message': 'Item deleted successfully'}
            return {'message': 'Item not found'}, 404

api.add_resource(BucketListAPI._CRUD, '/bucketlist')

if __name__ == '__main__':
    app.run(debug=True)