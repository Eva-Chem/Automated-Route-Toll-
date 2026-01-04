from flask import Blueprint, jsonify
from models.toll_zone import fetch_all_toll_zones

toll_zones_bp = Blueprint("toll_zones", __name__)

@toll_zones_bp.route("/", methods=["GET"])

def get_toll_zones():
    try:
        toll_zones = fetch_all_toll_zones()

        # Transform polygon data to coordinates format for frontend
        for zone in toll_zones:
            zone["coordinates"] = zone.pop("polygon")

        return jsonify({
            "success": True,
            "data": toll_zones
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
