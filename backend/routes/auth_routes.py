from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from services.auth_service import authenticate

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Missing credentials"}), 400

    user = authenticate(data["username"], data["password"])

    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "sub": {
                "id": user.id,
                "role": user.role
            }
        }
    )

    return jsonify({
        "token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    }), 200
