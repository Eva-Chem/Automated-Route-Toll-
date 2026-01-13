from shapely.geometry import Point, Polygon
import json

def check_point_in_zone(lat, lng, polygon_coords):
    """
    Check if a point (lat, lng) is inside or on the edge of a polygon.
    
    Args:
        lat (float): Latitude of the point
        lng (float): Longitude of the point
        polygon_coords (list or str): List of {"lat": ..., "lng": ...} dicts
                                      or JSON string from DB
    
    Returns:
        bool: True if point is inside or on the polygon, False otherwise
    """
    try:
        # If the polygon coords are a JSON string, parse them
        if isinstance(polygon_coords, str):
            polygon_coords = json.loads(polygon_coords)

        # Shapely expects (x, y) = (lng, lat)
        coords = [(c["lng"], c["lat"]) for c in polygon_coords]
        polygon = Polygon(coords)
        point = Point(lng, lat)

        return polygon.contains(point) or polygon.touches(point)

    except Exception as e:
        print("Geo-fencing error:", e)
        return False
