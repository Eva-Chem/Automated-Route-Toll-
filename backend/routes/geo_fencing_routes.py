"""
Geo-Fencing Routes
File: backend/routes/geo_fencing_routes.py
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from models.models import db, TollZone, TollEntry, TollPaid, User
from shapely.geometry import Point, Polygon
import uuid

geo_fencing_bp = Blueprint("geo_fencing_bp", __name__)


# --------------------------------
# HELPER: Check if point is inside polygon
# --------------------------------
def is_point_inside_zone(lat, lng, polygon_coords):
    """
    polygon_coords: list of dicts [{"lat": .., "lng": ..}, ...]
    """
    poly_points = [(p["lng"], p["lat"]) for p in polygon_coords]
    point = Point(lng, lat)
    polygon = Polygon(poly_points)
    return polygon.contains(point)


# --------------------------------
# POST /check-zone
# Trigger when vehicle enters a zone
# --------------------------------
@geo_fencing_bp.route("/check-zone", methods=["POST"])
def check_zone():
    data = request.get_json()
    vehicle_id = data.get("vehicle_id")
    lat = data.get("lat")
    lng = data.get("lng")

    if not vehicle_id or lat is None or lng is None:
        return jsonify({"success": False, "message": "Missing vehicle_id, lat, or lng"}), 400

    # Convert vehicle_id to UUID if needed
    try:
        driver_uuid = uuid.UUID(vehicle_id)
    except ValueError:
        return jsonify({"success": False, "message": "Invalid vehicle_id (must be UUID)"}), 400

    # Check all active toll zones
    zones = TollZone.query.filter_by(is_active=True).all()
    for zone in zones:
        if is_point_inside_zone(lat, lng, zone.polygon_coords):
            # Check if an active entry exists
            existing_entry = TollEntry.query.filter_by(
                driver_id=driver_uuid,
                zone_id=zone.zone_id,
                exit_time=None
            ).first()

            if existing_entry:
                return jsonify({
                    "success": True,
                    "in_zone": True,
                    "existing_entry": existing_entry.to_dict(),
                    "entry": None,
                    "should_trigger_payment": False,
                    "message": f"Already in {zone.zone_name}. Payment not triggered (duplicate prevention).",
                    "zone": zone.to_dict()
                }), 200

            # Create new Toll Entry
            entry = TollEntry(
                driver_id=driver_uuid,
                zone_id=zone.zone_id,
                entry_time=datetime.utcnow()
            )
            db.session.add(entry)
            db.session.commit()

            # Trigger payment (create TollPaid record)
            driver = User.query.get(driver_uuid)
            if driver:
                payment = TollPaid(
                    zone_id=zone.zone_id,
                    driver_id=driver_uuid,
                    amount=zone.charge_amount,
                    phone_number=driver.phone_number,
                    status="Pending"
                )
                db.session.add(payment)
                db.session.commit()

                # Link entry to payment
                entry.payment_id = payment.id
                db.session.commit()

            return jsonify({
                "success": True,
                "in_zone": True,
                "entry": entry.to_dict(),
                "existing_entry": None,
                "should_trigger_payment": True,
                "message": f"Entered {zone.zone_name}. Payment triggered.",
                "zone": zone.to_dict()
            }), 200

    # Not in any zone
    return jsonify({
        "success": True,
        "in_zone": False,
        "entry": None,
        "existing_entry": None,
        "should_trigger_payment": False,
        "message": "Not in any toll zone",
        "zone": None
    }), 200


# --------------------------------
# POST /exit-zone
# Trigger when vehicle exits a zone
# --------------------------------
@geo_fencing_bp.route("/exit-zone", methods=["POST"])
def exit_zone():
    data = request.get_json()
    vehicle_id = data.get("vehicle_id")
    zone_id = data.get("zone_id")

    if not vehicle_id or not zone_id:
        return jsonify({"success": False, "message": "Missing vehicle_id or zone_id"}), 400

    try:
        driver_uuid = uuid.UUID(vehicle_id)
        zone_uuid = uuid.UUID(zone_id)
    except ValueError:
        return jsonify({"success": False, "message": "Invalid UUID format"}), 400

    # Find active entry
    entry = TollEntry.query.filter_by(
        driver_id=driver_uuid,
        zone_id=zone_uuid,
        exit_time=None
    ).first()

    if not entry:
        return jsonify({
            "success": False,
            "message": f"No active entry found for vehicle {vehicle_id} in zone {zone_id}"
        }), 404

    # Update exit time
    entry.exit_time = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Vehicle {vehicle_id} exited zone {zone_id}",
        "entry": entry.to_dict()
    }), 200
