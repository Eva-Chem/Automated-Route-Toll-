from flask import Flask, jsonify
from flask_cors import CORS
<<<<<<< HEAD
=======
from db.database import init_db, get_db_connection
>>>>>>> 80d0f6c (Backend: Flask app, PostgreSQL setup, toll zones API, cleanup)

app = Flask(__name__)
CORS(app)

# Initialize database (creates tables + sample data)
init_db()

<<<<<<< HEAD
    # Health check route
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "ok",
            "message": "Backend running"
        }), 200
=======
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Automated Route Toll Backend is running"})

>>>>>>> 80d0f6c (Backend: Flask app, PostgreSQL setup, toll zones API, cleanup)

@app.route("/toll-zones", methods=["GET"])
def get_toll_zones():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name, charge_amount, polygon FROM toll_zones;")
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

    return jsonify(zones)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
