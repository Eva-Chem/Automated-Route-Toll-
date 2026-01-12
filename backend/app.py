"""
Main Application Entry Point
File: backend/app.py
"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from models.models import db
import os


def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))
    
    db.init_app(app)
    
    jwt = JWTManager(app)
    
    # Register test routes
    from routes.test_routes import test_bp
    app.register_blueprint(test_bp, url_prefix='/api')
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy', 'message': 'Toll Tracker API is running'}, 200
    
    @app.route('/', methods=['GET'])
    def index():
        return {
            "status": "online",
            "message": "Automated Route Toll API is running",
            "environment": os.getenv('FLASK_ENV', 'development')
        }, 200

    return app

# Create the final app object
app = create_app()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
