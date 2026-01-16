# backend/services/geo_service.py
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
        polygon_coords: list of {"lat": x, "lng": y}
        """
        coords = [(c["lng"], c["lat"]) for c in polygon_coords]
        polygon = Polygon(coords)
        point = Point(lng, lat)

        return polygon.contains(point) or polygon.touches(point)

    # --------------------------------------------------
    # Zone Entry Detection
    # --------------------------------------------------
    @staticmethod
    def check_zone_entry(driver_id, latitude, longitude):
        active_zones = TollZone.query.all()

        for zone in active_zones:
            if GeoFencingService.is_point_in_polygon(
                latitude, longitude, zone.polygon_coords
            ):
                # Check for active entry (no exit yet)
                existing_entry = TollEntry.query.filter_by(
                    user_id=driver_id,  # Changed from driver_id to user_id
                    exit_time=None
                ).first()

                if existing_entry:
                    return {
                        "in_zone": True,
                        "zone": zone,
                        "should_trigger_payment": False,
                        "message": "Driver already inside zone"
                    }

                # Check last exit (30-minute rule)
                recent_exit = TollEntry.query.filter(
                    TollEntry.user_id == driver_id,  # Changed from driver_id
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

                # Create new entry
                entry = TollEntry(
                    user_id=driver_id,  # Changed from driver_id
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
        entry = TollEntry.query.filter_by(
            user_id=driver_id,  # Changed from driver_id
            exit_time=None
        ).first()

        if not entry:
            return False

        entry.exit_time = datetime.utcnow()
        db.session.commit()
        return True