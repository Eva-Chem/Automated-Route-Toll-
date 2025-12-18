from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return {"status": "Backend running"}, 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
