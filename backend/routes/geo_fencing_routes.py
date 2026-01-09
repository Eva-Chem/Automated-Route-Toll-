from flask import Blueprint, request, jsonify
from services.geo_fencing import check_point_in_zone
from models.models import TollZone

geo_fencing_bp = Blueprint(
    "geo_fencing",
    __name__,
    url_prefix="/api"
)

@geo_fencing_bp.route("/check-zone", methods=["POST"])
def check_zone():
    data = request.get_json()
    lat = data.get("lat")
    lng = data.get("lng")

    zones = TollZone.query.all()

    for zone in zones:
        if check_point_in_zone(lat, lng, zone.coordinates):
            return jsonify({
                "success": True,
                "inside_zone": True,
                "zone": {
                    "id": zone.id,
                    "name": zone.name,
                    "charge_amount": zone.charge_amount
                }
            })

    return jsonify({
        "success": True,
        "inside_zone": False
    })