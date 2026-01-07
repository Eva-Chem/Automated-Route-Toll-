"""
Test Routes for Geo-Fencing and Auth Middleware
File: backend/routes/test_routes.py

These routes test your SCRUM-22 and SCRUM-33 implementations
"""

from flask import Blueprint, request, jsonify
from services.geo_service import GeoFencingService
from middleware.auth_middleware import admin_required, operator_required, driver_required, get_current_user
from models.models import TollZone, User
from flask_jwt_extended import create_access_token, jwt_required

test_bp = Blueprint('test', __name__)


# ============================================================
# AUTHENTICATION TEST ROUTES
# ============================================================

@test_bp.route('/test/login', methods=['POST'])
def test_login():
    """
    Test login endpoint (simplified for testing)
    POST /api/test/login
    Body: {"email": "admin@toll.com", "password": "admin123"}
    """
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # In production, use proper password verification
    # For testing, we'll create a token
    access_token = create_access_token(identity=str(user.user_id))
    
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200


# ============================================================
# ROLE-BASED ACCESS TEST ROUTES (SCRUM-33)
# ============================================================

@test_bp.route('/test/admin-only', methods=['GET'])
@admin_required
def admin_only_route():
    """
    Test admin-only access
    GET /api/test/admin-only
    Headers: Authorization: Bearer <token>
    """
    user = get_current_user()
    return jsonify({
        'message': 'Admin access granted!',
        'user': user.to_dict(),
        'test': 'SCRUM-33 - Admin middleware working'
    }), 200


@test_bp.route('/test/operator-only', methods=['GET'])
@operator_required
def operator_only_route():
    """
    Test operator access (Operator and Admin can access)
    GET /api/test/operator-only
    Headers: Authorization: Bearer <token>
    """
    user = get_current_user()
    return jsonify({
        'message': 'Operator access granted!',
        'user': user.to_dict(),
        'test': 'SCRUM-33 - Operator middleware working'
    }), 200


@test_bp.route('/test/driver-only', methods=['GET'])
@driver_required
def driver_only_route():
    """
    Test driver access
    GET /api/test/driver-only
    Headers: Authorization: Bearer <token>
    """
    user = get_current_user()
    return jsonify({
        'message': 'Driver access granted!',
        'user': user.to_dict(),
        'test': 'SCRUM-33 - Driver middleware working'
    }), 200


# ============================================================
# GEO-FENCING TEST ROUTES (SCRUM-22)
# ============================================================

@test_bp.route('/test/check-zone', methods=['POST'])
@jwt_required()
def test_check_zone():
    """
    Test geo-fencing zone detection
    POST /api/test/check-zone
    Headers: Authorization: Bearer <token>
    Body: {"latitude": -1.2170, "longitude": 36.8894}
    """
    data = request.get_json()
    
    if not data or 'latitude' not in data or 'longitude' not in data:
        return jsonify({'error': 'Latitude and longitude required'}), 400
    
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Validate coordinates
    is_valid, error_msg = GeoFencingService.validate_coordinates(
        data['latitude'],
        data['longitude']
    )
    
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    # Check zone entry
    result = GeoFencingService.check_zone_entry(
        str(user.user_id),
        data['latitude'],
        data['longitude']
    )
    
    response = {
        'test': 'SCRUM-22 - Geo-fencing validation working',
        'in_zone': result['in_zone'],
        'message': result['message'],
        'should_trigger_payment': result['should_trigger_payment'],
        'coordinates': {
            'latitude': data['latitude'],
            'longitude': data['longitude']
        }
    }
    
    if result['zone']:
        response['zone'] = result['zone'].to_dict()
    
    return jsonify(response), 200


@test_bp.route('/test/point-in-polygon', methods=['POST'])
def test_point_in_polygon():
    """
    Test raw Point-in-Polygon algorithm
    POST /api/test/point-in-polygon
    Body: {
        "latitude": -1.2170,
        "longitude": 36.8894,
        "polygon": [[-1.2195, 36.8869], [-1.2195, 36.8919], [-1.2145, 36.8919], [-1.2145, 36.8869]]
    }
    """
    data = request.get_json()
    
    if not data or 'latitude' not in data or 'longitude' not in data or 'polygon' not in data:
        return jsonify({'error': 'Latitude, longitude, and polygon required'}), 400
    
    is_inside = GeoFencingService.is_point_in_polygon(
        data['latitude'],
        data['longitude'],
        data['polygon']
    )
    
    return jsonify({
        'test': 'SCRUM-22 - Point-in-Polygon algorithm',
        'is_inside': is_inside,
        'coordinates': {
            'latitude': data['latitude'],
            'longitude': data['longitude']
        },
        'polygon_points': len(data['polygon'])
    }), 200


@test_bp.route('/test/zones', methods=['GET'])
def test_get_zones():
    """
    Get all toll zones for testing
    GET /api/test/zones
    """
    zones = TollZone.query.filter_by(is_active=True).all()
    
    return jsonify({
        'test': 'Get toll zones',
        'count': len(zones),
        'zones': [zone.to_dict() for zone in zones]
    }), 200


# ============================================================
# COMBINED TEST ROUTE
# ============================================================

@test_bp.route('/test/full-flow', methods=['POST'])
@driver_required
def test_full_flow():
    """
    Test complete flow: Auth + Geo-fencing
    POST /api/test/full-flow
    Headers: Authorization: Bearer <token>
    Body: {"latitude": -1.2170, "longitude": 36.8894}
    """
    data = request.get_json()
    user = get_current_user()
    
    if not data or 'latitude' not in data or 'longitude' not in data:
        return jsonify({'error': 'Latitude and longitude required'}), 400
    
    # Check zone
    result = GeoFencingService.check_zone_entry(
        str(user.user_id),
        data['latitude'],
        data['longitude']
    )
    
    return jsonify({
        'test': 'FULL FLOW - Auth (SCRUM-33) + Geo-fencing (SCRUM-22)',
        'auth': {
            'authenticated': True,
            'user': user.to_dict(),
            'role_check': 'PASSED'
        },
        'geo_fencing': {
            'in_zone': result['in_zone'],
            'message': result['message'],
            'should_trigger_payment': result['should_trigger_payment'],
            'zone': result['zone'].to_dict() if result['zone'] else None
        }
    }), 200
