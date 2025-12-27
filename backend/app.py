from flask import Flask, jsonify
from flask_cors import CORS

from routes.toll_zones import toll_zones_bp
from routes.check_zone import check_zone_bp
from routes.mpesa_routes import mpesa_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.register_blueprint(toll_zones_bp)
    app.register_blueprint(check_zone_bp)
    app.register_blueprint(mpesa_bp)
    
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
    
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "ok", "message": "Backend running"}), 200
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)