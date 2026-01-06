# backend/app.py
from flask import Flask, jsonify, request
from config import Config
from db.database import db, init_db
from models.models import User, TollZone, TollPaid
from utils.helpers import is_point_inside_zone
from functools import wraps
from flask_cors import CORS
import jwt
import datetime

# -------------------------
# Role-based Auth Middleware
# -------------------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            token = token.split(" ")[1]  # Bearer token
            data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.filter_by(id=data["user_id"]).first()
            if not current_user:
                raise Exception("User not found")
        except Exception as e:
            return jsonify({"message": "Token is invalid!", "error": str(e)}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(current_user, *args, **kwargs):
            if current_user.role not in roles:
                return jsonify({"message": "Forbidden: insufficient role"}), 403
            return f(current_user, *args, **kwargs)
        return wrapper
    return decorator

# -------------------------
# App Factory
# -------------------------
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # Initialize DB
    init_db(app)

    # -------------------------
    # Routes
    # -------------------------

    @app.route("/api/toll-zones", methods=["GET"])
    @token_required
    def get_toll_zones(current_user):
        zones = TollZone.query.all()
        result = [
            {
                "zone_id": str(z.zone_id),
                "name": z.name,
                "charge_amount": z.charge_amount,
                "polygon_coords": z.polygon_coords
            }
            for z in zones
        ]
        return jsonify(result)

    @app.route("/api/check-zone", methods=["POST"])
    @token_required
    def check_zone(current_user):
        data = request.json
        lat = data.get("lat")
        lng = data.get("lng")
        if lat is None or lng is None:
            return jsonify({"message": "Latitude and longitude required"}), 400

        zones = TollZone.query.all()
        for zone in zones:
            if is_point_inside_zone(lat, lng, zone.polygon_coords):
                return jsonify({
                    "zone_id": str(zone.zone_id),
                    "name": zone.name,
                    "charge_amount": zone.charge_amount
                })
        return jsonify({"message": "No toll zone matched"}), 404

    @app.route("/api/admin/dashboard")
    @token_required
    @roles_required("ADMIN")
    def admin_dashboard(current_user):
        total_tolls = TollPaid.query.count()
        completed = TollPaid.query.filter_by(status="Completed").count()
        pending = TollPaid.query.filter_by(status="Pending").count()
        failed = TollPaid.query.filter_by(status="Failed").count()
        return jsonify({
            "message": f"Welcome {current_user.username}",
            "total_tolls": total_tolls,
            "completed": completed,
            "pending": pending,
            "failed": failed
        })

    @app.route("/api/login", methods=["POST"])
    def login():
        data = request.json
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return jsonify({"message": "Username and password required"}), 400

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return jsonify({"message": "Invalid credentials"}), 401

        token = jwt.encode({
            "user_id": str(user.id),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        }, Config.JWT_SECRET_KEY, algorithm="HS256")

        return jsonify({"token": token, "role": user.role})

    return app

# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
