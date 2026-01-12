from shapely.geometry import Point, Polygon

def check_point_in_zone(lat, lng, polygon_coords):
    try:
        point = Point(lat, lng)
        coords = [(c["lat"], c["lng"]) for c in polygon_coords]
        polygon = Polygon(coords)
        return polygon.contains(point) or polygon.touches(point)
    except Exception as e:
        print("Geo-fencing error:", e)
        return False