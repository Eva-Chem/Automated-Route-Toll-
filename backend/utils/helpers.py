# backend/utils/helpers.py
from shapely.geometry import Point, Polygon

def is_point_inside_zone(lat, lng, polygon_coords):
    points = [(p["lng"], p["lat"]) for p in polygon_coords]
    poly = Polygon(points)
    return poly.contains(Point(lng, lat))
