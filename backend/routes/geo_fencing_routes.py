from flask import Blueprint, request, jsonify
from models.models import TollZone

geo_fencing_bp = Blueprint("geo_fencing_bp", __name__)

@geo_fencing_bp.route("/check-zone", methods=["GET", "POST"])
def check_zone():
    # import inside function to avoid circular imports
    from services.geo_fencing import check_point_in_zone

    # -------------------------------------------------
    # GET → VISIBILITY (so you can SEE check zones)
    # -------------------------------------------------
    if request.method == "GET":
        zones = TollZone.query.filter_by(is_active=True).all()

        return jsonify({
            "success": True,
            "message": "Use POST with lat and lng to check a zone",
            "active_zones": [zone.to_dict() for zone in zones]
        }), 200

    # -------------------------------------------------
    # POST → REAL GEO-FENCING CHECK
    # -------------------------------------------------
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    lat = data.get("lat")
    lng = data.get("lng")

    if lat is None or lng is None:
        return jsonify({
            "success": False,
            "message": "lat and lng are required"
        }), 400

    zones = TollZone.query.filter_by(is_active=True).all()

    for zone in zones:
        inside = check_point_in_zone(
            lat,
            lng,
            zone.polygon_coords
        )

        if inside:
            return jsonify({
                "success": True,
                "inside_zone": True,
                "zone": zone.to_dict()
            }), 200

    return jsonify({
        "success": True,
        "inside_zone": False
    }), 200
