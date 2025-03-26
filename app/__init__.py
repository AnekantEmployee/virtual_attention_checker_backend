from flask import Flask

from .config import Config
from app.routes.auth import auth_bp
from .utils.database import db, bcrypt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app
