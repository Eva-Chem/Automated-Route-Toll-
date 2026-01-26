"""
Authentication & Role Middleware
File: backend/middleware/auth_middleware.py
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from models.models import User


# -------------------------------------------------
# HELPER: GET CURRENT USER
# -------------------------------------------------
def get_current_user():
    """
    Fetch logged-in user from JWT token
    """
    user_id = get_jwt_identity()
    if not user_id:
        return None

    return User.query.filter_by(user_id=user_id).first()


# -------------------------------------------------
# ROLE CHECK DECORATOR (GENERIC)
# -------------------------------------------------
def role_required(allowed_roles):
    """
    Generic role-based access decorator
    """
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user = get_current_user()

            if not user:
                return jsonify({"error": "User not found"}), 404

            if user.role.lower() not in allowed_roles:
                return jsonify({
                    "error": "Access denied",
                    "required_roles": allowed_roles,
                    "your_role": user.role
                }), 403

            return fn(*args, **kwargs)

        return wrapper
    return decorator


# -------------------------------------------------
# SPECIFIC ROLE DECORATORS
# -------------------------------------------------
def admin_required(fn):
    return role_required(["admin"])(fn)


def operator_required(fn):
    return role_required(["operator", "admin"])(fn)


def driver_required(fn):
    return role_required(["driver"])(fn)
