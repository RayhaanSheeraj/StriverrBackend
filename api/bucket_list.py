from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from __init__ import app, db
from api.jwt_authorize import token_required
from model.bucket_list import bucket_list

bucket_list_api = Blueprint('bucket_list_api', __name__, url_prefix='/api')
api = Api(bucket_list_api)

class BucketList(Resource):
    @token_required
    def get(self):
        """
        Retrieve all bucket list items.
        """
        current_user = g.current_user  # Ensure user is extracted
        if not current_user:
            return jsonify({"message": "Unauthorized: User not found"}), 401

        bucket_list_items = bucket_list.query.filter_by(user=current_user.id).all()
        all_items = str([item.read() for item in bucket_list_items])
        return jsonify(all_items)
    
    @token_required
    def post(self):
        """
        Create a new bucket list item.
        """
        current_user = g.current_user
        if not current_user:
            return jsonify({"message": "Unauthorized: User not found"}), 401
        
        data = request.get_json()
        if not data or not data.get('title'):
            return jsonify({"message": "Title is required"}), 400
        
        bucket_list_item = bucket_list(
            title=data['title'],
            description=data.get('description', ''),
            status=data.get('status', 'Pending'),
            user=current_user.id
        )
        bucket_list_item.create()
        return jsonify(bucket_list_item.read())

    @token_required
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
        
        bucket_list_item = bucket_list.query.filter_by(id=data['id'], user=current_user.id).first()
        if bucket_list_item:
            bucket_list_item.update(
                title=data.get('title'),
                description=data.get('description'),
                status=data.get('status')
            )
            return jsonify(bucket_list_item.read())
        return jsonify({'message': 'Item not found or unauthorized'}), 404

    @token_required
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
        
        bucket_list_item = bucket_list.query.filter_by(id=data['id'], user=current_user.id).first()
        if bucket_list_item:
            bucket_list_item.delete()
            return jsonify({'message': 'Item deleted successfully'})
        return jsonify({'message': 'Item not found or unauthorized'}), 404

api.add_resource(BucketList, '/bucketlist')

if __name__ == '__main__':
    app.run(debug=True)