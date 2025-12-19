import psycopg2
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/toll_tracker"
)

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)
