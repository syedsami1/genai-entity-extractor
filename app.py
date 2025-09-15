from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/results", methods=["GET"])
def get_results():
    conn = sqlite3.connect("results.db")
    cursor = conn.cursor()
    cursor.execute("SELECT filename, persons, dates FROM extracted_data")
    rows = cursor.fetchall()
    conn.close()
    results = []
    for row in rows:
        results.append({
            "filename": row[0],
            "persons": row[1].split(",") if row[1] else [],
            "dates": row[2].split(",") if row[2] else []
        })
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
