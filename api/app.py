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

@app.route('/api/neil')
def get_neil():
    InfoDb = []
    InfoDb.append({
        "FirstName": "Neil",
        "LastName": "Chandra",
        "DOB": "March 9",
        "Residence": "Kyrgyzstan",
        "Email": "reilchandra9@gmail.com",
        "Sports": ["Soccer", "Badminton"],
        "Cars": ["Honda", "Prius"]
    })

@app.route('/api/hithin')
def get_Hithin():
    InfoDb = []
    InfoDb.append({
        "FirstName": "Hithin",
        "LastName": "Pulamarasetty",
        "DOB": "December 14",
        "Residence": "San Fransisco",
        "Email": "Hithinp@gmail.com",
        "Formula 1": ["Mclaren", "Red bull", "Mercedes", "Ferrari", "Aston Martin", "Haas"], 
        "Scioly Events": ["Flight", "Helicopter", "Electric vehicle", "Air Traj", "Robot Tour", "Wheeled Vehicle"]
    })
    
@app.route('/api/pradyun')
def get_pradyun():
    InfoDb = []
    InfoDb.append({
        "FirstName": "Pradyun",
        "LastName": "Gowda",
        "DOB": "February 28",
        "Residence": "4S Ranch",
        "Email": "pradyungowda@gmail.com",
        "Extracurriculars": ["Math Club", "Physics Club", "Bio Club", "Competitive Badminton"],
        "FamilyOwnedCars": ["Tesla Model S", "Nissan Rogue"]
    })

@app.route('/api/nikith')
def get_nikith():
    InfoDb = []
    InfoDb.append({
        "FirstName": "Nikith",
        "LastName": "Muralikrishnan",
        "DOB": "October 4",
        "Residence": "Houston",
        "Email": "nikithmuralikrishnan@gmail.com",
        "FavoriteVideogame" : ["Brawl Stars", "Minecraft"]
    })

@app.route('/api/kush')
def get_kush():
    InfoDb = []
    InfoDb.append({
        "FirstName": "Kush",
        "LastName": "Kharia",
        "DOB": "February 6",
        "Residence": "North Pole",
        "Email": "khariakush06@gmail.com",
        "FavoriteSoccerPlayers": ["Virgil Van Dijk", "Lamine Yamal", "Mo Salah"]
    })