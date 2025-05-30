from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
DB_FILE = "db_simple.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/open", methods=["POST"])
def zaznam_otvorenia():
    data = request.get_json()
    meno = data.get("meno", "neznamy")
    cas = datetime.now().isoformat()

    db = load_db()
    db[meno] = {
        "status": "otvoril",
        "cas": cas
    }
    save_db(db)

    print(f"📥 Používateľ '{meno}' otvoril script v {cas}")
    return jsonify({"ok": True}), 200

@app.route("/zaznamy", methods=["GET"])
def get_all_users():
    return jsonify(load_db())

@app.route("/")
def index():
    return "Server beží"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
