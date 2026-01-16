"""
Main Application Entry Point
File: backend/app.py
"""

import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from db.database import db
from routes.auth_routes import auth_bp
from routes.check_zone import check_zone_bp
import os

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    # Configuration: Use SQLite as a fallback for local testing/pytest
    if test_config is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///toll_system.db')
    else:
        app.config.update(test_config)
        
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_super_secret_key')

    # Initialize extensions with the app context
    db.init_app(app)
    JWTManager(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(check_zone_bp, url_prefix='/api')

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({"message": "Automated Route Toll API", "version": "1.0.0"}), 200

    return app

# This instance is used by Gunicorn/Production
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
