#!/usr/bin/env python
"""Show toll zones from database"""
import sys
sys.path.insert(0, '/home/riyan/development/code/Automated-Route-Toll-/backend')

from db.database import get_db_connection

conn = get_db_connection()
cur = conn.cursor()

print("\n=== TOLL ZONES ===\n")
cur.execute("SELECT id, name, charge_amount, polygon FROM toll_zones;")
rows = cur.fetchall()

for row in rows:
    print(f"ID: {row[0]}")
    print(f"Name: {row[1]}")
    print(f"Charge: KES {row[2]}")
    print(f"Polygon: {row[3]}")
    print("-" * 40)

cur.close()
conn.close()

