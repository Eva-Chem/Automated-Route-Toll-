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
        print("\nTables created:")
        print("  - users")
        print("  - toll_zones")
        print("  - tolls_paid")
        print("  - toll_entries")
        print("=" * 60)


def seed_sample_data():
    """Seed database with sample data for testing"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "=" * 60)
        print("🌱 SEEDING SAMPLE DATA")
        print("=" * 60)
        
        # Check if data already exists
        existing_users = User.query.count()
        if existing_users > 0:
            print(f"\n⚠️  Database already contains {existing_users} users.")
            response = input("Do you want to seed anyway? This may create duplicates. (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Seeding cancelled.")
                return
        
        # ----------------------------
        # Create sample users
        # ----------------------------
        print("\n👥 Creating sample users...")
        users_data = [
            {'email': 'admin@toll.com', 'password': 'admin123', 'phone': '254712345678', 'role': 'ADMIN'},
            {'email': 'operator@toll.com', 'password': 'operator123', 'phone': '254723456789', 'role': 'OPERATOR'},
            {'email': 'driver1@toll.com', 'password': 'driver123', 'phone': '254734567890', 'role': 'DRIVER'},
            {'email': 'driver2@toll.com', 'password': 'driver123', 'phone': '254745678901', 'role': 'DRIVER'}
        ]
        
        created_users = []
        for user_data in users_data:
            existing = User.query.filter_by(email=user_data['email']).first()
            if existing:
                print(f"   ⚠️  User {user_data['email']} already exists, skipping...")
                created_users.append(existing)
                continue
            
            user = User(
                email=user_data['email'],
                password_hash=generate_password_hash(user_data['password']),
                phone_number=user_data['phone'],
                role=user_data['role'],
                is_active=True
            )
            db.session.add(user)
            created_users.append(user)
            print(f"   ✅ Created: {user_data['email']} ({user_data['role']})")
        
        db.session.commit()
        print(f"\n✅ Total users in database: {User.query.count()}")
        
        # ----------------------------
        # Create sample toll zones
        # ----------------------------
        operator = next((u for u in created_users if u.role == 'OPERATOR'), None)
        print("\n🗺️  Creating sample toll zones...")
        zones_data = [
            {'name': 'Thika Road Toll', 'charge': 5000, 'coords': [[-1.2195,36.8869],[-1.2195,36.8919],[-1.2145,36.8919],[-1.2145,36.8869],[-1.2195,36.8869]]},
            {'name': 'Mombasa Road Toll', 'charge': 7500, 'coords': [[-1.3195,36.9269],[-1.3195,36.9319],[-1.3145,36.9319],[-1.3145,36.9269],[-1.3195,36.9269]]},
            {'name': 'Nairobi-Nakuru Toll', 'charge': 10000, 'coords': [[-1.0195,36.7869],[-1.0195,36.7919],[-1.0145,36.7919],[-1.0145,36.7869],[-1.0195,36.7869]]}
        ]
        
        created_zones = []
        for zone_data in zones_data:
            existing = TollZone.query.filter_by(zone_name=zone_data['name']).first()
            if existing:
                print(f"   ⚠️  Zone '{zone_data['name']}' already exists, skipping...")
                created_zones.append(existing)
                continue
            
            zone = TollZone(
                zone_name=zone_data['name'],
                charge_amount=zone_data['charge'],
                polygon_coords=zone_data['coords'],
                is_active=True,
                created_by=operator.user_id if operator else None
            )
            db.session.add(zone)
            created_zones.append(zone)
            print(f"   ✅ Created: {zone_data['name']} (KES {zone_data['charge']/100:.2f})")
        
        db.session.commit()
        print(f"\n✅ Total toll zones in database: {TollZone.query.count()}")
        
        # ----------------------------
        # Create sample payments
        # ----------------------------
        print("\n💰 Creating sample payment records...")
        drivers = [u for u in created_users if u.role == 'DRIVER']
        if drivers and created_zones:
            payments_data = [
                {'zone': created_zones[0], 'driver': drivers[0], 'status': 'Completed', 'checkout_id': 'ws_CO_DMZ_123456789_12345678901234567890'},
                {'zone': created_zones[1], 'driver': drivers[1] if len(drivers) > 1 else drivers[0], 'status': 'Completed', 'checkout_id': 'ws_CO_DMZ_987654321_09876543210987654321'},
                {'zone': created_zones[2] if len(created_zones) > 2 else created_zones[0], 'driver': drivers[0], 'status': 'Pending', 'checkout_id': None}
            ]
            for pd in payments_data:
                if pd['checkout_id']:
                    existing = TollPaid.query.filter_by(checkout_request_id=pd['checkout_id']).first()
                    if existing:
                        print(f"   ⚠️  Payment already exists, skipping...")
                        continue
                payment = TollPaid(
                    zone_id=pd['zone'].zone_id,
                    driver_id=pd['driver'].user_id,
                    amount=pd['zone'].charge_amount,
                    phone_number=pd['driver'].phone_number,
                    checkout_request_id=pd['checkout_id'],
                    status=pd['status']
                )
                db.session.add(payment)
                print(f"   ✅ Created: {pd['status']} payment for {pd['zone'].zone_name}")
            db.session.commit()
            print(f"\n✅ Total payments in database: {TollPaid.query.count()}")
        
        # ----------------------------
        # Create sample toll entries
        # ----------------------------
        print("\n🚪 Creating sample toll entries...")
        if drivers and created_zones and TollPaid.query.count() > 0:
            entries_data = [
                {'driver': drivers[0], 'zone': created_zones[0]},
                {'driver': drivers[1] if len(drivers) > 1 else drivers[0], 'zone': created_zones[1]}
            ]
            for ed in entries_data:
                payment = TollPaid.query.filter_by(driver_id=ed['driver'].user_id, zone_id=ed['zone'].zone_id).first()
                existing_entry = TollEntry.query.filter_by(driver_id=ed['driver'].user_id, zone_id=ed['zone'].zone_id).first()
                if existing_entry:
                    print(f"   ⚠️  Toll entry for {ed['driver'].email} in {ed['zone'].zone_name} already exists, skipping...")
                    continue
                entry = TollEntry(
                    driver_id=ed['driver'].user_id,
                    zone_id=ed['zone'].zone_id,
                    payment_id=payment.id if payment else None
                )
                db.session.add(entry)
                print(f"   ✅ Created toll entry for {ed['driver'].email} in {ed['zone'].zone_name}")
            db.session.commit()
            print(f"\n✅ Total toll entries in database: {TollEntry.query.count()}")
        
        # ----------------------------
        # Print summary
        # ----------------------------
        print("\n" + "=" * 60)
        print("✅ SEEDING COMPLETE!")
        print("=" * 60)
        print("\n📋 Test Credentials:")
        print("-" * 60)
        print("   ADMIN:\n     Email: admin@toll.com\n     Password: admin123\n")
        print("   OPERATOR:\n     Email: operator@toll.com\n     Password: operator123\n")
        print("   DRIVER 1:\n     Email: driver1@toll.com\n     Password: driver123\n")
        print("   DRIVER 2:\n     Email: driver2@toll.com\n     Password: driver123\n")
        print("=" * 60)


def drop_all_tables():
    """Drop all tables (use with caution!)"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "=" * 60)
        print("⚠️  WARNING: DROP ALL TABLES")
        print("=" * 60)
        response = input("\nThis will DELETE all data permanently. Are you sure? (type 'DELETE' to confirm): ")
        if response == 'DELETE':
            print("\n🗑️  Dropping all tables...")
            db.drop_all()
            print("✅ All tables dropped!")
        else:
            print("❌ Operation cancelled.")


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == 'init':
            init_database()
        elif command == 'seed':
            seed_sample_data()
        elif command == 'reset':
            drop_all_tables()
            init_database()
            seed_sample_data()
        elif command == 'drop':
            drop_all_tables()
        else:
            print("Usage: python init_db.py [init|seed|reset|drop]")
    else:
        # Default: init and seed
        init_database()
        seed_sample_data()
