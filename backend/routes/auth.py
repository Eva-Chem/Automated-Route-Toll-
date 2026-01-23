"""
Authentication Routes Module
Handles user authentication and token generation
"""
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import jwt
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Secret key for JWT (in production, use environment variable)
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

# Mock user database - In production, use a real database
MOCK_USERS = {
    "admin": {
        "username": "admin",
        "password": "admin123",  # In production, use bcrypt hashing
        "name": "Administrator",
        "role": "admin",
        "email": "admin@tolls.com",
        "permissions": ["manage_zones", "view_transactions", "manage_operators", "view_reports"]
    },
    "operator": {
        "username": "operator",
        "password": "operator123",
        "name": "Toll Operator",
        "role": "operator",
        "email": "operator@tolls.com",
        "permissions": ["view_zones", "record_transaction"]
    }
}


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT token
    
    Request JSON:
    {
        "username": "admin",
        "password": "admin123"
    }
    
    Returns:
    {
        "success": true,
        "token": "jwt_token",
        "user": {
            "username": "admin",
            "name": "Administrator",
            "role": "admin",
            "email": "admin@tolls.com",
            "permissions": [...]
        },
        "expiresIn": 86400
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body required"
            }), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        # Validate input
        if not username or not password:
            return jsonify({
                "success": False,
                "error": "Username and password are required"
            }), 400
        
        # Find user
        user = MOCK_USERS.get(username)
        if not user or user['password'] != password:
            return jsonify({
                "success": False,
                "error": "Invalid username or password"
            }), 401
        
        # Generate JWT token
        payload = {
            'username': user['username'],
            'role': user['role'],
            'email': user['email'],
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        
        # Return user data (without password)
        user_data = {
            'username': user['username'],
            'name': user['name'],
            'role': user['role'],
            'email': user['email'],
            'permissions': user['permissions']
        }
        
        return jsonify({
            "success": True,
            "token": token,
            "user": user_data,
            "expiresIn": 86400  # 24 hours
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500


@auth_bp.route('/verify', methods=['POST'])
def verify_token():
    """
    Verify JWT token and return user info
    
    Headers:
    Authorization: Bearer <token>
    
    Returns:
    {
        "success": true,
        "user": {...},
        "valid": true
    }
    """
    try:
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return jsonify({
                "success": False,
                "valid": False,
                "error": "Missing or invalid token"
            }), 401
        
        token = auth_header.split(' ')[1]
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user = MOCK_USERS.get(payload['username'])
            
            if not user:
                return jsonify({
                    "success": False,
                    "valid": False,
                    "error": "User not found"
                }), 401
            
            user_data = {
                'username': user['username'],
                'name': user['name'],
                'role': user['role'],
                'email': user['email'],
                'permissions': user['permissions']
            }
            
            return jsonify({
                "success": True,
                "valid": True,
                "user": user_data
            }), 200
        
        except jwt.ExpiredSignatureError:
            return jsonify({
                "success": False,
                "valid": False,
                "error": "Token expired"
            }), 401
        
        except jwt.InvalidTokenError:
            return jsonify({
                "success": False,
                "valid": False,
                "error": "Invalid token"
            }), 401
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Logout user (invalidate token on client side)
    
    Returns:
    {
        "success": true,
        "message": "Logged out successfully"
    }
    """
    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    }), 200


@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """
    Get current user profile
    
    Headers:
    Authorization: Bearer <token>
    
    Returns user profile if token is valid
    """
    try:
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return jsonify({
                "success": False,
                "error": "Missing or invalid token"
            }), 401
        
        token = auth_header.split(' ')[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user = MOCK_USERS.get(payload['username'])
        
        if not user:
            return jsonify({
                "success": False,
                "error": "User not found"
            }), 404
        
        user_data = {
            'username': user['username'],
            'name': user['name'],
            'role': user['role'],
            'email': user['email'],
            'permissions': user['permissions']
        }
        
        return jsonify({
            "success": True,
            "user": user_data
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500
