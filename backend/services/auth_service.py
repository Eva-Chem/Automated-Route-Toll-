# backend/services/auth_service.py
from werkzeug.security import check_password_hash
from db.models import User

def authenticate(username, password):
    """
    Authenticate a user by username and password
    
    Args:
        username: The username
        password: The plain text password
        
    Returns:
        User object if authentication succeeds, None otherwise
    """
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password_hash, password):
        return user
    
    return None