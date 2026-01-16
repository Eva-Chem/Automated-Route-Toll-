# backend/db/models.py
from db.database import db
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid

# -----------------------------
# User Table
# -----------------------------
class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'


# -----------------------------
# Toll Entries Table
# -----------------------------
class TollEntry(db.Model):
    __tablename__ = 'toll_entries'
    
    entry_id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    entry_time = db.Column(db.DateTime, nullable=False)
    exit_time = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='toll_entries')
    
    def __repr__(self):
        return f'<TollEntry {self.entry_id}>'


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