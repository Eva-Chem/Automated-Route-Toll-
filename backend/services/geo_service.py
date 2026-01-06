from shapely.geometry import Point, Polygon

def check_point_in_zone(lat, lng, zone_polygon):
    """
    Returns True if driver coordinates are inside the polygon
    zone_polygon: list of {"lat": float, "lng": float}
    """
    poly_points = [(point["lng"], point["lat"]) for point in zone_polygon]
    polygon = Polygon(poly_points)
    return polygon.contains(Point(lng, lat))
