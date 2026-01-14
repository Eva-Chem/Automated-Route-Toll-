from flask import Blueprint, jsonify
from services.toll_zone_service import fetch_all_toll_zones

toll_zones_bp = Blueprint("toll_zones", __name__)

@toll_zones_bp.route("/api/toll-zones", methods=["GET"])
def get_toll_zones():
    return jsonify({
        "success": True,
        "data": fetch_all_toll_zones()
    })
