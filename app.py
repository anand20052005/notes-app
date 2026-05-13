from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Create database table
def init_db():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/api/notes", methods=["GET"])
def get_notes():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()

    conn.close()

    return jsonify(notes)

@app.route("/api/notes", methods=["POST"])
def add_note():
    data = request.json
    content = data.get("content")

    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notes (content) VALUES (?)",
        (content,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Note added"})

@app.route("/")
def home():
    return open("index.html").read()

if __name__ == "__main__":
    app.run(debug=True)