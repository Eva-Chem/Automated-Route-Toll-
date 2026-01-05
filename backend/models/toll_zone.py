import uuid
from datetime import datetime
from db.database import db


class TollZone(db.Model):
    __tablename__ = 'toll_zones'

    # Using zone_id to match your SQL insert statements
    zone_id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    polygon_coords = db.Column(db.JSON, nullable=False)
    charge_amount = db.Column(db.Float, nullable=False)

    def __init__(self, name, polygon_coords, charge_amount, zone_id=None):
        self.zone_id = zone_id or str(uuid.uuid4())
        self.name = name
        self.polygon_coords = polygon_coords
        self.charge_amount = charge_amount

    def to_dict(self):
        return {
            "zone_id": self.zone_id,
            "name": self.name,
            "polygon_coords": self.polygon_coords,
            "charge": self.charge_amount  # Renamed for API consistency
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

