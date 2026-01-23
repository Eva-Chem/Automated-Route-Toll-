from flask import Flask, jsonify
from flask_cors import CORS
from routes.toll_zones import toll_zones_bp
from routes.auth import auth_bp

def create_app():
    app = Flask(__name__)

    # Enable CORS for frontend communication
    CORS(app)

    # Register routes
    app.register_blueprint(auth_bp)
    app.register_blueprint(toll_zones_bp)

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
    app.run(host="127.0.0.1", port=5000, debug=True)
