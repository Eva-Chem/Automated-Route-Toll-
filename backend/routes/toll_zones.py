"""
Toll Zones Routes
File: backend/routes/toll_zones.py
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.models import db, TollZone

toll_zones_bp = Blueprint("toll_zones_bp", __name__)


# --------------------------------
# GET all ACTIVE toll zones (public)
# --------------------------------
@toll_zones_bp.route("/toll-zones", methods=["GET"])
def get_toll_zones():
    zones = TollZone.query.filter_by(is_active=True).all()

    return jsonify({
        "success": True,
        "data": [zone.to_dict() for zone in zones]
    }), 200


# --------------------------------
# CREATE toll zone (Operator/Admin)
# --------------------------------
@toll_zones_bp.route("/toll-zones", methods=["POST"])
def create_toll_zone():
    try:
        data = request.get_json()

        zone = TollZone(
            zone_name=data["zone_name"],
            charge_amount=data["charge_amount"],
            polygon_coords=data["polygon_coords"],
            created_by=data.get("created_by")
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
@jwt_required()
def update_toll_zone(zone_id):
    try:
        zone = TollZone.query.filter_by(zone_id=zone_id).first_or_404()
        data = request.get_json()

        zone.zone_name = data.get("zone_name", zone.zone_name)
        zone.charge_amount = data.get("charge_amount", zone.charge_amount)
        zone.polygon_coords = data.get("polygon_coords", zone.polygon_coords)
        zone.is_active = data.get("is_active", zone.is_active)

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Toll zone updated",
            "zone": zone.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# --------------------------------
# SOFT DELETE (disable zone)
# --------------------------------
@toll_zones_bp.route("/toll-zones/<uuid:zone_id>", methods=["DELETE"])
@jwt_required()
def disable_toll_zone(zone_id):
    try:
        zone = TollZone.query.filter_by(zone_id=zone_id).first_or_404()
        zone.is_active = False

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Toll zone disabled"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500