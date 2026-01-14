from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid

db = SQLAlchemy()


# -----------------------------
# Toll Zones Table
# -----------------------------
class TollZone(db.Model):
    __tablename__ = "toll_zones"

    zone_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    zone_name = db.Column(db.String, nullable=False)
    charge_amount = db.Column(db.Integer, nullable=False)
    polygon_coords = db.Column(JSONB, nullable=False)
    
    def to_dict(self):
        return {
            "zone_id": str(self.zone_id),
            "zone_name": self.zone_name,
            "charge_amount": self.charge_amount,
            "polygon_coords": self.polygon_coords
        }

# -----------------------------
# Tolls Paid Table
# -----------------------------
class TollPaid(db.Model):
    __tablename__ = "tolls_paid"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    zone_id = db.Column(UUID(as_uuid=True), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    checkout_request_id = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
