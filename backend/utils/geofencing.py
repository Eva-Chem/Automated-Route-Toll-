def point_in_polygon(lat, lng, polygon):
    inside = False
    n = len(polygon)
    j = n - 1

    for i in range(n):
        x1, y1 = polygon[i]["lat"], polygon[i]["lng"]
        x2, y2 = polygon[j]["lat"], polygon[j]["lng"]

        intersects = ((y1 > lng) != (y2 > lng)) and \
                     (lat < (x2 - x1) * (lng - y1) / ((y2 - y1) or 1e-9) + x1)

        if intersects:
            inside = not inside

        j = i

    return inside

