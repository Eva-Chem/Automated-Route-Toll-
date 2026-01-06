# backend/routes/geo_fencing.py
from flask import Blueprint, request, jsonify
from db.database import db
from models.models import TollZone
from utils.helpers import is_point_inside_zone
from middleware.auth_middleware import token_required

geo_bp = Blueprint("geo_fencing", __name__, url_prefix="/api/check-zone")

@geo_bp.route("/", methods=["POST"])
@token_required
def check_zone(current_user):
    data = request.get_json()
    lat = data.get("lat")
    lng = data.get("lng")

    if lat is None or lng is None:
        return jsonify({"message": "Latitude and longitude required"}), 400

    zones = TollZone.query.all()
    for zone in zones:
        if is_point_inside_zone(lat, lng, zone.polygon_coords):
            return jsonify({
                "inside_zone": True,
                "zone_id": str(zone.zone_id),
                "zone_name": zone.name,
                "charge_amount": zone.charge_amount
            })

    return jsonify({"inside_zone": False})
