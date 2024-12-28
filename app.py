from flask import Flask
from utils.db import init_db
from routes.auth import auth
from routes.protected_routes import protected

app = Flask(__name__)

# Initialize the database
init_db(app)

# Register blueprints
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(protected, url_prefix='/protected')

@app.route('/')
def home():
    return "Welcome to BBAP WebApp!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')