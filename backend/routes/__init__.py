# Routes package
from routes.auth import auth_bp
from routes.toll_zones import toll_zones_bp
from routes.geo_fencing import geo_fencing_bp
from routes.admin import admin_bp
from routes.mpesa import mpesa_bp

__all__ = ['auth_bp', 'toll_zones_bp', 'geo_fencing_bp', 'admin_bp', 'mpesa_bp']

