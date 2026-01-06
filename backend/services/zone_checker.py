from models.models import TollZone
from utils.geofencing import point_in_polygon


def check_driver_zone(lat, lng):
    """
    Checks whether driver coordinates fall inside any active toll zone.
    """
    zones = TollZone.query.filter_by(is_active=True).all()

    for zone in zones:
        if point_in_polygon(lat, lng, zone.polygon_coords):
            return {
                "inside": True,
                "zone_id": str(zone.zone_id),
                "zone_name": zone.zone_name,
                "charge_amount": zone.charge_amount
            }

    return {"inside": False}
