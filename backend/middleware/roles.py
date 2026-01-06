from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def role_required(*allowed_roles):
    """
    Restrict endpoint access based on user role.
    Example: @role_required("ADMIN", "OPERATOR")
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            user = get_jwt_identity()
            if not user or "role" not in user:
                return jsonify({"error": "Invalid token"}), 401

            if user["role"] not in allowed_roles:
                return jsonify({"error": "Forbidden"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
