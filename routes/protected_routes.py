from flask import Blueprint, request, jsonify
from utils.db import db  # اگر db استفاده می‌کنید

#  Blueprint
protected = Blueprint('protected', __name__)

@protected.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({'msg': 'Invalid data'}), 400
    return jsonify({'msg': 'Task added successfully'})