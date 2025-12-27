from flask import Blueprint, request, jsonify
from services.geo_fencing import check_zone_status

check_zone_bp = Blueprint("check_zone", __name__)

@check_zone_bp.route("/api/check-zone", methods=["POST"])
def check_zone():
    """
    Endpoint to check if driver coordinates are inside a toll zone.
    Expected payload: {"lat": float, "lng": float}
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data or "lat" not in data or "lng" not in data:
            return jsonify({
                "success": False,
                "error": "Missing required fields: lat and lng"
            }), 400
        
        lat = float(data["lat"])
        lng = float(data["lng"])
        
        # Validate coordinate ranges
        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            return jsonify({
                "success": False,
                "error": "Invalid coordinates"
            }), 400
        
        # Check zone status
        result = check_zone_status(lat, lng)
        
        return jsonify({
            "success": True,
            "data": {
                "inside_zone": result["inside_zone"],
                "status": result["status"],
                "zone": result["zone"],
                "coordinates": {
                    "lat": lat,
                    "lng": lng
                }
            }
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