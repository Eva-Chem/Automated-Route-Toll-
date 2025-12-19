from shapely.geometry import Point, Polygon

def is_point_inside_zone(lat, lng, polygon):
    polygon_points = [
        (point["lng"], point["lat"])
        for point in polygon
    ]

    zone_polygon = Polygon(polygon_points)
    vehicle_point = Point(lng, lat)

    return zone_polygon.contains(vehicle_point)
