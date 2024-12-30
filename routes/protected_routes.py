from flask import Blueprint, request, jsonify, redirect, url_for
from utils.db import db
from models import Task

protected = Blueprint('protected', __name__)

# Add task
@protected.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task_name = data.get('task')
    new_task = Task(name=task_name)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"msg": "Task added successfully!"})

# Delete task
@protected.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"msg": "Task deleted successfully!"})
    else:
        return jsonify({"msg": "Task not found"}), 404
