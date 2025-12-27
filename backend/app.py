from flask import Flask, jsonify
from flask_cors import CORS
import logging

# Import blueprints
from routes.toll_zones import toll_zones_bp
from routes.check_zone import check_zone_bp
from routes.mpesa_routes import mpesa_bp

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Enable CORS for frontend
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(toll_zones_bp)
    app.register_blueprint(check_zone_bp)
    app.register_blueprint(mpesa_bp)
    
    # Root endpoint
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "message": "Automated Route Toll API",
            "version": "1.0.0",
            "endpoints": {
                "health": "/api/health",
                "stk_push": "/payments/stk-push",
                "c2b_simulate": "/payments/c2b/simulate"
            }
        }), 200
    
    # Health check
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "ok",
            "message": "Backend running"
        }), 200
    
    logger.info("✅ Flask app initialized successfully")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)