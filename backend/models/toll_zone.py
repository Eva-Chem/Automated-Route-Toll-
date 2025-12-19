from db.database import get_db_connection

def fetch_all_toll_zones():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, charge_amount, polygon
        FROM toll_zones
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    zones = []
    for row in rows:
        zones.append({
            "id": row[0],
            "name": row[1],
            "charge_amount": float(row[2]),
            "polygon": row[3]
        })

    return zones
