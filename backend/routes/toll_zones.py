from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from middlewares import admin_required
from db import get_db_connection

toll_zones_bp = Blueprint("toll_zones", __name__)

@toll_zones_bp.route("/", methods=["GET"])
@jwt_required()
def get_toll_zones():
    """Get all toll zones - accessible by admin and operator"""
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


@toll_zones_bp.route("/", methods=["POST"])
@jwt_required()
@admin_required
def create_toll_zone():
    """Create new toll zone - admin only"""
    data = request.get_json()
    
    if not data or "name" not in data or "charge_amount" not in data or "polygon" not in data:
        return jsonify({"error": "Missing required fields: name, charge_amount, polygon"}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO toll_zones (name, charge_amount, polygon)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (data["name"], data["charge_amount"], data["polygon"]))
    
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({
        "message": "Toll zone created successfully",
        "id": new_id,
        "name": data["name"],
        "charge_amount": data["charge_amount"]
    }), 201


@toll_zones_bp.route("/<int:zone_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_toll_zone(zone_id):
    """Update toll zone - admin only"""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Check if zone exists
    cur.execute("SELECT id FROM toll_zones WHERE id = %s;", (zone_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({"error": "Toll zone not found"}), 404
    
    # Update the zone
    cur.execute("""
        UPDATE toll_zones 
        SET name = COALESCE(%s, name),
            charge_amount = COALESCE(%s, charge_amount),
            polygon = COALESCE(%s, polygon)
        WHERE id = %s
    """, (data.get("name"), data.get("charge_amount"), data.get("polygon"), zone_id))
    
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "Toll zone updated successfully", "id": zone_id}), 200


@toll_zones_bp.route("/<int:zone_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_toll_zone(zone_id):
    """Delete toll zone - admin only"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Check if zone exists
    cur.execute("SELECT id FROM toll_zones WHERE id = %s;", (zone_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({"error": "Toll zone not found"}), 404
    
    # Delete the zone
    cur.execute("DELETE FROM toll_zones WHERE id = %s;", (zone_id,))
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "Toll zone deleted successfully", "id": zone_id}), 200
