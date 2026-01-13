from flask import Blueprint, jsonify
import os

from utils.auth import optional_jwt
from flask_jwt_extended import get_jwt_identity
from models.models import TollPaid, User

tolls_history_bp = Blueprint("tolls_history_bp", __name__)

@tolls_history_bp.route("/tolls-history", methods=["GET"])
@optional_jwt
def get_tolls_history():
    # --------------------------------
    # AUTH: ADMIN ONLY (PRODUCTION)
    # --------------------------------
    if os.getenv("FLASK_ENV") != "development":
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(user_id=current_user_id).first()

        if not user or user.role != "ADMIN":
            return jsonify({
                "success": False,
                "message": "Access forbidden: Admins only"
            }), 403

    # --------------------------------
    # FETCH TRANSACTIONS
    # --------------------------------
    tolls = TollPaid.query.order_by(TollPaid.created_at.desc()).all()

    results = []
    for toll in tolls:
        results.append({
            "toll_id": str(toll.id),
            "zone_name": toll.toll_zone.zone_name if toll.toll_zone else None,
            "amount": toll.amount,
            "status": toll.status,
            "timestamp": toll.created_at.isoformat()
        })

    return jsonify({
        "success": True,
        "data": results
    }), 200
