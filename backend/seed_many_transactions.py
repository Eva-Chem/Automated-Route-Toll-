from app import create_app
from models.models import db, TollPaid, TollZone, User
from datetime import datetime, timedelta
import uuid
import random

app = create_app()

STATUSES = ["Completed", "Pending", "Failed"]
AMOUNTS = [200, 300, 500, 700, 1000]

with app.app_context():
    zone = TollZone.query.all()
    if not zone:
        print("❌ No toll zones found. Create zones first.")
        exit()

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

    records = []

    for i in range(30): 
        payment = TollPaid(
            id=uuid.uuid4(),
            zone_id=zone.zone_id,
            driver_id=admin.user_id,
            amount=random.choice(AMOUNTS),
            phone_number="0700000000",
            status=random.choice(STATUSES),
            created_at=datetime.utcnow() - timedelta(minutes=i * 7)
        )
        records.append(payment)

    db.session.add_all(records)
    db.session.commit()

    print(f"✅ Seeded {len(records)} toll history records successfully.")
