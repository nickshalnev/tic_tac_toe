import logging
from app import create_app, socketio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

if __name__ == '__main__':
    logger.info("Starting the application...")
    socketio.run(app, host='0.0.0.0', port=15239, debug=True)
