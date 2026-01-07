"""
Flask application factory
File: backend/app.py
"""

from dotenv import load_dotenv
load_dotenv()  # MUST be first

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
    app.config.from_object(config.get(config_name, config["default"]))

    # Initialize extensions
    db.init_app(app)
    CORS(app)
    JWTManager(app)

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.toll_zones import toll_zones_bp
    from routes.check_zone import check_zone_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(toll_zones_bp, url_prefix="/api")
    app.register_blueprint(check_zone_bp, url_prefix="/api")

    # Health check
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify(
            status="healthy",
            message="Toll Tracker API is running"
        ), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

