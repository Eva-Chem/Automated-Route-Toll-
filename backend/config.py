import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "super-secret-key-change-this"
    )

    # Use Render database URL in production, local for development
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/toll_tracker"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Base URL for the deployed API (Render)
API_BASE_URL = "https://automated-route-toll.onrender.com"
