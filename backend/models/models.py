"""
Database Models for Automated Route Toll & Payment Tracker
File: backend/models/models.py
Task: SCRUM-20 - Toll Zone Data Model

This file contains all database models:
- User: Drivers, Operators, and Admins
- TollZone: Toll zone polygons and charges
- TollPaid: Payment transaction records
- TollEntry: Entry/exit tracking for duplicate prevention
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid

# Initialize SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    """
    User model for drivers, operators, and admins
    
    Roles:
    - DRIVER: Regular drivers who pay tolls
    - OPERATOR: Toll operators who manage zones
    - ADMIN: System administrators with full access
    """
    __tablename__ = 'users'
    
    # Primary Key
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # User Information
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'DRIVER', 'OPERATOR', 'ADMIN'
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tolls_paid = db.relationship('TollPaid', backref='driver', lazy=True)
    zones_created = db.relationship('TollZone', backref='creator', lazy=True)
    toll_entries = db.relationship('TollEntry', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.email} - {self.role}>'
    
    def to_dict(self):
        """Convert user to dictionary (exclude sensitive data)"""
        return {
            'user_id': str(self.user_id),
            'email': self.email,
            'phone_number': self.phone_number,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class TollZone(db.Model):
    """
    Toll zone model with geo-fencing polygon coordinates
    
    Each toll zone is defined by:
    - A polygon (array of [lat, lng] coordinates)
    - A charge amount (in cents, e.g., 5000 = KES 50.00)
    - Active/inactive status
    """
    __tablename__ = 'toll_zones'
    
    # Primary Key
    zone_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Zone Information
    zone_name = db.Column(db.String(255), nullable=False)
    charge_amount = db.Column(db.Integer, nullable=False)  # Amount in cents
    polygon_coords = db.Column(JSONB, nullable=False)  # Array of [lat, lng] pairs
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Metadata
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tolls_paid = db.relationship('TollPaid', backref='toll_zone', lazy=True)
    toll_entries = db.relationship('TollEntry', backref='zone', lazy=True)
    
    def __repr__(self):
        return f'<TollZone {self.zone_name} - KES {self.charge_amount/100:.2f}>'
    
    def to_dict(self):
        """Convert toll zone to dictionary"""
        return {
            'zone_id': str(self.zone_id),
            'zone_name': self.zone_name,
            'charge_amount': self.charge_amount,
            'charge_amount_formatted': f'KES {self.charge_amount/100:.2f}',
            'polygon_coords': self.polygon_coords,
            'is_active': self.is_active,
            'created_by': str(self.created_by) if self.created_by else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class TollPaid(db.Model):
    """
    Payment record for toll transactions
    
    Tracks:
    - Which driver paid
    - Which zone was entered
    - M-Pesa transaction details
    - Payment status (Pending, Completed, Failed)
    """
    __tablename__ = 'tolls_paid'
    
    # Primary Key
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Transaction Information
    zone_id = db.Column(UUID(as_uuid=True), db.ForeignKey('toll_zones.zone_id'), nullable=False, index=True)
    driver_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False, index=True)
    amount = db.Column(db.Integer, nullable=False)  # Amount in cents
    phone_number = db.Column(db.String(15), nullable=False)  # M-Pesa phone number
    
    # M-Pesa Details
    checkout_request_id = db.Column(db.String(255), unique=True, nullable=True, index=True)
    
    # Payment Status
    status = db.Column(db.String(20), nullable=False, default='Pending')  # 'Pending', 'Completed', 'Failed'
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<TollPaid {self.id} - {self.status} - KES {self.amount/100:.2f}>'
    
    def to_dict(self):
        """Convert toll payment to dictionary"""
        return {
            'id': str(self.id),
            'zone_id': str(self.zone_id),
            'zone_name': self.toll_zone.zone_name if self.toll_zone else None,
            'driver_id': str(self.driver_id),
            'driver_email': self.driver.email if self.driver else None,
            'amount': self.amount,
            'amount_formatted': f'KES {self.amount/100:.2f}',
            'phone_number': self.phone_number,
            'checkout_request_id': self.checkout_request_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class TollEntry(db.Model):
    """
    Track driver entries into toll zones to prevent duplicate triggers
    
    Purpose:
    - Record when a driver enters a toll zone
    - Record when a driver exits a toll zone
    - Prevent duplicate toll charges within 30 minutes
    - Link to payment record
    """
    __tablename__ = 'toll_entries'
    
    # Primary Key
    entry_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Entry Information
    driver_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False, index=True)
    zone_id = db.Column(UUID(as_uuid=True), db.ForeignKey('toll_zones.zone_id'), nullable=False, index=True)
    
    # Timing
    entry_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    exit_time = db.Column(db.DateTime, nullable=True)
    
    # Payment Link
    payment_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tolls_paid.id'), nullable=True)
    
    # Composite index for efficient duplicate detection
    __table_args__ = (
        db.Index('idx_driver_zone_active', 'driver_id', 'zone_id', 'exit_time'),
    )
    
    def __repr__(self):
        return f'<TollEntry driver:{self.driver_id} zone:{self.zone_id}>'
    
    def to_dict(self):
        """Convert toll entry to dictionary"""
        return {
            'entry_id': str(self.entry_id),
            'driver_id': str(self.driver_id),
            'zone_id': str(self.zone_id),
            'zone_name': self.zone.zone_name if self.zone else None,
            'entry_time': self.entry_time.isoformat() if self.entry_time else None,
            'exit_time': self.exit_time.isoformat() if self.exit_time else None,
            'payment_id': str(self.payment_id) if self.payment_id else None,
            'duration_minutes': self._calculate_duration() if self.exit_time else None
        }
    
    def _calculate_duration(self):
        """Calculate duration in minutes between entry and exit"""
        if self.entry_time and self.exit_time:
            duration = self.exit_time - self.entry_time
            return round(duration.total_seconds() / 60, 2)
        return None


# Helper functions for easy imports
def get_user_by_id(user_id):
    """Get user by ID"""
    return User.query.filter_by(user_id=user_id).first()


def get_user_by_email(email):
    """Get user by email"""
    return User.query.filter_by(email=email).first()


def get_active_toll_zones():
    """Get all active toll zones"""
    return TollZone.query.filter_by(is_active=True).all()


def get_zone_by_id(zone_id):
    """Get toll zone by ID"""
    return TollZone.query.filter_by(zone_id=zone_id).first()


def get_payment_by_id(payment_id):
    """Get payment by ID"""
    return TollPaid.query.filter_by(id=payment_id).first()