# backend/routes/geo_fencing_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db, TollZone
from services.geo_service import GeoFencingService

geo_fencing_bp = Blueprint("geo_fencing_bp", __name__)

@geo_fencing_bp.route("/check-zones", methods=["GET"])
def check_zones_browser():
    zones = TollZone.query.all()

    return jsonify({
        "success": True,
        "count": len(zones),
        "zones": [zone.to_dict() for zone in zones]
    }), 200


@geo_fencing_bp.route("/check-location", methods=["POST"])
@jwt_required()
def check_location():
    """Check if driver's coordinates are inside any toll zone"""
    try:
        data = request.get_json()
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        
        # Validate coordinates
        is_valid, error = GeoFencingService.validate_coordinates(latitude, longitude)
        if not is_valid:
            return jsonify({
                "success": False,
                "error": error
            }), 400
        
        # Get current user ID from JWT token
        current_user_id = get_jwt_identity()
        
        # Check zone entry
        result = GeoFencingService.check_zone_entry(
            driver_id=current_user_id,
            latitude=float(latitude),
            longitude=float(longitude)
        )
        
        # Format response
        response = {
            "success": True,
            "in_zone": result["in_zone"],
            "should_trigger_payment": result["should_trigger_payment"],
            "message": result["message"]
        }
        
        if result["zone"]:
            response["zone"] = {
                "zone_id": str(result["zone"].zone_id),
                "zone_name": result["zone"].zone_name,
                "charge_amount": result["zone"].charge_amount
            }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@geo_fencing_bp.route("/exit-zone", methods=["POST"])
@jwt_required()
def exit_zone():
    """Record when driver exits a toll zone"""
    try:
        current_user_id = get_jwt_identity()
        
        success = GeoFencingService.record_zone_exit(current_user_id)
        
        if success:
            return jsonify({
                "success": True,
                "message": "Zone exit recorded successfully"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "No active zone entry found"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500