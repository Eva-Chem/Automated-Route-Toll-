from shapely.geometry import Point, Polygon

def is_point_inside_zone(lat, lng, polygon):
    polygon_points = [
        (point["lng"], point["lat"])
        for point in polygon
    ]

    zone_polygon = Polygon(polygon_points)
    vehicle_point = Point(lng, lat)

    return zone_polygon.contains(vehicle_point)

def check_zone_status(lat, lng):
    """
    Check if coordinates are inside any toll zone.
    Returns the zone info and entry/exit status.
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