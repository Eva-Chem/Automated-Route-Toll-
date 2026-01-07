"""
Flask application factory
File: backend/app.py
"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
<<<<<<< HEAD

from routes.toll_zones import toll_zones_bp
from routes.check_zone import check_zone_bp
from routes.mpesa_routes import mpesa_bp
from routes.auth_routes import auth_bp

=======
from config import config
from models.models import db
import os

>>>>>>> riyan-backend

def create_app(config_name=None):
    """
    Application factory pattern
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
<<<<<<< HEAD

    # JWT config
    app.config.from_object("config")
    JWTManager(app)

    # Enable CORS
    CORS(app)

    # Register blueprints
    app.register_blueprint(toll_zones_bp)
    app.register_blueprint(check_zone_bp)
    app.register_blueprint(mpesa_bp)
    app.register_blueprint(auth_bp)

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "message": "Automated Route Toll API",
            "version": "1.0.0"
        }), 200

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "ok", "message": "Backend running"}), 200

    return app



app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
=======
    
    # Load configuration
    app.config.from_object(config.get(config_name, config['default']))
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    jwt = JWTManager(app)
    
    # Register blueprints
    from routes.test_routes import test_bp
    app.register_blueprint(test_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy', 'message': 'Toll Tracker API is running'}, 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def index():
        return {
            'name': 'Automated Route Toll & Payment Tracker API',
            'version': '1.0.0',
            'status': 'active'
        }, 200
    
    return app


# This allows running the app directly with `python app.py`
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
>>>>>>> riyan-backend
