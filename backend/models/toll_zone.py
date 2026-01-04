import uuid
from datetime import datetime
from db.database import db
import json

class TollZone(db.Model):
    __tablename__ = 'toll_zones'

    zone_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    # polygon_coords stores the list of lat/lng pairs
    polygon_coords = db.Column(db.JSON, nullable=False) 
    charge_amount = db.Column(db.Integer, nullable=False)  # Store as cents/KES integer

    def __init__(self, name, polygon_coords, charge_amount):
        self.zone_id = str(uuid.uuid4())
        self.name = name
        self.polygon_coords = polygon_coords
        self.charge_amount = charge_amount

    def to_dict(self):
        return {
            "zone_id": self.zone_id,
            "name": self.name,
            "polygon_coords": self.polygon_coords,
            "charge_amount": self.charge_amount
        }

    @staticmethod
    def get_all():
        return TollZone.query.all()


class TollPayment(db.Model):
    __tablename__ = 'tolls_paid'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    zone_id = db.Column(db.String(36), db.ForeignKey('toll_zones.zone_id'))
    amount = db.Column(db.Integer, nullable=False)
    checkout_request_id = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(20), default='Pending')  # Pending/Completed/Failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, zone_id, amount, checkout_request_id, status='Pending'):
        self.id = str(uuid.uuid4())
        self.zone_id = zone_id
        self.amount = amount
        self.checkout_request_id = checkout_request_id
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "zone_id": self.zone_id,
            "amount": self.amount,
            "checkout_request_id": self.checkout_request_id,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }

def fetch_all_toll_zones():
    """
    Fetch all toll zones from the database (legacy function for compatibility).
    
    Returns:
        list: List of toll zone dictionaries
    """
    conn = db.get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id, name, charge_amount, polygon FROM toll_zones;")
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return [
        {
            "id": row[0],
            "name": row[1],
            "charge_amount": float(row[2]),
            "polygon_coords": row[3]  # Changed from "polygon" to "polygon_coords"
        }
        for row in rows
    ]

