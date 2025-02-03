from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from flask_cors import CORS
from __init__ import app, db
from api.jwt_authorize import token_required
from model.bucket_list import BucketList

bucket_list_api = Blueprint('bucket_list_api', __name__, url_prefix='/api')
CORS(bucket_list_api)
api = Api(bucket_list_api)

class BucketListAPI:
    class _CRUD(Resource):

        def get(self):

            bucket_id = request.args.get('id')

            if bucket_id:

                bucketlist = BucketList.query.get(bucket_id)
                if not bucketlist:
                    return {'message': 'Bucket list not found'}, 404
                return jsonify(bucketlist.read())

            all_bucketlists = BucketList.query.all()
            return jsonify([bucketlist.read() for bucketlist in all_bucketlists])
        

        def post(self):
        
            data = request.get_json()

            bucketlist = BucketList(
                title=data.get('title'),
                description=data.get('description'),
                category=data.get('category'),
                user=1,
            )

            try:
                bucketlist.create()
                return jsonify(bucketlist.read())
            except Exception as e:
                return {'message': f'Error saving bucketlist: {e}'}, 500

        def put(self):
            """
            Update a bucket list item.
            """
            current_user = g.current_user
            if not current_user:
                return jsonify({"message": "Unauthorized: User not found"}), 401

            data = request.get_json()
            if not data or not data.get('id'):
                return jsonify({"message": "ID is required"}), 400
            
            bucket_list_item = BucketList.query.filter_by(id=data['id'], user=current_user.id).first()
            if bucket_list_item:
                bucket_list_item.update(
                    title=data.get('title'),
                    description=data.get('description'),
                    category=data.get('category')
                )
                return jsonify(bucket_list_item.read())
            return jsonify({'message': 'Item not found or unauthorized'}), 404

        def delete(self):
            """
            Delete a bucket list item.
            """
            current_user = g.current_user
            if not current_user:
                return jsonify({"message": "Unauthorized: User not found"}), 401

            data = request.get_json()
            if not data or not data.get('id'):
                return jsonify({"message": "ID is required"}), 400
            
            bucket_list_item = BucketList.query.filter_by(id=data['id'], user=current_user.id).first()
            if bucket_list_item:
                bucket_list_item.delete()
                return jsonify({'message': 'Item deleted successfully'})
            return jsonify({'message': 'Item not found or unauthorized'}), 404

    api.add_resource(_CRUD, '/bucketlist')