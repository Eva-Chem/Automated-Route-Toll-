from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()


class TollZone(db.Model):
    __tablename__ = "toll_zones"

    zone_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    polygon_coords = db.Column(db.JSON, nullable=False)
    charge_amount = db.Column(db.Integer, nullable=False)  # store in cents
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    tolls = db.relationship("TollPaid", backref="zone", lazy=True)

    def to_dict(self):
        return {
            "zone_id": self.zone_id,
            "name": self.name,
            "polygon_coords": self.polygon_coords,
            "charge_amount": self.charge_amount,
            "is_active": self.is_active
        }


class TollPaid(db.Model):
    __tablename__ = "tolls_paid"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    zone_id = db.Column(
        db.String(36),
        db.ForeignKey("toll_zones.zone_id"),
        nullable=False
    )

    driver_id = db.Column(db.String(36), nullable=True)

    amount = db.Column(db.Integer, nullable=False)
    checkout_request_id = db.Column(db.String(100), nullable=True)
    mpesa_receipt_number = db.Column(db.String(100), nullable=True)

    status = db.Column(
        db.String(20),
        default="PENDING"  # PENDING | COMPLETED | FAILED
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "zone_id": self.zone_id,
            "driver_id": self.driver_id,
            "amount": self.amount,
            "status": self.status,
            "checkout_request_id": self.checkout_request_id,
            "created_at": self.created_at.isoformat()
        }
