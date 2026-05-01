import sqlite3

conn = sqlite3.connect("chatbot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT,
    route TEXT,
    latency REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

def insert_log(query, route, latency):
    cursor.execute(
        "INSERT INTO logs (query, route, latency) VALUES (?, ?, ?)",
        (query, route, latency)
    )
    conn.commit()

def get_logs():
    cursor.execute("SELECT * FROM logs")
    return cursor.fetchall()