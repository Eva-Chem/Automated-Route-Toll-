"""
Geo-Fencing Service
File: backend/services/geo_service.py
Task: SCRUM-22 - Geo-fencing Logic

Responsibilities:
- Validate GPS coordinates
- Detect zone entry using polygon
- Prevent duplicate toll triggers
- Record zone exit
"""

from datetime import datetime, timedelta
from shapely.geometry import Point, Polygon
from db import db, TollZone, TollPaid, TollEntry
import json


class GeoFencingService:

    # --------------------------------------------------
    # Coordinate Validation
    # --------------------------------------------------
    @staticmethod
    def validate_coordinates(latitude, longitude):
        if latitude is None or longitude is None:
            return False, "Latitude and longitude are required"

        try:
            lat = float(latitude)
            lng = float(longitude)
        except ValueError:
            return False, "Latitude and longitude must be numbers"

        if lat < -90 or lat > 90:
            return False, "Latitude must be between -90 and 90"

        if lng < -180 or lng > 180:
            return False, "Longitude must be between -180 and 180"

        return True, None

    # --------------------------------------------------
    # Point in Polygon Check
    # --------------------------------------------------
    @staticmethod
    def is_point_in_polygon(lat, lng, polygon_coords):
        """
        polygon_coords: Can be either:
        1. GeoJSON format: {"type": "Polygon", "coordinates": [[[lng, lat], ...]]}
        2. Simple list format: [{"lat": x, "lng": y}, ...]
        3. JSON string of either format
        
        NOTE: Includes auto-detection for reversed coordinates as a safety measure
        """
        # Parse if it's a string
        if isinstance(polygon_coords, str):
            polygon_coords = json.loads(polygon_coords)
        
        # Handle GeoJSON format
        if isinstance(polygon_coords, dict) and polygon_coords.get("type") == "Polygon":
            # GeoJSON format: coordinates should be [longitude, latitude]
            coords = polygon_coords["coordinates"][0]  # Get outer ring
            
            # Safety check: Auto-detect if coordinates are reversed [lat, lng]
            # This handles legacy data or incorrectly formatted coordinates
            if coords and len(coords[0]) == 2:
                first_val = coords[0][0]
                second_val = coords[0][1]
                
                # Heuristic: If first value is within latitude range (-90 to 90)
                # and second value is outside that range (likely longitude),
                # then coordinates are reversed
                if abs(first_val) <= 90 and abs(second_val) > 90:
                    # Coordinates are reversed [lat, lng], swap to [lng, lat]
                    coords = [(lng, lat) for lat, lng in coords]
                    print(f"⚠️  Auto-corrected reversed coordinates for polygon")
            
            polygon = Polygon(coords)
        else:
            # Simple format: [{"lat": x, "lng": y}, ...]
            coords = [(c["lng"], c["lat"]) for c in polygon_coords]
            polygon = Polygon(coords)
        
        point = Point(lng, lat)
        return polygon.contains(point) or polygon.touches(point)

    # --------------------------------------------------
    # Zone Entry Detection
    # --------------------------------------------------
    @staticmethod
    def check_zone_entry(driver_id, latitude, longitude):
        """
        Check if driver has entered a toll zone
        
        Args:
            driver_id: UUID of the driver
            latitude: GPS latitude coordinate
            longitude: GPS longitude coordinate
            
        Returns:
            dict: Contains zone info, payment trigger status, and message
        """
        active_zones = TollZone.query.all()

        for zone in active_zones:
            if GeoFencingService.is_point_in_polygon(
                latitude, longitude, zone.polygon_coords
            ):
                # Check for active entry in THIS SPECIFIC ZONE (no exit yet)
                existing_entry = TollEntry.query.filter_by(
                    user_id=driver_id,
                    zone_id=zone.zone_id,
                    exit_time=None
                ).first()

                if existing_entry:
                    return {
                        "in_zone": True,
                        "zone": zone,
                        "should_trigger_payment": False,
                        "message": "Driver already inside zone"
                    }

                # Check last exit from THIS ZONE (30-minute grace period rule)
                recent_exit = TollEntry.query.filter(
                    TollEntry.user_id == driver_id,
                    TollEntry.zone_id == zone.zone_id,
                    TollEntry.exit_time.isnot(None)
                ).order_by(TollEntry.exit_time.desc()).first()

                if recent_exit:
                    time_diff = datetime.utcnow() - recent_exit.exit_time
                    if time_diff < timedelta(minutes=30):
                        return {
                            "in_zone": True,
                            "zone": zone,
                            "should_trigger_payment": False,
                            "message": "Recently exited zone — no duplicate charge"
                        }

                # Create new entry with zone_id
                entry = TollEntry(
                    user_id=driver_id,
                    zone_id=zone.zone_id,
                    entry_time=datetime.utcnow()
                )
                db.session.add(entry)
                db.session.commit()

                return {
                    "in_zone": True,
                    "zone": zone,
                    "should_trigger_payment": True,
                    "message": "Entered toll zone — payment required"
                }

        return {
            "in_zone": False,
            "zone": None,
            "should_trigger_payment": False,
            "message": "Not inside any toll zone"
        }

    # --------------------------------------------------
    # Zone Exit Recording
    # --------------------------------------------------
    @staticmethod
    def record_zone_exit(driver_id):
        """
        Record when a driver exits their current toll zone
        
        Args:
            driver_id: UUID of the driver
            
        Returns:
            bool: True if exit was recorded, False if no active entry found
        """
        entry = TollEntry.query.filter_by(
            user_id=driver_id,
            exit_time=None
        ).first()

        if not entry:
            return False

        entry.exit_time = datetime.utcnow()
        db.session.commit()
        return True