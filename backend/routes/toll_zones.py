"""
Toll Zones Routes
File: backend/routes/toll_zones.py
Task: Backend Task 3 - Toll Zone CRUD API
"""

from flask import Blueprint, request, jsonify
from models.models import db, TollZone

toll_zones_bp = Blueprint("toll_zones_bp", __name__, url_prefix="/api")


# --------------------------------
# GET all toll zones
# --------------------------------
@toll_zones_bp.route("/toll-zones", methods=["GET"])
def get_toll_zones():
    zones = TollZone.query.all()

    return jsonify({
        "success": True,
        "data": [zone.to_dict() for zone in zones]
    }), 200


# --------------------------------
# CREATE toll zone
# --------------------------------
@toll_zones_bp.route("/toll-zones", methods=["POST"])
def create_toll_zone():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "No data provided"
        }), 400

    try:
        zone = TollZone(
            zone_name=data["zone_name"],
            charge_amount=data["charge_amount"],
            polygon_coords=data["polygon_coords"]
        )

        db.session.add(zone)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Toll zone created successfully",
            "zone": zone.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# --------------------------------
# UPDATE toll zone
# --------------------------------
@toll_zones_bp.route("/toll-zones/<uuid:zone_id>", methods=["PUT"])
def update_toll_zone(zone_id):
    zone = TollZone.query.filter_by(zone_id=zone_id).first()

    if not zone:
        return jsonify({
            "success": False,
            "error": "Toll zone not found"
        }), 404

    data = request.get_json()

    try:
        zone.zone_name = data.get("zone_name", zone.zone_name)
        zone.charge_amount = data.get("charge_amount", zone.charge_amount)
        zone.polygon_coords = data.get("polygon_coords", zone.polygon_coords)

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Toll zone updated successfully",
            "zone": zone.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
