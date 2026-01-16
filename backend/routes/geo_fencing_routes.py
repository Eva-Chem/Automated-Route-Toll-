# backend/routes/geo_fencing_routes.py
from flask import Blueprint, jsonify
from db import db, TollZone

geo_fencing_bp = Blueprint("geo_fencing_bp", __name__)

@geo_fencing_bp.route("/check-zones", methods=["GET"])
def check_zones_browser():
    zones = TollZone.query.all()

    return jsonify({
        "success": True,
        "count": len(zones),
        "zones": [zone.to_dict() for zone in zones]
    }), 200