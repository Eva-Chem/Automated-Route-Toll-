"""
Authentication service for user registration, login, and password management
"""

from models import db, User
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta


class AuthService:
    """Service class for authentication operations"""
    
    def register_user(self, username, email, password, phone_number=None):
        """
        Register a new user
        
        Args:
            username: Unique username
            email: Unique email address
            password: Plain text password
            phone_number: Optional phone number
            
        Returns:
            User object
            
        Raises:
            ValueError: If username or email already exists
        """
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            raise ValueError('Username already exists')
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            raise ValueError('Email already exists')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            phone_number=phone_number,
            role='user'  # Default role
        )
        
        # Set password
        user.set_password(password)
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        return user
    
    def authenticate_user(self, username, password):
        """
        Authenticate user with username and password
        
        Args:
            username: Username or email
            password: Plain text password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        # Try to find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user:
            return None
        
        if not user.check_password(password):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    def change_password(self, user, current_password, new_password):
        """
        Change user password
        
        Args:
            user: User object
            current_password: Current password
            new_password: New password
            
        Returns:
            True if password changed successfully, False otherwise
        """
        if not user.check_password(current_password):
            return False
        
        user.set_password(new_password)
        db.session.commit()
        
        return True
    
    def generate_tokens(self, user_id):
        """
        Generate access and refresh tokens for a user
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with access_token and refresh_token
        """
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    
    def verify_token(self, token):
        """
        Verify JWT token
        
        Args:
            token: JWT token string
            
        Returns:
            User ID if token valid, None otherwise
        """
        from flask_jwt_extended import jwt_required, get_jwt_identity
        try:
            # This will raise an exception if token is invalid
            return get_jwt_identity()
        except Exception:
            return None
    
    def get_user_by_id(self, user_id):
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User object or None
        """
        return User.query.get(user_id)
    
    def get_user_by_username(self, username):
        """
        Get user by username
        
        Args:
            username: Username
            
        Returns:
            User object or None
        """
        return User.query.filter_by(username=username).first()
    
    def get_user_by_email(self, email):
        """
        Get user by email
        
        Args:
            email: Email address
            
        Returns:
            User object or None
        """
        return User.query.filter_by(email=email).first()
    
    def update_user(self, user_id, **kwargs):
        """
        Update user fields
        
        Args:
            user_id: User ID
            **kwargs: Fields to update
            
        Returns:
            Updated User object or None
        """
        user = User.query.get(user_id)
        
        if not user:
            return None
        
        allowed_fields = ['username', 'email', 'phone_number', 'is_active']
        
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(user, key, value)
        
        db.session.commit()
        
        return user
    
    def deactivate_user(self, user_id):
        """
        Deactivate user account
        
        Args:
            user_id: User ID
            
        Returns:
            True if deactivated, False if user not found
        """
        user = User.query.get(user_id)
        
        if not user:
            return False
        
        user.is_active = False
        db.session.commit()
        
        return True
    
    def activate_user(self, user_id):
        """
        Activate user account
        
        Args:
            user_id: User ID
            
        Returns:
            True if activated, False if user not found
        """
        user = User.query.get(user_id)
        
        if not user:
            return False
        
        user.is_active = True
        db.session.commit()
        
        return True
    
    def update_user_role(self, user_id, new_role):
        """
        Update user role
        
        Args:
            user_id: User ID
            new_role: New role ('user', 'operator', 'admin')
            
        Returns:
            Updated User object or None
        """
        valid_roles = ['user', 'operator', 'admin']
        
        if new_role not in valid_roles:
            raise ValueError(f'Invalid role. Must be one of: {valid_roles}')
        
        user = User.query.get(user_id)
        
        if not user:
            return None
        
        user.role = new_role
        db.session.commit()
        
        return user

