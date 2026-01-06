"""
Input validation utilities for the Toll Management System
"""

import re
from datetime import datetime
from email_validator import validate_email, EmailNotValidError


class ValidationError(Exception):
    """Custom validation error"""
    def __init__(self, message, field=None):
        self.message = message
        self.field = field
        super().__init__(message)


class Validators:
    """Collection of validation methods"""
    
    @staticmethod
    def validate_username(username, min_length=3, max_length=80):
        """Validate username"""
        if not username:
            raise ValidationError('Username is required', 'username')
        
        if len(username) < min_length:
            raise ValidationError(f'Username must be at least {min_length} characters', 'username')
        
        if len(username) > max_length:
            raise ValidationError(f'Username must be at most {max_length} characters', 'username')
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError('Username can only contain letters, numbers, and underscores', 'username')
        
        return True
    
    @staticmethod
    def validate_email(email):
        """Validate email address"""
        if not email:
            raise ValidationError('Email is required', 'email')
        
        try:
            valid = validate_email(email)
            return valid.email
        except EmailNotValidError as e:
            raise ValidationError(str(e), 'email')
    
    @staticmethod
    def validate_password(password, min_length=8):
        """Validate password strength"""
        if not password:
            raise ValidationError('Password is required', 'password')
        
        if len(password) < min_length:
            raise ValidationError(f'Password must be at least {min_length} characters', 'password')
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter', 'password')
        
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter', 'password')
        
        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one number', 'password')
        
        return True
    
    @staticmethod
    def validate_phone_number(phone_number):
        """Validate phone number (Kenyan format)"""
        if not phone_number:
            raise ValidationError('Phone number is required', 'phone_number')
        
        cleaned = re.sub(r'[\s\-\(\)]', '', phone_number)
        
        if re.match(r'^07\d{8}$', cleaned):
            return cleaned
        elif re.match(r'^254\d{9}$', cleaned):
            return cleaned
        else:
            raise ValidationError('Invalid phone number format. Use 07XXXXXXXX or 254XXXXXXXXX', 'phone_number')
    
    @staticmethod
    def validate_plate_number(plate_number):
        """Validate vehicle plate number"""
        if not plate_number:
            raise ValidationError('Plate number is required', 'plate_number')
        
        pattern = r'^[K][A-Z]{2}\s?\d{3,4}[A-Z]?$'
        
        if re.match(pattern, plate_number.upper()):
            return plate_number.upper()
        else:
            raise ValidationError('Invalid plate number format', 'plate_number')
    
    @staticmethod
    def validate_coordinates(latitude, longitude):
        """Validate geographic coordinates"""
        try:
            lat = float(latitude)
            lon = float(longitude)
        except (ValueError, TypeError):
            raise ValidationError('Invalid coordinate format', 'coordinates')
        
        if not -90 <= lat <= 90:
            raise ValidationError('Latitude must be between -90 and 90', 'latitude')
        
        if not -180 <= lon <= 180:
            raise ValidationError('Longitude must be between -180 and 180', 'longitude')
        
        return True
    
    @staticmethod
    def validate_amount(amount, min_amount=0):
        """Validate monetary amount"""
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            raise ValidationError('Invalid amount format', 'amount')
        
        if amount < min_amount:
            raise ValidationError(f'Amount must be at least {min_amount}', 'amount')
        
        return amount
    
    @staticmethod
    def sanitize_string(value, max_length=None):
        """Sanitize string input"""
        if value is None:
            return None
        
        sanitized = re.sub(r'<[^>]*>', '', str(value))
        sanitized = ' '.join(sanitized.split())
        
        if max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized

