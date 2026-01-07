"""
Flask application factory
File: backend/app.py
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import config
from models.models import db


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config.get(config_name, config["default"]))

    # Initialize extensions
    db.init_app(app)
    CORS(app)
    JWTManager(app)

    # Register blueprints
    from routes.test_routes import test_bp
    app.register_blueprint(test_bp, url_prefix="/api")

    # Health check
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify(
            status="healthy",
            message="Toll Tracker API is running"
        ), 200

    # Root endpoint
    @app.route("/", methods=["GET"])
    def index():
        return jsonify(
            name="Automated Route Toll & Payment Tracker API",
            version="1.0.0",
            status="active"
        ), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)

