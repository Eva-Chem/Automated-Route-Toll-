"""
Database configuration for Flask application
File: backend/config.py
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration"""
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://localhost/toll_tracker'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('FLASK_ENV') == 'development'
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # M-Pesa Configuration
    MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY')
    MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET')
    MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE')
    MPESA_PASSKEY = os.getenv('MPESA_PASSKEY')
    MPESA_CALLBACK_URL = os.getenv('MPESA_CALLBACK_URL')
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/toll_tracker_test'


# Configuration dictionary - THIS IS THE IMPORTANT PART!
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


# Helper function to get current config
def get_config(config_name=None):
    """Get configuration based on environment"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    return config.get(config_name, config['default'])
