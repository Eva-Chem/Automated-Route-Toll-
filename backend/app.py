from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from db import init_db

from routes.auth_routes import auth_bp
from routes.mpesa_routes import mpesa_bp
from routes.toll_zones import toll_zones_bp
from routes.check_zone import check_zone_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app)

    # JWT configuration
    JWTManager(app)

    # Initialize database
    init_db(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(mpesa_bp, url_prefix="/api/mpesa")
    app.register_blueprint(toll_zones_bp, url_prefix="/api/toll-zones")
    app.register_blueprint(check_zone_bp, url_prefix="/api/check-zone")

    # Root route
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "message": "Automated Route Toll API",
            "version": "1.0.0"
        }), 200

    # Health check
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "ok",
            "message": "Backend running"
        }), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
