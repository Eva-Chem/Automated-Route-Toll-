# backend/db/database.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models here to register them with SQLAlchemy
    # This must happen after db.init_app() but before create_all()
    from db import models
    
    # Create tables in development/testing
    with app.app_context():
        db.create_all()
    
    return db