from shapely.geometry import Point, Polygon

def check_point_in_zone(lat, lng, polygon_coords):
    """
    Checks if coordinates are inside a list of lat/lng dictionaries.
    
    Args:
        lat: Latitude of the point
        lng: Longitude of the point
        polygon_coords: List of dicts with 'lat' and 'lng' keys
        
    Returns:
        bool: True if point is inside the polygon
    """
    try:
        # 1. Create the point using (lat, lng) order for consistency
        point = Point(lat, lng)
        
        # 2. Convert list of dicts to list of tuples for Shapely
        # Ensure we use (lat, lng) order consistently
        coords_tuple = [(c['lat'], c['lng']) for c in polygon_coords]
        
        # 3. Create polygon and check
        polygon = Polygon(coords_tuple)
        return polygon.contains(point)
    except Exception as e:
        print(f"Geo-fencing error: {e}")
        return False

