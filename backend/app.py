# backend/app.py
import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from db.database import db, init_db
from routes.auth_routes import auth_bp
from routes.mpesa_routes import mpesa_bp
from routes.geo_fencing_routes import geo_fencing_bp
from routes.toll_zones import toll_zones_bp
from routes.tolls_history import tolls_history_bp

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    # Configuration
    if test_config is None:
        # Get DATABASE_URL from environment
        database_url = os.getenv('DATABASE_URL')
        
        # Fix for Render's postgres:// vs postgresql:// issue
        if database_url and database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        
        # Use PostgreSQL from env or SQLite as fallback for local testing
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///toll_system.db'
    else:
        app.config.update(test_config)
    
    # Additional configs
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_super_secret_key')

    # Initialize database using the init_db function
    init_db(app)
    
    # Initialize JWT
    JWTManager(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(mpesa_bp)
    app.register_blueprint(geo_fencing_bp, url_prefix='/api/geo-fencing')
    app.register_blueprint(toll_zones_bp, url_prefix='/api')
    app.register_blueprint(tolls_history_bp, url_prefix='/api')
    
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({"message": "Automated Route Toll API", "version": "1.0.0"}), 200

    return app

# This instance is used by Gunicorn/Production
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)