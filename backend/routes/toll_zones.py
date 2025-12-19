from flask import Blueprint, jsonify

toll_zones_bp = Blueprint("toll_zones", __name__)

@toll_zones_bp.route("/api/toll-zones", methods=["GET"])
def get_toll_zones():
    toll_zones = [
        {
            "id": 1,
            "name": "Westlands Toll",
            "charge_amount": 200,
            "coordinates": [
                {"lat": -1.2675, "lng": 36.8123},
                {"lat": -1.2680, "lng": 36.8140},
                {"lat": -1.2660, "lng": 36.8150},
                {"lat": -1.2655, "lng": 36.8130}
            ]
        }
    ]

    return jsonify({
        "success": True,
        "data": toll_zones
    })
