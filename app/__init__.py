from flask import Flask

from .config import Config
from .utils.database import db, bcrypt
from app.routes.admin_auth import admin_auth
from app.routes.employee_crud import employee_crud


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(admin_auth, url_prefix="/api/admin/auth")
    app.register_blueprint(employee_crud, url_prefix="/api/employee")

    return app
