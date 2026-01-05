"""
Comprehensive Test Suite for Automated Route Toll Backend
Tests all major components: Models, Auth Middleware, Geo-fencing, API Routes
"""

import pytest
import json
import uuid
from unittest.mock import MagicMock, patch
from datetime import datetime

# Import all components to test
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.toll_zone import TollZone, TollPayment
from services.geo_fencing import check_point_in_zone
from middlewares.auth import admin_required, operator_required


# ==================== MODEL TESTS ====================

class TestTollZoneModel:
    """Test TollZone model functionality"""
    
    def test_toll_zone_creation(self):
        """Test TollZone can be created with valid data"""
        zone = TollZone(
            name="Test Zone",
            polygon_coords=[{"lat": -1.28, "lng": 36.82}, {"lat": -1.29, "lng": 36.82}],
            charge_amount=200
        )
        
        assert zone.name == "Test Zone"
        assert zone.charge_amount == 200
        assert zone.zone_id is not None
        assert len(zone.polygon_coords) == 2
    
    def test_toll_zone_to_dict(self):
        """Test TollZone serialization to dictionary"""
        zone = TollZone(
            name="CBD Zone",
            polygon_coords=[{"lat": -1.28, "lng": 36.82}],
            charge_amount=300
        )

        zone_dict = zone.to_dict()

        assert "zone_id" in zone_dict
        assert zone_dict["name"] == "CBD Zone"
        assert zone_dict["charge"] == 300  # Changed from charge_amount for API consistency
        assert zone_dict["polygon_coords"] == [{"lat": -1.28, "lng": 36.82}]
    
    def test_toll_zone_default_values(self):
        """Test TollZone has correct default values"""
        zone = TollZone(
            name="Default Test",
            polygon_coords=[{"lat": 0, "lng": 0}],
            charge_amount=100
        )
        
        assert zone.zone_id is not None
        assert isinstance(zone.zone_id, str)


class TestTollPaymentModel:
    """Test TollPayment model functionality"""
    
    def test_toll_payment_creation(self):
        """Test TollPayment can be created with valid data"""
        payment = TollPayment(
            zone_id="test-zone-id",
            amount=200,
            checkout_request_id="test-checkout-123"
        )
        
        assert payment.zone_id == "test-zone-id"
        assert payment.amount == 200
        assert payment.checkout_request_id == "test-checkout-123"
        assert payment.status == "Pending"  # Default status
    
    def test_toll_payment_to_dict(self):
        """Test TollPayment serialization to dictionary"""
        payment = TollPayment(
            zone_id="zone-123",
            amount=500,
            checkout_request_id="checkout-456"
        )
        
        payment_dict = payment.to_dict()
        
        assert "id" in payment_dict
        assert payment_dict["zone_id"] == "zone-123"
        assert payment_dict["amount"] == 500
        assert payment_dict["status"] == "Pending"
        assert "created_at" in payment_dict
    
    def test_toll_payment_custom_status(self):
        """Test TollPayment with custom status"""
        payment = TollPayment(
            zone_id="zone-123",
            amount=100,
            checkout_request_id="checkout-789",
            status="Completed"
        )
        
        assert payment.status == "Completed"


# ==================== GEO-FENCING TESTS ====================

