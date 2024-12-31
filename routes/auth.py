from flask import Blueprint, request, jsonify, render_template
from database import db
from models.user import User

auth = Blueprint('auth', __name__)
main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html")

@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'})

@main.route("/tasks")
def tasks():
    # در اینجا داده‌های تسک‌ها را از دیتابیس بگیرید
    tasks = [
        {"id": 1, "title": "Task 1", "description": "Description 1"},
        {"id": 2, "title": "Task 2", "description": "Description 2"}
    ]
    return render_template("tasks.html", tasks=tasks)