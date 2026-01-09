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


def create_app(config_name=None):
    """Application factory pattern"""

    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config["default"]))

    # Enable CORS
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    JWTManager(app)

    # -------------------------
    # Register Blueprints
    # -------------------------
    from routes.test_routes import test_bp
    from routes.toll_zones import toll_zones_bp
    from routes.geo_fencing_routes import geo_fencing_bp
    

    app.register_blueprint(test_bp, url_prefix="/api")
    app.register_blueprint(toll_zones_bp)
    app.register_blueprint(geo_fencing_bp)
    

    # -------------------------
    # Health & Index
    # -------------------------
    @app.route("/health", methods=["GET"])
    def health_check():
        return {
            "status": "healthy",
            "message": "Toll Tracker API is running"
        }, 200

    @app.route("/", methods=["GET"])
    def index():
        return {
            "status": "online",
            "message": "Automated Route Toll API is running",
            "environment": os.getenv("FLASK_ENV", "development")
        }, 200

    return app


# Create app instance
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)     
