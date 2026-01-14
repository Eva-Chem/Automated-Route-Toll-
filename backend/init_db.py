"""
Database Initialization and Seeding Script
File: backend/init_db.py
Task: SCRUM-20 - Toll Zone Data Model

Usage:
    python init_db.py           # Initialize and seed
    python init_db.py init      # Just create tables
    python init_db.py seed      # Just seed data
    python init_db.py reset     # Drop, recreate, and seed
"""

from app import create_app
from models.models import db, User, TollZone, TollPaid, TollEntry
from werkzeug.security import generate_password_hash


def init_database():
    """Initialize database with tables"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("🗄️  INITIALIZING DATABASE")
        print("=" * 60)
        print("\n📋 Creating tables...")
        
        db.create_all()
        
        print("✅ Database tables created successfully!")
        print("\nTables created: users, toll_zones, tolls_paid, toll_entries")
        print("=" * 60)


def seed_sample_data():
    """Seed database with sample data for testing"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "=" * 60)
        print("🌱 SEEDING SAMPLE DATA")
        print("=" * 60)
        
        # ----------------------------
        # Sample users
        # ----------------------------
        users_data = [
            {'email': 'admin@toll.com', 'password': 'admin123', 'phone': '254712345678', 'role': 'ADMIN'},
            {'email': 'operator@toll.com', 'password': 'operator123', 'phone': '254723456789', 'role': 'OPERATOR'},
            {'email': 'driver1@toll.com', 'password': 'driver123', 'phone': '254734567890', 'role': 'DRIVER'},
            {'email': 'driver2@toll.com', 'password': 'driver123', 'phone': '254745678901', 'role': 'DRIVER'}
        ]
        
        created_users = []
        for udata in users_data:
            existing = User.query.filter_by(email=udata['email']).first()
            if existing:
                created_users.append(existing)
                continue
            user = User(
                email=udata['email'],
                password_hash=generate_password_hash(udata['password']),
                phone_number=udata['phone'],
                role=udata['role'],
                is_active=True
            )
            db.session.add(user)
            created_users.append(user)
        db.session.commit()
        
        # ----------------------------
        # Sample toll zones
        # ----------------------------
        operator = next((u for u in created_users if u.role == 'OPERATOR'), None)
        zones_data = [
            {'name': 'Thika Road Toll', 'charge': 5000, 'coords': [
                {'lat': -1.2195, 'lng': 36.8869},
                {'lat': -1.2195, 'lng': 36.8919},
                {'lat': -1.2145, 'lng': 36.8919},
                {'lat': -1.2145, 'lng': 36.8869},
                {'lat': -1.2195, 'lng': 36.8869}
            ]},
            {'name': 'Mombasa Road Toll', 'charge': 7500, 'coords': [
                {'lat': -1.3195, 'lng': 36.9269},
                {'lat': -1.3195, 'lng': 36.9319},
                {'lat': -1.3145, 'lng': 36.9319},
                {'lat': -1.3145, 'lng': 36.9269},
                {'lat': -1.3195, 'lng': 36.9269}
            ]},
            {'name': 'Nairobi-Nakuru Toll', 'charge': 10000, 'coords': [
                {'lat': -1.0195, 'lng': 36.7869},
                {'lat': -1.0195, 'lng': 36.7919},
                {'lat': -1.0145, 'lng': 36.7919},
                {'lat': -1.0145, 'lng': 36.7869},
                {'lat': -1.0195, 'lng': 36.7869}
            ]}
        ]
        
        created_zones = []
        for zdata in zones_data:
            existing = TollZone.query.filter_by(zone_name=zdata['name']).first()
            if existing:
                created_zones.append(existing)
                continue
            zone = TollZone(
                zone_name=zdata['name'],
                charge_amount=zdata['charge'],
                polygon_coords=zdata['coords'],
                is_active=True,
                created_by=operator.user_id if operator else None
            )
            db.session.add(zone)
            created_zones.append(zone)
        db.session.commit()
        
        # ----------------------------
        # Sample payments
        # ----------------------------
        drivers = [u for u in created_users if u.role == 'DRIVER']
        if drivers and created_zones:
            payments_data = [
                {'zone': created_zones[0], 'driver': drivers[0], 'status': 'Completed', 'checkout_id': 'ws_CO_DMZ_123'},
                {'zone': created_zones[1], 'driver': drivers[1] if len(drivers)>1 else drivers[0], 'status': 'Completed', 'checkout_id': 'ws_CO_DMZ_987'},
                {'zone': created_zones[2] if len(created_zones)>2 else created_zones[0], 'driver': drivers[0], 'status': 'Pending', 'checkout_id': None}
            ]
            for pd in payments_data:
                payment = TollPaid(
                    zone_id=pd['zone'].zone_id,
                    driver_id=pd['driver'].user_id,
                    amount=pd['zone'].charge_amount,
                    phone_number=pd['driver'].phone_number,
                    checkout_request_id=pd['checkout_id'],
                    status=pd['status']
                )
                db.session.add(payment)
            db.session.commit()
        
        # ----------------------------
        # Sample toll entries
        # ----------------------------
        if drivers and created_zones:
            for i, driver in enumerate(drivers):
                zone = created_zones[i % len(created_zones)]
                existing_entry = TollEntry.query.filter_by(driver_id=driver.user_id, zone_id=zone.zone_id).first()
                if existing_entry:
                    continue
                payment = TollPaid.query.filter_by(driver_id=driver.user_id, zone_id=zone.zone_id).first()
                entry = TollEntry(
                    driver_id=driver.user_id,
                    zone_id=zone.zone_id,
                    payment_id=payment.id if payment else None
                )
                db.session.add(entry)
            db.session.commit()
        
        print("\n✅ Database seeding complete!")


def drop_all_tables():
    """Drop all tables (use with caution!)"""
    app = create_app()
    
    with app.app_context():
        confirm = input("Type 'DELETE' to drop all tables: ")
        if confirm == 'DELETE':
            db.drop_all()
            print("✅ All tables dropped!")
        else:
            print("❌ Operation cancelled.")


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == 'init':
            init_database()
        elif cmd == 'seed':
            seed_sample_data()
        elif cmd == 'reset':
            drop_all_tables()
            init_database()
            seed_sample_data()
        elif cmd == 'drop':
            drop_all_tables()
        else:
            print("Usage: python init_db.py [init|seed|reset|drop]")
    else:
        # default
        init_database()
        seed_sample_data()
