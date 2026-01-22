# backend/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from db import db, User
import uuid

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        role = data.get("role", "toll_operator")  # NEW: Get role, default to toll_operator

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # NEW: Validate role
        if role not in ["admin", "toll_operator"]:
            return jsonify({"error": "Invalid role. Must be 'admin' or 'toll_operator'"}), 400

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"error": "Username already exists"}), 400

        # Create new user
        password_hash = generate_password_hash(password)
        new_user = User(
            user_id=uuid.uuid4(),
            username=username,
            password_hash=password_hash,
            role=role  # NEW: Add role
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "User registered successfully",
            "user": {
                "user_id": str(new_user.user_id),
                "username": new_user.username,
                "role": new_user.role  # NEW: Return role
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Find user
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid username or password"}), 401

        # NEW: Create access token with role in additional claims
        access_token = create_access_token(
            identity=str(user.user_id),
            additional_claims={"role": user.role}  # Include role in JWT
        )

        return jsonify({
            "message": "Login successful",
            "token": access_token,
            "user": {
                "user_id": str(user.user_id),
                "username": user.username,
                "role": user.role  # NEW: Return role
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500