"""Role-based authorization middleware for Flask-JWT-Extended"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def admin_required(fn):
    """
    Decorator to require admin role for access.
    
    Usage:
        @app.route("/admin-only")
        @jwt_required()
        @admin_required
        def admin_endpoint():
            return jsonify({"message": "Admin access granted"}), 200
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Verify JWT is present and valid
        verify_jwt_in_request()
        
        # Extract role from JWT claims
        claims = get_jwt()
        role = claims.get("role")
        
        # Check if user is admin
        if role != "admin":
            return jsonify({
                "message": "Forbidden: Admin access required",
                "error": "insufficient_permissions",
                "required_role": "admin",
                "your_role": role
            }), 403
        
        return fn(*args, **kwargs)
    
    return wrapper


def role_required(allowed_roles):
    """
    Decorator factory for role-based access control.
    
    Usage:
        @app.route("/operators-and-admins")
        @jwt_required()
        @role_required(["admin", "operator"])
        def operator_endpoint():
            return jsonify({"message": "Access granted"}), 200
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            role = claims.get("role")
            
            if role not in allowed_roles:
                return jsonify({
                    "message": "Forbidden: insufficient permissions",
                    "error": "role_not_allowed",
                    "required_roles": allowed_roles,
                    "your_role": role
                }), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator

