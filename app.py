from flask import Flask
from database import db
from routes.auth import auth
from routes.auth import main

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(main)

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True,host = '0.0.0.0')