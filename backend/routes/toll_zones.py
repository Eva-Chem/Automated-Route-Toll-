# backend/routes/toll_zones.py
from flask import Blueprint, request, jsonify
from db import db, TollZone

toll_zones_bp = Blueprint("toll_zones_bp", __name__)

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
# CREATE a toll zone
# --------------------------------
@toll_zones_bp.route("/toll-zones", methods=["POST"])
def create_toll_zone():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "Request body is required"
        }), 400

    required_fields = ["zone_name", "charge_amount", "polygon_coords"]
    for field in required_fields:
        if field not in data:
            return jsonify({
                "success": False,
                "error": f"Missing required field: {field}"
            }), 400

    try:
        new_zone = TollZone(
            zone_name=data["zone_name"],
            charge_amount=int(data["charge_amount"]),
            polygon_coords=data["polygon_coords"]
        )

        db.session.add(new_zone)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Toll zone created successfully",
            "zone": new_zone.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# --------------------------------
# UPDATE a toll zone
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

    if not data:
        return jsonify({
            "success": False,
            "error": "Request body is required"
        }), 400

    try:
        if "zone_name" in data:
            zone.zone_name = data["zone_name"]

        if "charge_amount" in data:
            zone.charge_amount = int(data["charge_amount"])

        if "polygon_coords" in data:
            zone.polygon_coords = data["polygon_coords"]

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