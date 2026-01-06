# backend/middleware/auth_middleware.py
from functools import wraps
from flask import request, jsonify
import jwt
from config import Config
from models.models import User
from db.database import db

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            token = token.replace("Bearer ", "")
            data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(data["user_id"])
            if not current_user:
                return jsonify({"message": "User not found!"}), 401
        except Exception as e:
            return jsonify({"message": "Token is invalid!", "error": str(e)}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(current_user, *args, **kwargs):
            if current_user.role not in roles:
                return jsonify({"message": "Forbidden: You do not have access to this resource"}), 403
            return f(current_user, *args, **kwargs)
        return wrapper
    return decorator
