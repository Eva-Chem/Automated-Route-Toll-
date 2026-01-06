import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-secret-jwt-key-change-in-prod")

    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-flask-secret-key-change-in-prod")
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")

    # CORS
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

    # M-Pesa placeholders
    MPESA_CONSUMER_KEY = os.environ.get("MPESA_CONSUMER_KEY", "")
    MPESA_CONSUMER_SECRET = os.environ.get("MPESA_CONSUMER_SECRET", "")
    MPESA_SHORTCODE = os.environ.get("MPESA_SHORTCODE", "")
    MPESA_PASSKEY = os.environ.get("MPESA_PASSKEY", "")
    MPESA_CALLBACK_URL = os.environ.get("MPESA_CALLBACK_URL", "")
