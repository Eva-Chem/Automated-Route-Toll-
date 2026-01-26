from shapely.geometry import Point, Polygon

def check_point_in_zone(lat, lng, polygon_coords):
    point = Point(lng, lat)  # x = lng, y = lat
    polygon = Polygon([(lng, lat) for lat, lng in polygon_coords])
    return polygon.contains(point)
