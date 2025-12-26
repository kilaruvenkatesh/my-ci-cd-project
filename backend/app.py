from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # VERY IMPORTANT

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/ready")
def ready():
    db_host = os.getenv("DB_HOST", "not_set")
    return jsonify({"ready": True, "db_host": db_host}), 200

@app.route("/api/test")
def test_api():
    return jsonify({"message": "API working fine!"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
