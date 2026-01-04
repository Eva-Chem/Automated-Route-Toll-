from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from db.database import init_db

# Import Blueprints
from routes.auth_routes import auth_bp
from routes.mpesa_routes import mpesa_bp
from routes.toll_zones import toll_zones_bp
from routes.check_zone import check_zone_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app)

    # JWT Configuration
    jwt = JWTManager(app)

    # --- JWT FIX: Handles dictionary identity in your current token ---
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        # If user is a dict (like in your token), return the ID as a string
        if isinstance(user, dict):
            return str(user.get("id"))
        return str(user)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        # Returns the full dictionary so middleware can see the 'role'
        return jwt_data["sub"]

    # Initialize database with SQLAlchemy
    init_db(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(mpesa_bp, url_prefix="/api/mpesa")
    app.register_blueprint(toll_zones_bp, url_prefix="/api/toll-zones")
    app.register_blueprint(check_zone_bp, url_prefix="/api")

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

