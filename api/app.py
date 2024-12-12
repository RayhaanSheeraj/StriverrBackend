from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')
@app.route('/api/rayhaan')
def get_rayhaan():
    InfoDb = []
    InfoDb.append({
        "FirstName": "Rayhaan",
        "LastName": "Sheeraj",
        "DOB": "July 24",
        "Residence": "Iceland",
        "Email": "rayhaanss786@gmail.com",
        "Color": ["Blue", "Black", "Green"]
    })
    return jsonify(InfoDb)
@app.route('/api/neil')
def get_neil():
    InfoDb = []
    InfoDb.append({
        "FirstName": "Neil",
        "LastName": "Chandra",
        "DOB": "March 9",
        "Residence": "Kyrgyzstan",
        "Email": "reilchandra9@gmail.com",
        "Color": ["Yellow", "Red", "Green"]
    })
    return jsonify(InfoDb)
@app.route('/api/hithin')
def get_Hithin():
    InfoDb = []
    InfoDb.append({
        "FirstName": "Hithin",
        "LastName": "Pulamarasetty",
        "DOB": "December 14",
        "Residence": "San Fransisco",
        "Email": "Hithinp@gmail.com",
        "Color": ["Purple", "Light Pink", "Hot Pink"]
    })
    return jsonify(InfoDb)
@app.route('/api/pradyun')
def get_pradyun():
    InfoDb = []
    InfoDb.append({
        "FirstName": "Pradyun",
        "LastName": "Gowda",
        "DOB": "February 28",
        "Residence": "4S Ranch",
        "Email": "pradyungowda@gmail.com",
        "Color": ["Orange", "Black", "Red"]
    })
    return jsonify(InfoDb)
@app.route('/api/nikith')
def get_nikith():
    InfoDb = []
    InfoDb.append({
        "FirstName": "Nikith",
        "LastName": "Muralikrishnan",
        "DOB": "October 4",
        "Residence": "Houston",
        "Email": "nikithmuralikrishnan@gmail.com",
        "Color": ["Cyan"]
    })
    return jsonify(InfoDb)
@app.route('/api/kush')
def get_kush():
    InfoDb = []
    InfoDb.append({
        "FirstName": "Kush",
        "LastName": "Kharia",
        "DOB": "February 6",
        "Residence": "North Pole",
        "Email": "khariakush06@gmail.com",
        "Color": ["Hot Pink", "Neon Pink", "Dark Pink"]
    })
    return jsonify(InfoDb)
#test
# add an HTML endpoint to flask app
@app.route('/')
def say_hello():
    html_content = """
    <html>
    <head>
        <title>Hellox</title>
    </head>
    <body>
        <h2>Hello, World!</h2>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    # starts flask server on default port, http://127.0.0.1:5001
    app.run(port=3333)