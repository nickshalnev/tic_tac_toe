import logging
from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    logger.info("Creating Flask application...")

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'  # for prod we need to store it in other place

    from .routes import main
    app.register_blueprint(main)

    socketio.init_app(app)

    logger.info("Flask application created successfully")

    return app
