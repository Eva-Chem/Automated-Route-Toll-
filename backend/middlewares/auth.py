from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        
        # Robust role check: handles both nested 'sub' and direct 'role' claims
        sub_data = claims.get("sub", {})
        role = sub_data.get("role") if isinstance(sub_data, dict) else claims.get("role")

        if not role or role.upper() != "ADMIN":
            return jsonify({
                "msg": "Forbidden: Admin access required",
                "your_role": role
            }), 403
            
        return fn(*args, **kwargs)
    return wrapper

def operator_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        
        # Robust role check: handles both nested 'sub' and direct 'role' claims
        sub_data = claims.get("sub", {})
        role = sub_data.get("role") if isinstance(sub_data, dict) else claims.get("role")

        if not role or role.upper() not in ["ADMIN", "OPERATOR"]:
            return jsonify({
                "msg": "Forbidden: Insufficient permissions",
                "your_role": role
            }), 403
            
        return fn(*args, **kwargs)
    return wrapper

