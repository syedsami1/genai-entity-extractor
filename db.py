import sqlite3

def init_db():
    conn = sqlite3.connect("results.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS extracted_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            persons TEXT,
            dates TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_data(filename, persons, dates):
    conn = sqlite3.connect("results.db")
    cursor = conn.cursor()

    # Check if file already exists
    cursor.execute("SELECT id FROM extracted_data WHERE filename = ?", (filename,))
    if cursor.fetchone():
        conn.close()
        print(f"⚠️ Skipped duplicate: {filename}")
        return

    cursor.execute("""
        INSERT INTO extracted_data (filename, persons, dates)
        VALUES (?, ?, ?)
    """, (filename, ",".join(persons), ",".join(dates)))
    conn.commit()
    conn.close()
