# backend/routes/toll_zones.py
from flask import Blueprint, jsonify
from db.database import db
from models.models import TollZone
from middleware.auth_middleware import token_required, roles_required

toll_bp = Blueprint("toll_zones", __name__, url_prefix="/api/toll-zones")

# Get all toll zones
@toll_bp.route("/", methods=["GET"])
@token_required
def get_toll_zones(current_user):
    zones = TollZone.query.all()
    results = []
    for z in zones:
        results.append({
            "zone_id": str(z.zone_id),
            "name": z.name,
            "charge_amount": z.charge_amount,
            "polygon_coords": z.polygon_coords
        })
    return jsonify(results)
