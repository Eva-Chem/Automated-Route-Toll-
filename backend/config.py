import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "super-secret-key-change-this"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/toll_tracker"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