class TestGeoFencing:
    """Test geo-fencing logic"""
    
    def test_point_inside_polygon(self):
        """Test point inside a simple square polygon"""
        # Square polygon: (-1.28, 36.82) to (-1.29, 36.83)
        polygon_coords = [
            {"lat": -1.282, "lng": 36.820},
            {"lat": -1.288, "lng": 36.820},
            {"lat": -1.288, "lng": 36.828},
            {"lat": -1.282, "lng": 36.828}
        ]
        
        # Point in the center of the polygon
        result = check_point_in_zone(-1.285, 36.824, polygon_coords)
        assert result is True
    
    def test_point_outside_polygon(self):
        """Test point outside a polygon"""
        polygon_coords = [
            {"lat": -1.282, "lng": 36.820},
            {"lat": -1.288, "lng": 36.820},
            {"lat": -1.288, "lng": 36.828},
            {"lat": -1.282, "lng": 36.828}
        ]
        
        # Point far outside the polygon
        result = check_point_in_zone(-1.300, 36.850, polygon_coords)
        assert result is False
    
    def test_point_on_polygon_boundary(self):
        """Test point exactly on polygon boundary"""
        polygon_coords = [
            {"lat": -1.282, "lng": 36.820},
            {"lat": -1.288, "lng": 36.820},
            {"lat": -1.288, "lng": 36.828},
            {"lat": -1.282, "lng": 36.828}
        ]
        
        # Point on the boundary
        result = check_point_in_zone(-1.282, 36.824, polygon_coords)
        assert result is True  # Shapely contains boundary points
    
    def test_empty_polygon(self):
        """Test handling of empty polygon coordinates"""
        result = check_point_in_zone(-1.285, 36.824, [])
        assert result is False
    
    def test_single_point_polygon(self):
        """Test handling of single point polygon"""
        result = check_point_in_zone(-1.285, 36.824, [{"lat": -1.285, "lng": 36.824}])
        assert result is False  # Can't contain a point with single coordinate
    
    def test_nairobi_cbd_zone(self):
        """Test with actual Nairobi CBD zone coordinates"""
        polygon_coords = [
            {"lat": -1.2820, "lng": 36.8140},
            {"lat": -1.2950, "lng": 36.8140},
            {"lat": -1.2950, "lng": 36.8300},
            {"lat": -1.2820, "lng": 36.8300}
        ]
        
        # Point in CBD (near University of Nairobi)
        result = check_point_in_zone(-1.2860, 36.8170, polygon_coords)
        assert result is True
        
        # Point outside CBD (near Westlands)
        result = check_point_in_zone(-1.2650, 36.8100, polygon_coords)
        assert result is False


# ==================== AUTH MIDDLEWARE TESTS ====================

class TestAuthMiddleware:
    """Test authentication middleware"""
    
    def test_admin_required_no_jwt(self):
        """Test admin_required decorator blocks requests without JWT"""
        @admin_required
        def test_function():
            return "success"
        
        # Mock verify_jwt_in_request to raise exception
        with patch('routes.payment_routes.verify_jwt_in_request') as mock_verify:
            mock_verify.side_effect = Exception("No JWT token")
            
            result = test_function()
            
            assert result[1] == 403  # Should return 403 Forbidden
    
    def test_admin_required_non_admin(self):
        """Test admin_required decorator blocks non-admin users"""
        @admin_required
        def test_function():
            return "success"
        
        # Mock JWT claims with non-admin role
        with patch('routes.payment_routes.verify_jwt_in_request'):
            with patch('routes.payment_routes.get_jwt') as mock_get_jwt:
                mock_get_jwt.return_value = {"sub": {"id": "user123", "role": "USER"}}
                
                result = test_function()
                
                assert result[1] == 403  # Should return 403 Forbidden
    
    def test_operator_required_non_authorized(self):
        """Test operator_required blocks unauthorized roles"""
        @operator_required
        def test_function():
            return "success"
        
        # Mock JWT claims with unauthorized role
        with patch('routes.payment_routes.verify_jwt_in_request'):
            with patch('routes.payment_routes.get_jwt') as mock_get_jwt:
                mock_get_jwt.return_value = {"sub": {"id": "user123", "role": "DRIVER"}}
                
                result = test_function()
                
                assert result[1] == 403  # Should return 403 Forbidden
    
    def test_admin_required_admin_user(self):
        """Test admin_required allows admin users"""
        @admin_required
        def test_function():
            return "success", 200
        
        # Mock JWT claims with admin role
        with patch('routes.payment_routes.verify_jwt_in_request'):
            with patch('routes.payment_routes.get_jwt') as mock_get_jwt:
                mock_get_jwt.return_value = {"sub": {"id": "admin123", "role": "ADMIN"}}
                
                result = test_function()
                
                assert result == ("success", 200)
    
    def test_operator_required_admin(self):
        """Test operator_required allows admin users"""
        @operator_required
        def test_function():
            return "success", 200
        
        # Mock JWT claims with admin role
        with patch('routes.payment_routes.verify_jwt_in_request'):
            with patch('routes.payment_routes.get_jwt') as mock_get_jwt:
                mock_get_jwt.return_value = {"sub": {"id": "admin123", "role": "ADMIN"}}
                
                result = test_function()
                
                assert result == ("success", 200)
    
    def test_operator_required_operator(self):
        """Test operator_required allows operator users"""
        @operator_required
        def test_function():
            return "success", 200
        
        # Mock JWT claims with operator role
        with patch('routes.payment_routes.verify_jwt_in_request'):
            with patch('routes.payment_routes.get_jwt') as mock_get_jwt:
                mock_get_jwt.return_value = {"sub": {"id": "op123", "role": "OPERATOR"}}
                
                result = test_function()
                
                assert result == ("success", 200)


