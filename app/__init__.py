from flask import Flask
from app.models import init_db


def create_app():
    """Application factory for the Bellbird Books web app."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'bellbird-dev-key'

    # Initialise database tables on startup
    with app.app_context():
        init_db()

    from app.routes import main
    app.register_blueprint(main)

    return app