"""
Database Models for Automated Route Toll & Payment Tracker
File: backend/models/models.py

Tasks:
- SCRUM-20: Toll Zone Data Model
- SCRUM-22: Geo-fencing support
- SCRUM-33: Role-based access
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid

# --------------------------------
# SQLAlchemy Instance
# --------------------------------
db = SQLAlchemy()


# ============================================================
# USER MODEL
# ============================================================
class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # ADMIN | OPERATOR | DRIVER
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    tolls_paid = db.relationship("TollPaid", backref="driver", lazy=True)
    zones_created = db.relationship("TollZone", backref="creator", lazy=True)
    toll_entries = db.relationship("TollEntry", backref="user", lazy=True)

    def to_dict(self):
        return {
            "user_id": str(self.user_id),
            "email": self.email,
            "phone_number": self.phone_number,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat()
        }


# ============================================================
# TOLL ZONE MODEL
# ============================================================
class TollZone(db.Model):
    __tablename__ = "toll_zones"

    zone_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    zone_name = db.Column(db.String(255), nullable=False)
    charge_amount = db.Column(db.Integer, nullable=False)  # cents
    polygon_coords = db.Column(JSONB, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey("users.user_id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    tolls_paid = db.relationship("TollPaid", backref="toll_zone", lazy=True)
    toll_entries = db.relationship("TollEntry", backref="zone", lazy=True)

    def to_dict(self):
        return {
            "zone_id": str(self.zone_id),
            "zone_name": self.zone_name,
            "charge_amount": self.charge_amount,
            "charge_amount_formatted": f"KES {self.charge_amount / 100:.2f}",
            "polygon_coords": self.polygon_coords,
            "is_active": self.is_active,
            "created_by": str(self.created_by) if self.created_by else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


# ============================================================
# PAYMENT MODEL
# ============================================================
class TollPaid(db.Model):
    __tablename__ = "tolls_paid"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    zone_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("toll_zones.zone_id"),
        nullable=False,
        index=True
    )

    driver_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.user_id"),
        nullable=False,
        index=True
    )

    amount = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    checkout_request_id = db.Column(db.String(255), unique=True, index=True)
    status = db.Column(db.String(20), default="Pending", nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": str(self.id),
            "zone_id": str(self.zone_id),
            "zone_name": self.toll_zone.zone_name if self.toll_zone else None,
            "driver_id": str(self.driver_id),
            "driver_email": self.driver.email if self.driver else None,
            "amount": self.amount,
            "amount_formatted": f"KES {self.amount / 100:.2f}",
            "phone_number": self.phone_number,
            "checkout_request_id": self.checkout_request_id,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }


# ============================================================
# TOLL ENTRY MODEL
# ============================================================
class TollEntry(db.Model):
    __tablename__ = "toll_entries"

    entry_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    driver_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.user_id"),
        nullable=False,
        index=True
    )

    zone_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("toll_zones.zone_id"),
        nullable=False,
        index=True
    )

    entry_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    exit_time = db.Column(db.DateTime)

    payment_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("tolls_paid.id")
    )

    __table_args__ = (
        db.Index("idx_active_entry", "driver_id", "zone_id", "exit_time"),
    )

    def to_dict(self):
        return {
            "entry_id": str(self.entry_id),
            "driver_id": str(self.driver_id),
            "zone_id": str(self.zone_id),
            "zone_name": self.zone.zone_name if self.zone else None,
            "entry_time": self.entry_time.isoformat(),
            "exit_time": self.exit_time.isoformat() if self.exit_time else None
        }


# ============================================================
# HELPER QUERIES
# ============================================================
def get_user_by_id(user_id):
    return User.query.filter_by(user_id=user_id).first()


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_active_toll_zones():
    return TollZone.query.filter_by(is_active=True).all()
