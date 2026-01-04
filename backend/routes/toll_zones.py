from flask import Blueprint, jsonify
from db import get_db_connection

toll_zones_bp = Blueprint("toll_zones", __name__)

@toll_zones_bp.route("/", methods=["GET"])
def get_toll_zones():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name, charge_amount, polygon FROM toll_zones;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    zones = [
        {
            "id": row[0],
            "name": row[1],
            "charge_amount": float(row[2]),
            "polygon": row[3]
        }
        for row in rows
    ]

    return jsonify(zones), 200
