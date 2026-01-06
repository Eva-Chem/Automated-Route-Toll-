# backend/models/models.py
import uuid
from db.database import db
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="DRIVER")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class TollZone(db.Model):
    __tablename__ = "toll_zones"

    zone_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    charge_amount = db.Column(db.Integer, nullable=False)
    polygon_coords = db.Column(JSONB, nullable=False)

class TollPaid(db.Model):
    __tablename__ = "tolls_paid"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    zone_id = db.Column(UUID(as_uuid=True), db.ForeignKey("toll_zones.zone_id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    checkout_request_id = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
