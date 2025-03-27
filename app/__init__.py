from flask import Flask

from .config import Config
from .utils.database import db, bcrypt
from app.routes.admin_auth import admin_auth
from app.routes.meeting_crud import meeting_crud


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(admin_auth, url_prefix="/api/admin/auth")
    app.register_blueprint(meeting_crud, url_prefix="/api/meeting")
    # app.register_blueprint(employee_crud, url_prefix="/api/employee")

    return app
