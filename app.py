from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from utils.db import db, init_db
from models.task import Task
from forms.task_form import TaskForm
from models import User
from routes.auth import auth
from routes.protected_routes import protected
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'
init_db(app)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

users = {}

# Register new user
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if username in users:
        return jsonify({"msg": "User already exists"}), 400

    users[username] = password
    return jsonify({"msg": "User registered successfully"}), 201

# Login
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if users.get(username) != password:
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# Task manager page
@app.route('/tasks', methods=['GET', 'POST'])
def task_manager():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(task=form.task.data)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('task_manager'))

    tasks = Task.query.all()
    return render_template('tasks.html', form=form, tasks=tasks)

# Register Blueprint for protected routes and auth
app.register_blueprint(protected, url_prefix='/protected')
app.register_blueprint(auth, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')