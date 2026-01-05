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
                zone_id="cbd-zone-001",
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

            # Seed Thika Road Toll Zone
            thika_zone = TollZone(
                zone_id="thika-zone-001",
                name="Thika Road",
                polygon_coords=[
                    {"lat": -1.2000, "lng": 36.8900},
                    {"lat": -1.2100, "lng": 36.9000},
                    {"lat": -1.2200, "lng": 36.8800},
                    {"lat": -1.2100, "lng": 36.8700}
                ],
                charge_amount=150.00
            )
            db.session.add(thika_zone)

            db.session.commit()
            print("✅ Database seeded with Nairobi CBD and Thika Road Toll Zones")
