from flask import Flask, jsonify
from flask_cors import CORS
from routes.toll_zones import toll_zones_bp
from routes.check_zone import check_zone_bp
from routes.mpesa_routes import mpesa_bp
from services.config import MpesaConfig
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)

    # Enable CORS for frontend communication
    CORS(app)

    # Validate M-Pesa configuration
    try:
        MpesaConfig.validate()
        logger.info("✅ M-Pesa configuration validated")
    except ValueError as e:
        logger.error(f"❌ M-Pesa configuration error: {str(e)}")

    # Register routes
    app.register_blueprint(toll_zones_bp)
    app.register_blueprint(check_zone_bp)
    app.register_blueprint(mpesa_bp)

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "message": "Automated Route Toll API",
            "endpoints": {
                "health": "/api/health",
                "payments_token": "/payments/access-token",
                "register_urls": "/payments/register-urls"
            }
        }), 200
    
    # Health check route
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