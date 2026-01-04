#!/usr/bin/env python
"""Show all database tables"""
import sys
sys.path.insert(0, '/home/riyan/development/code/Automated-Route-Toll-/backend')

from db.database import get_db_connection

conn = get_db_connection()
cur = conn.cursor()

print("=== TOLL ZONES ===\n")
cur.execute("SELECT id, name, charge_amount, polygon FROM toll_zones;")
rows = cur.fetchall()
for row in rows:
    print(f"ID: {row[0]}")
    print(f"Name: {row[1]}")
    print(f"Charge: KES {row[2]}")
    print(f"Polygon: {row[3]}")
    print("-" * 40)

print("\n=== USERS ===\n")
cur.execute("SELECT id, username, role, created_at FROM users;")
rows = cur.fetchall()
for row in rows:
    print(f"ID: {row[0]}")
    print(f"Username: {row[1]}")
    print(f"Role: {row[2]}")
    print(f"Created: {row[3]}")
    print("-" * 40)

print("\n=== TRANSACTIONS ===\n")
cur.execute("SELECT id, phone, amount, status, created_at FROM transactions;")
rows = cur.fetchall()
if rows:
    for row in rows:
        print(f"ID: {row[0]}, Phone: {row[1]}, Amount: KES {row[2]}, Status: {row[3]}, Created: {row[4]}")
        print("-" * 40)
else:
    print("No transactions yet")

cur.close()
conn.close()

