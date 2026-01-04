from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from middlewares.auth import admin_required, operator_required
from models.toll_zone import TollZone, db

toll_zones_bp = Blueprint("toll_zones", __name__)

@toll_zones_bp.route("/", methods=["GET"])
@jwt_required()
@operator_required
def get_toll_zones():
    """Get all toll zones - accessible by admin and operator"""
    zones = TollZone.query.all()
    
    return jsonify({
        "success": True,
        "data": [zone.to_dict() for zone in zones]
    }), 200


@toll_zones_bp.route("/", methods=["POST"])
@jwt_required()
@admin_required
def create_toll_zone():
    """Create new toll zone - admin only"""
    data = request.get_json()
    
    if not data or "name" not in data or "charge_amount" not in data or "polygon_coords" not in data:
        return jsonify({
            "success": False,
            "error": "Missing required fields: name, charge_amount, polygon_coords"
        }), 400
    
    try:
        new_zone = TollZone(
            name=data['name'],
            charge_amount=int(data['charge_amount']),
            polygon_coords=data['polygon_coords']
        )
        db.session.add(new_zone)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "msg": "Zone created",
            "id": new_zone.zone_id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@toll_zones_bp.route("/<string:zone_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_toll_zone(zone_id):
    """Update toll zone - admin only"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            "success": False,
            "error": "No data provided"
        }), 400
    
    zone = TollZone.query.filter_by(zone_id=zone_id).first()
    
    if not zone:
        return jsonify({
            "success": False,
            "error": "Toll zone not found"
        }), 404
    
    try:
        if "name" in data:
            zone.name = data["name"]
        if "charge_amount" in data:
            zone.charge_amount = int(data["charge_amount"])
        if "polygon_coords" in data:
            zone.polygon_coords = data["polygon_coords"]
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "msg": "Toll zone updated successfully",
            "zone": zone.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@toll_zones_bp.route("/<string:zone_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_toll_zone(zone_id):
    """Delete toll zone - admin only"""
    zone = TollZone.query.filter_by(zone_id=zone_id).first()
    
    if not zone:
        return jsonify({
            "success": False,
            "error": "Toll zone not found"
        }), 404
    
    try:
        db.session.delete(zone)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "msg": "Toll zone deleted successfully",
            "id": zone_id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

