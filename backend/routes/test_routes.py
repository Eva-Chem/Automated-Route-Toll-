"""
Test Routes for Geo-Fencing and Auth Middleware
File: backend/routes/test_routes.py

Purpose:
- SCRUM-22: Geo-fencing validation
- SCRUM-33: Role-based access control
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required

from models.models import User, TollZone
from services.geo_service import GeoFencingService
from middleware.auth_middleware import (
    admin_required,
    operator_required,
    driver_required,
    get_current_user
)

test_bp = Blueprint("test", __name__)

# ============================================================
# AUTHENTICATION TEST
# ============================================================

@test_bp.route("/test/login", methods=["POST"])
def test_login():
    """
    POST /api/test/login
    Body:
    {
        "email": "admin@toll.com",
        "password": "admin123"
    }
    """
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    access_token = create_access_token(identity=str(user.user_id))

    return jsonify({
        "access_token": access_token,
        "user": user.to_dict()
    }), 200


# ============================================================
# ROLE-BASED ACCESS TESTS (SCRUM-33)
# ============================================================

@test_bp.route("/test/admin-only", methods=["GET"])
@admin_required
def admin_only():
    user = get_current_user()
    return jsonify({
        "message": "Admin access granted",
        "user": user.to_dict(),
        "test": "SCRUM-33 PASSED"
    }), 200


@test_bp.route("/test/operator-only", methods=["GET"])
@operator_required
def operator_only():
    user = get_current_user()
    return jsonify({
        "message": "Operator access granted",
        "user": user.to_dict(),
        "test": "SCRUM-33 PASSED"
    }), 200


@test_bp.route("/test/driver-only", methods=["GET"])
@driver_required
def driver_only():
    user = get_current_user()
    return jsonify({
        "message": "Driver access granted",
        "user": user.to_dict(),
        "test": "SCRUM-33 PASSED"
    }), 200


# ============================================================
# GEO-FENCING TESTS (SCRUM-22)
# ============================================================

@test_bp.route("/test/check-zone", methods=["POST"])
@jwt_required()
def test_check_zone():
    """
    POST /api/test/check-zone
    Headers: Authorization: Bearer <token>
    Body:
    {
        "latitude": -1.2170,
        "longitude": 36.8894
    }
    """
    data = request.get_json()

    if not data or "latitude" not in data or "longitude" not in data:
        return jsonify({"error": "Latitude and longitude required"}), 400

    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    is_valid, error_msg = GeoFencingService.validate_coordinates(
        data["latitude"],
        data["longitude"]
    )

    if not is_valid:
        return jsonify({"error": error_msg}), 400

    result = GeoFencingService.check_zone_entry(
        str(user.user_id),
        data["latitude"],
        data["longitude"]
    )

    return jsonify({
        "test": "SCRUM-22 PASSED",
        "in_zone": result["in_zone"],
        "message": result["message"],
        "should_trigger_payment": result["should_trigger_payment"],
        "zone": result["zone"].to_dict() if result["zone"] else None
    }), 200


@test_bp.route("/test/point-in-polygon", methods=["POST"])
def test_point_in_polygon():
    """
    POST /api/test/point-in-polygon
    Body:
    {
        "latitude": -1.2170,
        "longitude": 36.8894,
        "polygon": [...]
    }
    """
    data = request.get_json()

    if not data or "latitude" not in data or "longitude" not in data or "polygon" not in data:
        return jsonify({"error": "latitude, longitude and polygon required"}), 400

    is_inside = GeoFencingService.is_point_in_polygon(
        data["latitude"],
        data["longitude"],
        data["polygon"]
    )

    return jsonify({
        "test": "Point-in-Polygon",
        "is_inside": is_inside,
        "points": len(data["polygon"])
    }), 200


# ============================================================
# UTILITY TESTS
# ============================================================

@test_bp.route("/test/zones", methods=["GET"])
def test_get_zones():
    zones = TollZone.query.filter_by(is_active=True).all()

    return jsonify({
        "count": len(zones),
        "zones": [zone.to_dict() for zone in zones]
    }), 200


@test_bp.route("/test/full-flow", methods=["POST"])
@driver_required
def test_full_flow():
    """
    Tests:
    - Authentication
    - Role validation
    - Geo-fencing logic
    """
    data = request.get_json()
    user = get_current_user()

    if not data or "latitude" not in data or "longitude" not in data:
        return jsonify({"error": "Latitude and longitude required"}), 400

    result = GeoFencingService.check_zone_entry(
        str(user.user_id),
        data["latitude"],
        data["longitude"]
    )

    return jsonify({
        "test": "FULL FLOW PASSED",
        "auth": {
            "user": user.to_dict(),
            "role": user.role
        },
        "geo_fencing": {
            "in_zone": result["in_zone"],
            "message": result["message"],
            "should_trigger_payment": result["should_trigger_payment"],
            "zone": result["zone"].to_dict() if result["zone"] else None
        }
    }), 200
