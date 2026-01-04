import psycopg2
import os
from flask_sqlalchemy import SQLAlchemy

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:Group5@localhost:5432/toll_tracker"
)

db = SQLAlchemy()

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db(app):
    """Initialize database with SQLAlchemy"""
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        # Create all tables defined in models
        from models.toll_zone import TollZone, TollPayment
        db.create_all()
        
        # Insert sample data if table is empty
        if TollZone.query.count() == 0:
            sample_zone = TollZone(
                name='CBD Toll Zone',
                charge_amount=200,
                polygon_coords=[
                    {"lat": -1.2921, "lng": 36.8219},
                    {"lat": -1.2925, "lng": 36.8225},
                    {"lat": -1.2930, "lng": 36.8220},
                    {"lat": -1.2921, "lng": 36.8219}
                ]
            )
            db.session.add(sample_zone)
            db.session.commit()

