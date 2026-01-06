"""
Database initialization and seeding
File: backend/init_db.py
"""

from dotenv import load_dotenv
load_dotenv()  # ✅ Load environment variables FIRST

from app import create_app
from models.models import db, TollZone, TollPaid


def init_database():
    """Create all database tables"""
    app = create_app()

    with app.app_context():
        print("🗄️ Creating database tables...")
        db.create_all()
        print("✅ Tables created successfully!")


def seed_sample_data():
    """Seed initial sample data"""
    app = create_app()

    with app.app_context():
        print("🌱 Checking for existing toll zones...")

        if TollZone.query.first():
            print("⚠️ Toll zones already exist. Skipping seeding.")
            return

        cbd_zone = TollZone(
            name="CBD Toll Zone",
            charge_amount=5000,
            polygon_coords=[
                {"lat": -1.286389, "lng": 36.817223},
                {"lat": -1.286389, "lng": 36.827223},
                {"lat": -1.276389, "lng": 36.827223},
                {"lat": -1.276389, "lng": 36.817223}
            ],
            is_active=True
        )

        db.session.add(cbd_zone)
        db.session.commit()

        print("✅ Sample toll zone seeded successfully!")


if __name__ == "__main__":
    init_database()
    seed_sample_data()
