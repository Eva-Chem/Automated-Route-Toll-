"""
Main Application Entry Point
File: backend/app.py
"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

# Import our shared database instance and config logic
from models.models import db
from config import get_config

def create_app(config_name=None):
    """
    Application factory to create and configure the Flask app.
    """
    app = Flask(__name__)

    # 1. Load Configuration from config.py
    # This ensures SQLALCHEMY_DATABASE_URI is set correctly
    env_config = get_config(config_name)
    app.config.from_object(env_config)

    # 2. Initialize Extensions
    db.init_app(app)
    
    jwt = JWTManager(app)
    
    # Enable CORS for frontend connectivity
    CORS(app, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS', '*')}})

    # 3. Register Blueprints
    # We use url_prefix='/api' so your routes match http://127.0.0.1:5000/api/test/...
    from routes.test_routes import test_bp
    app.register_blueprint(test_bp, url_prefix='/api')

    # Root route for quick health check
    @app.route('/')
    def index():
        return {
            "status": "online",
            "message": "Automated Route Toll API is running",
            "environment": os.getenv('FLASK_ENV', 'development')
        }, 200

    return app

# Create the final app object
app = create_app()

# This block is CRITICAL. It keeps the terminal open and listens for requests.
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 TOLL TRACKER SERVER STARTING")
    print("="*50)
    print(f"📍 URL: http://127.0.0.1:5000")
    print(f"🛠️  Debug Mode: ON")
    print("="*50 + "\n")
    
    # host='0.0.0.0' allows external connections (like from your phone or Windows browser)
    app.run(host='0.0.0.0', port=5000, debug=True)