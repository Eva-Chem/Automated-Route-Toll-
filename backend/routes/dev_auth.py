from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.models import User

dev_auth_bp = Blueprint("dev_auth_bp", __name__)

@dev_auth_bp.route("/dev-login", methods=["POST"])
def dev_login():
    data = request.get_json()

    if not data or "email" not in data:
        return jsonify({
            "success": False,
            "message": "Email is required"
        }), 400

    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    # Create JWT with user_id as identity
    access_token = create_access_token(identity=str(user.user_id))

    return jsonify({
        "success": True,
        "access_token": access_token,
        "role": user.role
    }), 200
