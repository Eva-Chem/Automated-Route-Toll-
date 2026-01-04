from shapely.geometry import Point, Polygon
from db import get_db_connection


def is_point_inside_zone(lat, lng, polygon):
    """
    Check if a point is inside a polygon using shapely.
    
    Args:
        lat: Latitude of the point
        lng: Longitude of the point
        polygon: List of dicts with 'lat' and 'lng' keys
        
    Returns:
        bool: True if point is inside the polygon
    """
    polygon_points = [
        (point["lng"], point["lat"])
        for point in polygon
    ]

    zone_polygon = Polygon(polygon_points)
    vehicle_point = Point(lng, lat)

    return zone_polygon.contains(vehicle_point)


def fetch_all_toll_zones():
    """
    Fetch all toll zones from the database.
    
    Returns:
        list: List of toll zone dictionaries
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id, name, charge_amount, polygon FROM toll_zones;")
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return [
        {
            "id": row[0],
            "name": row[1],
            "charge_amount": float(row[2]),
            "polygon": row[3]
        }
        for row in rows
    ]


def check_zone_status(lat, lng):
    """
    Check if coordinates are inside any toll zone.
    Returns the zone info and entry/exit status.
    
    Args:
        lat: Latitude of the vehicle
        lng: Longitude of the vehicle
        
    Returns:
        dict: Contains inside_zone (bool), status (str), and zone info (dict or None)
    """
    toll_zones = fetch_all_toll_zones()
    
    for zone in toll_zones:
        polygon = zone["polygon"]
        
        if is_point_inside_zone(lat, lng, polygon):
            return {
                "inside_zone": True,
                "status": "entry",
                "zone": {
                    "id": zone["id"],
                    "name": zone["name"],
                    "charge_amount": zone["charge_amount"]
                }
            }
    
    return {
        "inside_zone": False,
        "status": "exit",
        "zone": None
    }

