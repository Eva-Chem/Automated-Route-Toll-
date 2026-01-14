from flask import Blueprint, jsonify
from models.models import TollPaid, TollZone

tolls_history_bp = Blueprint("tolls_history_bp", __name__)

@tolls_history_bp.route("/tolls-history", methods=["GET"])
def get_tolls_history():
    tolls = TollPaid.query.order_by(TollPaid.created_at.desc()).all()

    results = []
    for toll in tolls:
        zone = TollZone.query.filter_by(zone_id=toll.zone_id).first()

        results.append({
            "id": str(toll.id),
            "zone_name": zone.zone_name if zone else None,
            "amount": toll.amount,
            "status": toll.status,
            "checkout_request_id": toll.checkout_request_id,
            "created_at": toll.created_at.isoformat()
        })

    return jsonify({
        "success": True,
        "data": results
    }), 200
