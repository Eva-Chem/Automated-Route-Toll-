import os
from flask_jwt_extended import jwt_required

def optional_jwt(fn):
    """
    Enforces JWT in production, skips it in development.
    """
    if os.getenv("FLASK_ENV") == "development":
        return fn
    return jwt_required()(fn)
