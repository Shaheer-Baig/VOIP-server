from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voip.db'  # SQLite database
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)
    socketio.init_app(app)

    # Register routes
    from App.routes import routes
    app.register_blueprint(routes)

    return app
