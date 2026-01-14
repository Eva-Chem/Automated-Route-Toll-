"""
Test Routes for Geo-Fencing and Auth Middleware
File: backend/routes/test_routes.py

Purpose:
- SCRUM-22: Geo-fencing validation
- SCRUM-33: Role-based access control
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from models.models import User, TollZone
from services.geo_service import GeoFencingService
from middleware.auth_middleware import (
    admin_required,
    operator_required,
    driver_required
)

test_bp = Blueprint("test_bp", __name__)

# ============================================================
# AUTHENTICATION TEST (TOKEN GENERATION)
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

    if not data:
        return jsonify({"error": "Request body required"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    # ⚠️ Password check skipped intentionally (TEST ROUTE ONLY)

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
    return jsonify({
        "message": "Admin access granted",
        "test": "SCRUM-33 PASSED"
    }), 200


@test_bp.route("/test/operator-only", methods=["GET"])
@operator_required
def operator_only():
    return jsonify({
        "message": "Operator access granted",
        "test": "SCRUM-33 PASSED"
    }), 200


@test_bp.route("/test/driver-only", methods=["GET"])
@driver_required
def driver_only():
    return jsonify({
        "message": "Driver access granted",
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
    data = request.get_js_
