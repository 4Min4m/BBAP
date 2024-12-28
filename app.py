# app.py
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Sample tasks data
tasks = [
    {"id": 1, "task": "Learn Flask"},
    {"id": 2, "task": "Implement APIs"}
]

@app.route('/')
def home():
    return render_template('index.html')

# To get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks})

# To create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    new_task = request.json
    new_task["id"] = len(tasks) + 1  # Simple ID generation
    tasks.append(new_task)
    return jsonify(new_task), 201

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')