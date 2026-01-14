from shapely.geometry import Point, Polygon
from services.toll_zone_service import fetch_all_toll_zones

def is_point_inside_zone(lat, lng, polygon):
    polygon_points = [(p["lng"], p["lat"]) for p in polygon]
    zone_polygon = Polygon(polygon_points)
    vehicle_point = Point(lng, lat)
    return zone_polygon.contains(vehicle_point)

def check_zone_status(lat, lng):
    toll_zones = fetch_all_toll_zones()

    for zone in toll_zones:
        if is_point_inside_zone(lat, lng, zone["polygon"]):
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
