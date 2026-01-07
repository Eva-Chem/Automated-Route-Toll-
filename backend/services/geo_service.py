"""
Geo-Fencing Service - Point-in-Polygon Implementation
File: backend/services/geo_service.py
Task: SCRUM-22 - Geo-Fencing Validation Logic

This service handles:
- Point-in-Polygon validation using Shapely
- Toll zone detection based on GPS coordinates
- Duplicate entry prevention
"""

from shapely.geometry import Point, Polygon
from models.models import TollZone, TollEntry, db
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeoFencingService:
    """Service for geo-fencing operations"""
    
    @staticmethod
    def is_point_in_polygon(latitude: float, longitude: float, polygon_coords: list) -> bool:
        """
        Check if a point (lat, lng) is inside a polygon using Shapely.
        
        Args:
            latitude (float): GPS latitude
            longitude (float): GPS longitude
            polygon_coords (list): List of [lat, lng] coordinate pairs
            
        Returns:
            bool: True if point is inside polygon, False otherwise
        """
        try:
            if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
                logger.error("Invalid coordinate types")
                return False
            
            if not polygon_coords or len(polygon_coords) < 3:
                logger.error("Invalid polygon: must have at least 3 points")
                return False
            
            point = Point(latitude, longitude)
            polygon = Polygon(polygon_coords)
            
            return polygon.contains(point)
            
        except Exception as e:
            logger.error(f"Error in point-in-polygon check: {str(e)}")
            return False
    
    
    @staticmethod
    def check_zone_entry(driver_id: str, latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Check if driver coordinates fall within any active toll zone.
        Prevents duplicate triggers within a time window.
        
        Args:
            driver_id (str): UUID of the driver
            latitude (float): Driver's current latitude
            longitude (float): Driver's current longitude
            
        Returns:
            dict: Result with zone information and payment trigger status
        """
        try:
            toll_zones = TollZone.query.filter_by(is_active=True).all()
            
            if not toll_zones:
                return {
                    'in_zone': False,
                    'zone': None,
                    'message': 'No active toll zones found',
                    'should_trigger_payment': False
                }
            
            for zone in toll_zones:
                is_inside = GeoFencingService.is_point_in_polygon(
                    latitude, 
                    longitude, 
                    zone.polygon_coords
                )
                
                if is_inside:
                    logger.info(f"Driver {driver_id} detected in zone {zone.zone_name}")
                    
                    recent_entry = TollEntry.query.filter(
                        TollEntry.driver_id == driver_id,
                        TollEntry.zone_id == zone.zone_id,
                        TollEntry.exit_time.is_(None),
                        TollEntry.entry_time >= datetime.utcnow() - timedelta(minutes=30)
                    ).first()
                    
                    if recent_entry:
                        return {
                            'in_zone': True,
                            'zone': zone,
                            'message': f'Already in {zone.zone_name}. Payment not triggered (duplicate prevention).',
                            'should_trigger_payment': False,
                            'existing_entry': recent_entry.to_dict()
                        }
                    
                    new_entry = TollEntry(
                        driver_id=driver_id,
                        zone_id=zone.zone_id,
                        entry_time=datetime.utcnow()
                    )
                    db.session.add(new_entry)
                    db.session.commit()
                    
                    return {
                        'in_zone': True,
                        'zone': zone,
                        'message': f'Entered {zone.zone_name}. Payment triggered.',
                        'should_trigger_payment': True,
                        'entry': new_entry.to_dict()
                    }
            
            return {
                'in_zone': False,
                'zone': None,
                'message': 'Not in any toll zone',
                'should_trigger_payment': False
            }
            
        except Exception as e:
            logger.error(f"Error checking zone entry: {str(e)}")
            db.session.rollback()
            return {
                'in_zone': False,
                'zone': None,
                'message': f'Error: {str(e)}',
                'should_trigger_payment': False
            }
    
    
    @staticmethod
    def record_zone_exit(driver_id: str, zone_id: str) -> bool:
        """Record when a driver exits a toll zone."""
        try:
            active_entry = TollEntry.query.filter(
                TollEntry.driver_id == driver_id,
                TollEntry.zone_id == zone_id,
                TollEntry.exit_time.is_(None)
            ).first()
            
            if active_entry:
                active_entry.exit_time = datetime.utcnow()
                db.session.commit()
                logger.info(f"Driver {driver_id} exited zone {zone_id}")
                return True
            else:
                logger.warning(f"No active entry found for driver {driver_id} in zone {zone_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error recording zone exit: {str(e)}")
            db.session.rollback()
            return False
    
    
    @staticmethod
    def validate_coordinates(latitude: float, longitude: float) -> tuple:
        """Validate GPS coordinates."""
        if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
            return False, "Coordinates must be numeric values"
        
        if latitude < -90 or latitude > 90:
            return False, "Latitude must be between -90 and 90"
        
        if longitude < -180 or longitude > 180:
            return False, "Longitude must be between -180 and 180"
        
        return True, ""


def check_if_in_zone(driver_id: str, latitude: float, longitude: float) -> Dict[str, Any]:
    """Convenience wrapper for zone checking"""
    return GeoFencingService.check_zone_entry(driver_id, latitude, longitude)