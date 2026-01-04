from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.geo_fencing import check_point_in_zone
from models.toll_zone import TollZone

check_zone_bp = Blueprint("check_zone", __name__)

@check_zone_bp.route("/check-zone", methods=["POST"])
@jwt_required()
def check_zone():
    """
    Endpoint to check if driver coordinates are inside a toll zone.
    Expected payload: {"lat": float, "lng": float}
    Requires JWT authentication (Driver/Operator role).
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data or "lat" not in data or "lng" not in data:
            return jsonify({
                "success": False,
                "error": "Missing required fields: lat and lng"
            }), 400
        
        lat = float(data['lat'])
        driver_lng = float(data['lng'])
        
        # Validate coordinate ranges
        if not (-90 <= lat <= 90) or not (-180 <= driver_lng <= 180):
            return jsonify({
                "success": False,
                "error": "Invalid coordinates"
            }), 400
        
        # Check all toll zones
        zones = TollZone.query.all()
        
        for zone in zones:
            if check_point_in_zone(lat, driver_lng, zone.polygon_coords):
                return jsonify({
                    "success": True,
                    "in_zone": True,
                    "zone_name": zone.name,
                    "charge": zone.charge_amount,
                    "zone_id": zone.zone_id
                }), 200
        
        return jsonify({
            "success": True,
            "in_zone": False
        }), 200
        
    except ValueError:
        return jsonify({
            "success": False,
            "error": "Invalid coordinate format"
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

