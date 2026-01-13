from app import create_app
from models.models import db, TollPaid, TollZone, User
from datetime import datetime
import uuid

app = create_app()

with app.app_context():
    # Get any toll zone
    zone = TollZone.query.first()
    if not zone:
        print("❌ No toll zones found. Seed zones first.")
        exit()

    # Get or create an admin user
    admin = User.query.filter_by(role="ADMIN").first()
    if not admin:
        admin = User(
            user_id=uuid.uuid4(),
            email="admin@example.com",
            password_hash="dev",
            phone_number="0700000000",
            role="ADMIN"
        )
        db.session.add(admin)
        db.session.commit()

    # Create fake toll payments
    payments = [
        TollPaid(
            id=uuid.uuid4(),
            zone_id=zone.zone_id,
            driver_id=admin.user_id,
            amount=500,
            phone_number="0700000000",
            status="Completed",
            created_at=datetime.utcnow()
        ),
        TollPaid(
            id=uuid.uuid4(),
            zone_id=zone.zone_id,
            driver_id=admin.user_id,
            amount=300,
            phone_number="0700000000",
            status="Pending",
            created_at=datetime.utcnow()
        ),
        TollPaid(
            id=uuid.uuid4(),
            zone_id=zone.zone_id,
            driver_id=admin.user_id,
            amount=700,
            phone_number="0700000000",
            status="Failed",
            created_at=datetime.utcnow()
        )
    ]

    db.session.add_all(payments)
    db.session.commit()

    print("✅ Seeded sample toll transactions successfully.")
