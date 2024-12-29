from flask import Flask, jsonify, request, render_template, redirect, url_for
from utils.db import db, init_db
from models.task import Task
from forms.task_form import TaskForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'
init_db(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(task=form.task.data)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))

    tasks = Task.query.all()
    return render_template('tasks.html', form=form, tasks=tasks)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    if tasks:
        return jsonify({"tasks": [{"id": task.id, "task": task.task} for task in tasks]})
    return jsonify({"message": "No tasks found"}), 404

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    if not data or 'task' not in data:
        return jsonify({"message": "Invalid input"}), 400

    new_task = Task(task=data['task'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"id": new_task.id, "task": new_task.task}), 201

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({"message": "Task not found"}), 404

    data = request.json
    if 'task' not in data:
        return jsonify({"message": "Invalid input"}), 400

    task.task = data['task']
    db.session.commit()
    return jsonify({"message": "Task updated successfully"})

@app.route('/tasks/<int:id>/delete', methods=['GET'])
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')