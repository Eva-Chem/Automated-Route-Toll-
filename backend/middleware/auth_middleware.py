"""
Role-Based Authorization Middleware
File: backend/middleware/auth_middleware.py
Task: SCRUM-33 - Role-Based Authorization Middleware

This middleware handles:
- JWT token validation
- Role-based access control
- Route protection (@admin_required, @operator_required, @driver_required)
"""

from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from models.models import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def token_required(f):
    """
    Decorator to require valid JWT token.
    Use this as the base decorator before role-specific decorators.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Token validation failed: {str(e)}")
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Valid authentication token required'
            }), 401
    
    return decorated_function


def get_current_user():
    """
    Get the current authenticated user from JWT token.
    
    Returns:
        User: User object or None
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            return None
        
        user = User.query.filter_by(user_id=user_id).first()
        return user
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        return None


def admin_required(f):
    """
    Decorator to restrict access to ADMIN role only.
    
    Usage:
        @app.route('/admin/dashboard')
        @admin_required
        def admin_dashboard():
            return {'message': 'Admin dashboard'}
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            
            user = get_current_user()
            
            if not user:
                logger.warning("Admin access attempted with invalid user")
                return jsonify({
                    'error': 'Forbidden',
                    'message': 'User not found'
                }), 403
            
            if not user.is_active:
                logger.warning(f"Admin access attempted by inactive user: {user.email}")
                return jsonify({
                    'error': 'Forbidden',
                    'message': 'User account is inactive'
                }), 403
            
            if user.role != 'ADMIN':
                logger.warning(f"Admin access denied for user: {user.email} (role: {user.role})")
                return jsonify({
                    'error': 'Forbidden',
                    'message': 'Admin access required. You do not have permission to access this resource.'
                }), 403
            
            logger.info(f"Admin access granted to: {user.email}")
            return f(*args, **kwargs)
            
        except Exception as e:
            logger.error(f"Admin authorization failed: {str(e)}")
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Authentication required'
            }), 401
    
    return decorated_function


def operator_required(f):
    """
    Decorator to restrict access to OPERATOR and ADMIN roles.
    
    Usage:
        @app.route('/operator/zones')
        @operator_required
        def manage_zones():
            return {'message': 'Toll zone management'}
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            
            user = get_current_user()
            
            if not user:
                logger.warning("Operator access attempted with invalid user")
                return jsonify({
                    'error': 'Forbidden',
                    'message': 'User not found'
                }), 403
            
            if not user.is_active:
                logger.warning(f"Operator access attempted by inactive user: {user.email}")
                return jsonify({
                    'error': 'Forbidden',
                    'message': 'User account is inactive'
                }), 403
            
            if user.role not in ['OPERATOR', 'ADMIN']:
                logger.warning(f"Operator access denied for user: {user.email} (role: {user.role})")
                return jsonify({
                    'error': 'Forbidden',
                    'message': 'Operator or Admin access required. You do not have permission to access this resource.'
                }), 403
            
            logger.info(f"Operator access granted to: {user.email} (role: {user.role})")
            return f(*args, **kwargs)
            
        except Exception as e:
            logger.error(f"Operator authorization failed: {str(e)}")
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Authentication required'
            }), 401
    
    return decorated_function


def driver_required(f):
    """
    Decorator to restrict access to DRIVER role (and optionally ADMIN for testing).
    
    Usage:
        @app.route('/driver/location')
        @driver_required
        def update_location():
            return {'message': 'Location updated'}
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            
            user = get_current_user()
            
            if not user:
                logger.warning("Driver access attempted with invalid user")
                return jsonify({
                    'error': 'Forbidden',
                    'message': 'User not found'
                }), 403
            
            if not user.is_active:
                logger.warning(f"Driver access attempted by inactive user: {user.email}")
                return jsonify({
                    'error': 'Forbidden',
                    'message': 'User account is inactive'
                }), 403
            
            if user.role not in ['DRIVER', 'ADMIN']:
                logger.warning(f"Driver access denied for user: {user.email} (role: {user.role})")
                return jsonify({
                    'error': 'Forbidden',
                    'message': 'Driver access required. You do not have permission to access this resource.'
                }), 403
            
            logger.info(f"Driver access granted to: {user.email}")
            return f(*args, **kwargs)
            
        except Exception as e:
            logger.error(f"Driver authorization failed: {str(e)}")
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Authentication required'
            }), 401
    
    return decorated_function


def role_required(allowed_roles):
    """
    Flexible decorator to allow multiple specific roles.
    
    Usage:
        @app.route('/special-endpoint')
        @role_required(['ADMIN', 'OPERATOR'])
        def special_function():
            return {'message': 'Special access'}
    
    Args:
        allowed_roles (list): List of role strings that are allowed
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                
                user = get_current_user()
                
                if not user:
                    return jsonify({
                        'error': 'Forbidden',
                        'message': 'User not found'
                    }), 403
                
                if not user.is_active:
                    return jsonify({
                        'error': 'Forbidden',
                        'message': 'User account is inactive'
                    }), 403
                
                if user.role not in allowed_roles:
                    logger.warning(f"Access denied for user: {user.email} (role: {user.role}, required: {allowed_roles})")
                    return jsonify({
                        'error': 'Forbidden',
                        'message': f'Access restricted to: {", ".join(allowed_roles)}'
                    }), 403
                
                logger.info(f"Access granted to: {user.email} (role: {user.role})")
                return f(*args, **kwargs)
                
            except Exception as e:
                logger.error(f"Authorization failed: {str(e)}")
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'Authentication required'
                }), 401
        
        return decorated_function
    return decorator