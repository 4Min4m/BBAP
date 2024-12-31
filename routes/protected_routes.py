from flask import Blueprint, request, jsonify
from utils.db import db
from models.task import Task
from flask_jwt_extended import jwt_required, get_jwt_identity

protected = Blueprint('protected', __name__)

# Get all tasks
@protected.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    tasks = Task.query.all()
    task_list = [{"id": task.id, "task": task.task} for task in tasks]
    return jsonify({"tasks": task_list}), 200

# Add a new task
@protected.route('/tasks', methods=['POST'])
@jwt_required()
def add_task():
    data = request.get_json()
    task_name = data.get('task')
    new_task = Task(task=task_name)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added successfully!"}), 201

# Delete a task
@protected.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"}), 200