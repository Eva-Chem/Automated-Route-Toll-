import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Seed the Nairobi CBD Toll Zone if the table is empty
        from models.toll_zone import TollZone
        if not TollZone.query.first():
            cbd_zone = TollZone(
                name="Nairobi CBD",
                polygon_coords=[
                    {"lat": -1.2820, "lng": 36.8140},
                    {"lat": -1.2950, "lng": 36.8140},
                    {"lat": -1.2950, "lng": 36.8300},
                    {"lat": -1.2820, "lng": 36.8300}
                ],
                charge_amount=200.00
            )
            db.session.add(cbd_zone)
            db.session.commit()
            print("✅ Database seeded with Nairobi CBD Toll Zone")