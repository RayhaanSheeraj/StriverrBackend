from flask import Blueprint, Flask, jsonify, request
from datetime import datetime
from flask_restful import Api, Resource
import uuid
from __init__ import app
from flask_cors import CORS

goals_api = Blueprint('goals_api', __name__, url_prefix='/api')
api = Api(goals_api)

CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for all routes

# In-memory storage for goals and progress
goals = {}
user_progress = {}

@app.route('/api/goals', methods=['GET'])
def get_goal():
    print("GET /api/goals was hit")
    goal_list = [
        "Drink 2 liters of water daily for 7 days",
        "Read 10 pages of a book daily for 5 days",
        "Walk 5,000 steps daily for 7 days",
        "Write a journal entry daily for 3 days",
        "Complete one coding problem daily for 5 days"
    ]
    goal_id = str(uuid.uuid4())
    selected_goal = {
        "goal_id": goal_id,
        "goal": goal_list[datetime.now().second % len(goal_list)],
        "duration_days": datetime.now().second % 7 + 1
    }
    goals[goal_id] = {
        "goal": selected_goal["goal"],
        "duration_days": selected_goal["duration_days"],
        "start_date": datetime.now().strftime('%Y-%m-%d'),
        "completed_days": 0
    }
    return jsonify(selected_goal), 200

@app.route('/api/progress/<goal_id>', methods=['POST'])
def track_progress(goal_id):
    print(f"POST /api/progress/{goal_id} was hit")
    if goal_id not in goals:
        return jsonify({"error": "Goal ID not found."}), 404

    today = datetime.now().strftime('%Y-%m-%d')

    if goal_id not in user_progress:
        user_progress[goal_id] = set()

    if today in user_progress[goal_id]:
        return jsonify({"message": "Progress already recorded for today."}), 200

    user_progress[goal_id].add(today)
    goals[goal_id]["completed_days"] += 1

    if goals[goal_id]["completed_days"] >= goals[goal_id]["duration_days"]:
        return jsonify({"message": "Goal completed! Congratulations!", "goal": goals[goal_id]}), 200

    return jsonify({"message": "Progress recorded.", "goal": goals[goal_id]}), 200

@app.route('/api/progress/<goal_id>', methods=['GET'])
def get_progress(goal_id):
    print(f"GET /api/progress/{goal_id} was hit")
    if goal_id not in goals:
        return jsonify({"error": "Goal ID not found."}), 404

    progress = {
        "goal": goals[goal_id]["goal"],
        "duration_days": goals[goal_id]["duration_days"],
        "completed_days": goals[goal_id]["completed_days"],
        "remaining_days": goals[goal_id]["duration_days"] - goals[goal_id]["completed_days"]
    }
    return jsonify(progress), 200

@app.route('/', methods=['GET'])
def home():
    return "Goaltrack API is running!", 200

# Explicitly define and expose the run_api function
def run_api():
    app.run(debug=False, host='0.0.0.0', port=5648)

if __name__ == '__main__':
    run_api()
