# backend/db/database.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

        # Seed sample toll zones if empty
        from models.models import TollZone, User
        if not TollZone.query.first():
            cbd = TollZone(
                name="Nairobi CBD",
                charge_amount=20000,
                polygon_coords=[
                    {"lat": -1.2820, "lng": 36.8140},
                    {"lat": -1.2950, "lng": 36.8140},
                    {"lat": -1.2950, "lng": 36.8300},
                    {"lat": -1.2820, "lng": 36.8300}
                ]
            )
            thika = TollZone(
                name="Thika Road",
                charge_amount=15000,
                polygon_coords=[
                    {"lat": -1.2000, "lng": 36.8900},
                    {"lat": -1.2100, "lng": 36.9000},
                    {"lat": -1.2200, "lng": 36.8800},
                    {"lat": -1.2100, "lng": 36.8700}
                ]
            )
            db.session.add_all([cbd, thika])

        # Seed default admin/operator
        if not User.query.first():
            admin = User(username="admin", role="ADMIN")
            admin.set_password("Group5")
            operator = User(username="operator", role="OPERATOR")
            operator.set_password("Group5")
            db.session.add_all([admin, operator])

        db.session.commit()
        print("✅ Database initialized and sample data added")
