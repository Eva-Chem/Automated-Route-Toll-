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
from routes.payment_routes import payment_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app)

    # JWT Configuration
    jwt = JWTManager(app)

    # JWT Identity Fix
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        if isinstance(user, dict):
            return str(user.get("id"))
        return str(user)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        return jwt_data["sub"]

    # Initialize Database
    init_db(app)

    # -----------------------------
    # HEALTH CHECK (REQUIRED)
    # -----------------------------
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "healthy",
            "message": "Toll Tracker API is running"
        }), 200

    # Root route (optional)
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "message": "Automated Route Toll API",
            "status": "Running"
        }), 200

    # -----------------------------
    # Register Blueprints
    # -----------------------------
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(mpesa_bp, url_prefix="/api/mpesa")
    app.register_blueprint(toll_zones_bp, url_prefix="/api/toll-zones")
    app.register_blueprint(check_zone_bp, url_prefix="/api")
    app.register_blueprint(payment_bp, url_prefix="/api")

    return app


# IMPORTANT: gunicorn looks for this
app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
