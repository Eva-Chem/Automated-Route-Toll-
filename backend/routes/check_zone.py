from flask import Blueprint, request, jsonify
from models.toll_zone import TollZone
from services.geo_fencing import check_point_in_zone

check_zone_bp = Blueprint('check_zone', __name__)


@check_zone_bp.route('/check-zone', methods=['POST'])
def check_zone():
    try:
        data = request.get_json()
        lat, lng = data.get('lat'), data.get('lng')

        if lat is None or lng is None:
            return jsonify({"error": "Missing coordinates", "success": False}), 400

        # Query all zones (including the ones from your SQL insert)
        all_zones = TollZone.query.all()

        for zone in all_zones:
            # Check if current lat/lng is inside the polygon from DB
            if check_point_in_zone(lat, lng, zone.polygon_coords):
                return jsonify({
                    "in_zone": True,
                    "zone_name": zone.name,
                    "charge": zone.charge_amount,
                    "success": True
                }), 200

        return jsonify({"in_zone": False, "success": True}), 200

    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500

