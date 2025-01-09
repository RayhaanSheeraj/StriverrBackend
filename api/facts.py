from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


API_URL = 'https://api.api-ninjas.com/v1/facts'
API_KEY = 'TJlX/mNVAxfBDJN4SEd4zg==Lh5Vs0FxjzliaXKA'

@app.route('/get_facts', methods=['GET'])
def get_facts():
    try:
       
        limit = request.args.get('limit', default=3, type=int)
        
        
        api_url = f'{API_URL}?limit={limit}'
        response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
        
        if response.status_code == requests.codes.ok:
            
            return jsonify({'status': 'success', 'data': response.json()})
        else:
            
            return jsonify({'status': 'error', 'message': response.text}), response.status_code
    except Exception as e:
        # returns string e that has the fact
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)