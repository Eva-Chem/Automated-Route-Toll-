from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models.models import TollPaid

tolls_history_bp = Blueprint("tolls_history_bp", __name__)

@tolls_history_bp.route("/api/tolls-history", methods=["GET"])
@jwt_required()
def get_tolls_history():
    """
    Get all toll payment transactions
    ADMIN ONLY
    """

    claims = get_jwt()
    role = claims.get("role")

    if role != "ADMIN":
        return jsonify({
            "success": False,
            "message": "Access denied. Admins only."
        }), 403

    tolls = TollPaid.query.order_by(TollPaid.created_at.desc()).all()

    return jsonify({
        "success": True,
        "data": [toll.to_dict() for toll in tolls]
    }), 200
