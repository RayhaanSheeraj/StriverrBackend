from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

API_URL = 'https://api.api-ninjas.com/v1/quotes'
API_KEY = 'dsH4Bmo4W7wv5SVKvjbSRQ==mRJPmT9DcU5oqtI7'  

@app.route('/get_quote', methods=['GET'])
def get_quote():
    
    category = request.args.get('category', None)
    headers = {'X-Api-Key': API_KEY}
    

    if category:
        url = f"{API_URL}?category={category}"
    else:
        url = API_URL

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            
            return jsonify(response.json()), 200
        else:
            
            return jsonify({
                "error": f"API request failed with status {response.status_code}",
                "details": response.text
            }), response.status_code
    except Exception as e:
        
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Quotes API!"})

if __name__ == '__main__':
    app.run(debug=True)