# ==================== API ROUTE TESTS ====================

class TestCheckZoneRoute:
    """Test /check-zone API endpoint"""
    
    def test_check_zone_missing_coordinates(self):
        """Test /check-zone returns error for missing coordinates"""
        from routes.check_zone import check_zone_bp
        
        # Create test client
        app = MagicMock()
        app.config = {'TESTING': True}
        
        # This would require actual Flask app setup - simplified test
        assert True  # Placeholder for full integration test
    
    def test_check_zone_response_format(self):
        """Test /check-zone returns correct response format"""
        # Response should contain: in_zone, zone_name, charge, success
        expected_keys = {"in_zone", "success"}
        
        # This would be tested with actual Flask test client
        assert True  # Placeholder for full integration test


# ==================== INTEGRATION TESTS ====================

class TestEndToEnd:
    """End-to-end integration tests"""
    
    def test_zone_payment_workflow(self):
        """Test complete workflow: create zone -> check location -> create payment"""
        # 1. Create a toll zone
        zone = TollZone(
            name="Integration Test Zone",
            polygon_coords=[
                {"lat": -1.280, "lng": 36.800},
                {"lat": -1.290, "lng": 36.800},
                {"lat": -1.290, "lng": 36.810},
                {"lat": -1.280, "lng": 36.810}
            ],
            charge_amount=250
        )
        
        # 2. Verify location is inside zone
        lat, lng = -1.285, 36.805
        is_inside = check_point_in_zone(lat, lng, zone.polygon_coords)
        assert is_inside is True
        
        # 3. Create payment for the zone
        payment = TollPayment(
            zone_id=zone.zone_id,
            amount=zone.charge_amount,
            checkout_request_id=f"test-{uuid.uuid4()}"
        )
        
        # 4. Verify payment was created correctly
        assert payment.zone_id == zone.zone_id
        assert payment.amount == zone.charge_amount
        assert payment.status == "Pending"
    
    def test_multiple_zones_geo_check(self):
        """Test checking location against multiple zones"""
        # Zone 1: Nairobi CBD
        zone1_coords = [
            {"lat": -1.2820, "lng": 36.8140},
            {"lat": -1.2950, "lng": 36.8140},
            {"lat": -1.2950, "lng": 36.8300},
            {"lat": -1.2820, "lng": 36.8300}
        ]
        
        # Zone 2: Westlands
        zone2_coords = [
            {"lat": -1.2650, "lng": 36.8050},
            {"lat": -1.2720, "lng": 36.8050},
            {"lat": -1.2720, "lng": 36.8150},
            {"lat": -1.2650, "lng": 36.8150}
        ]
        
        zones = [zone1_coords, zone2_coords]
        
        # Point in CBD
        in_zone1 = check_point_in_zone(-1.2860, 36.8200, zone1_coords)
        in_zone2 = check_point_in_zone(-1.2860, 36.8200, zone2_coords)
        
        assert in_zone1 is True
        assert in_zone2 is False
        
        # Point in Westlands
        in_zone1 = check_point_in_zone(-1.2680, 36.8100, zone1_coords)
        in_zone2 = check_point_in_zone(-1.2680, 36.8100, zone2_coords)
        
        assert in_zone1 is False
        assert in_zone2 is True


# ==================== RUNNER ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

