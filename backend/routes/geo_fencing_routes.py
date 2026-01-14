from flask import Blueprint, jsonify
from models.models import TollZone

geo_fencing_bp = Blueprint("geo_fencing_bp", __name__)

@geo_fencing_bp.route("/check-zones", methods=["GET"])
def check_zones_browser():
    zones = TollZone.query.filter_by(is_active=True).all()

    return jsonify({
        "success": True,
        "count": len(zones),
        "zones": [zone.to_dict() for zone in zones]
    }), 200
