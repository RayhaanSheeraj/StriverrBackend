from flask import Blueprint, jsonify
from flask_restful import Api, Resource
import requests

bucket_list_api = Blueprint('bucket_list_api', __name__, url_prefix='/api')
api = Api(bucket_list_api)

class BucketListAPI:
    class _BucketList(Resource):
        def get(self):
            try:
                bucket_data = get_bucket_item()
                if bucket_data:
                    return jsonify(bucket_data)
                else:
                    return jsonify({"error": "No data found"}), 404
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    api.add_resource(_BucketList, '/bucketlist')

def get_bucket_item():
    api_url = "https://api.api-ninjas.com/v1/bucketlist"
    headers = {"X-Api-Key": "JGc40AnVLVz3giTZJgCFDg==mSbIyNfV4Y3lX4Ln"}

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request exception occurred: {req_err}")
    return None
