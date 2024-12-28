from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Task {self.task}>"

# Initialize DB manually (remove before_first_request decorator)
def init_db():
    with app.app_context():
        db.create_all()

@app.route('/')
def home():
    return "Welcome to BBAP Task Manager"

# To get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify({"tasks": [task.task for task in tasks]})

# To create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    new_task = request.json
    task = Task(task=new_task['task'])
    db.session.add(task)
    db.session.commit()
    return jsonify({"task": task.task}), 201

# No task was found
@app.route('/tasks', methods=['GET'])
def fetch_tasks():
    tasks = Task.query.all()
    if tasks:  # Check if there are tasks
        return jsonify({"tasks": [task.task for task in tasks]})
    return jsonify({"message": "No tasks found"}), 404

if __name__ == "__main__":
    init_db()  # Explicitly call init_db
    app.run(debug=True, host='0.0.0.0')