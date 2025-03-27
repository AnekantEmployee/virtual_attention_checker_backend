from app.models import Admin
from app.utils.database import db, bcrypt
from flask import Blueprint, request, jsonify


admin_auth = Blueprint("auth", __name__)


@admin_auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Basic validation
    if (
        not data
        or not data.get("name")
        or not data.get("password")
        or not data.get("email")
    ):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if user exists
    if Admin.query.filter_by(email=data["email"].lower().strip()).first():
        return jsonify({"error": "Email already exists"}), 400

    # Hash password
    hashed_password = (
        bcrypt.generate_password_hash(data["password"]).strip().decode("utf-8")
    )

    # Create user
    user = Admin(
        name=data["name"].strip(),
        email=data["email"].lower().strip(),
        password=hashed_password,
    )

    db.session.add(user)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Admin created successfully",
                "user": {"id": user.id, "name": user.name, "email": user.email},
            }
        ),
        201,
    )


@admin_auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing Email or Password"}), 400

    user = Admin.query.filter_by(email=data["email"].lower().strip()).first()

    if not user or not bcrypt.check_password_hash(
        user.password, data["password"].strip()
    ):
        return jsonify({"error": "Invalid email or password"}), 401

    return (
        jsonify(
            {
                "message": "Login successful",
                "user": {"id": user.id, "email": user.email},
            }
        ),
        200,
    )
