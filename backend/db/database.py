import psycopg2
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:Group5@localhost:5432/toll_tracker"
)

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS toll_zones (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            charge_amount NUMERIC(10,2) NOT NULL,
            polygon JSONB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Insert sample data if table is empty
    cur.execute("SELECT COUNT(*) FROM toll_zones;")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO toll_zones (name, charge_amount, polygon)
            VALUES (
                'CBD Toll Zone',
                200.00,
                '[
                    {"lat": -1.2921, "lng": 36.8219},
                    {"lat": -1.2925, "lng": 36.8225},
                    {"lat": -1.2930, "lng": 36.8220},
                    {"lat": -1.2921, "lng": 36.8219}
                ]'::jsonb
            );
        """)

    conn.commit()
    cur.close()
    conn.close()
