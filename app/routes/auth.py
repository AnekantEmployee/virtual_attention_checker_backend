from flask import Blueprint, request, jsonify
from app.models import User
from app.utils.database import db, bcrypt

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
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
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    # Hash password
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    # Create user
    user = User(name=data["name"], email=data["email"], password=hashed_password)

    db.session.add(user)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "User created successfully",
                "user": {"id": user.id, "name": user.name, "email": user.email},
            }
        ),
        201,
    )


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing Email or Password"}), 400

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not bcrypt.check_password_hash(user.password, data["password"]):
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
