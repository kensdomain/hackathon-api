import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DB = "app.db"

# opens the connection to your database file (app.db). SQLite creates this file for you.
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS items "
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)"
    )
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return jsonify({"message": "hello"})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/items", methods=["GET"])
def get_items():
    conn = get_db()
    rows = conn.execute("SELECT * FROM items").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/items", methods=["POST"])
def add_item():
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "name is required"}), 400
    conn = get_db()
    cur = conn.execute("INSERT INTO items (name) VALUES (?)", (data["name"],))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify({"id": new_id, "name": data["name"]}), 201

if __name__ == "__main__":
    init_db()
    app.run(debug=True)