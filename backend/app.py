"""
Main Application Entry Point
File: backend/app.py
"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from models.models import db
import os

from routes.driver_toll_zones import driver_toll_zones_bp
from routes.payments import payments_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config["default"]))

    db.init_app(app)
    JWTManager(app)
    CORS(app)

    # Register routes
    app.register_blueprint(driver_toll_zones_bp)
    app.register_blueprint(payments_bp)

    @app.route("/health", methods=["GET"])
    def health_check():
        return {
            "status": "healthy",
            "message": "Toll Tracker API is running"
        }, 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
