"""
Main Application Entry Point
File: backend/app.py
"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .config import config
from models.models import db
import os


def create_app(config_name=None):

    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config["default"]))

    # Enable CORS
    CORS(app)

    # Init extensions
    db.init_app(app)
    JWTManager(app)

    # -------------------------
    # Register Blueprints
    # -------------------------
    from routes.test_routes import test_bp
    from routes.toll_zones import toll_zones_bp
    from routes.geo_fencing_routes import geo_fencing_bp

    app.register_blueprint(test_bp, url_prefix="/api")
    app.register_blueprint(toll_zones_bp, url_prefix="/api")
    app.register_blueprint(geo_fencing_bp, url_prefix="/api")

    # -------------------------
    # Health & Root
    # -------------------------
    @app.route("/health")
    def health():
        return {"status": "healthy"}, 200

    @app.route("/")
    def index():
        return {
            "status": "online",
            "message": "Automated Route Toll API running"
        }, 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)