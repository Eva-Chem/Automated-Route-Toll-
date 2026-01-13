"""
Main Application Entry Point
File: backend/app.py
"""

import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import config
from models.models import db
from flask_migrate import Migrate



def create_app(config_name=None):
    """Application factory pattern"""

    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config["default"]))

    # -------------------------
    # Initialize extensions
    # -------------------------
    CORS(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    JWTManager(app)

    # -------------------------
    # Register Blueprints
    # -------------------------
    from routes.test_routes import test_bp
    from routes.toll_zones import toll_zones_bp
    from routes.geo_fencing_routes import geo_fencing_bp
    from routes.tolls_history import tolls_history_bp
    from routes.dev_auth import dev_auth_bp

    app.register_blueprint(test_bp, url_prefix="/api")
    app.register_blueprint(toll_zones_bp, url_prefix="/api")
    app.register_blueprint(geo_fencing_bp, url_prefix="/api")
    app.register_blueprint(tolls_history_bp, url_prefix="/api")
    app.register_blueprint(dev_auth_bp, url_prefix="/api")

    # -------------------------
    # Health & Root
    # -------------------------
    @app.route("/health", methods=["GET"])
    def health():
        return {"status": "healthy"}, 200

    @app.route("/", methods=["GET"])
    def index():
        return {
            "status": "online",
            "message": "Automated Route Toll API running"
        }, 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
