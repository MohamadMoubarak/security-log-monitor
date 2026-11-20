import sqlite3

DB_PATH = "monitor.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_tables():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT NOT NULL,
                status TEXT NOT NULL,
                username TEXT NOT NULL,
                ip TEXT NOT NULL,
                port INTEGER NOT NULL
                )
            """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS alerts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT NOT NULL,
                failures INTEGER NOT NULL,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL
                )
            """)

def clear_tables():
    with get_connection() as conn:
        conn.execute("DELETE FROM events")
        conn.execute("DELETE FROM alerts")

def save_events(events):
    rows = [
        (e["time"],e["status"],e["user"], e["ip"], e["port"])
        for e in events
    ]
    with get_connection() as conn:
        conn.executemany(
            "INSERT INTO events (time, status, username, ip, port) VALUES (?, ?, ?, ?, ?)",
            rows,
        )

def save_alerts(alerts):
    rows = [
        (a["ip"], a["failures"], a["first_seen"].isoformat(), a["last_seen"].isoformat())
        for a in alerts
    ]
    with get_connection() as conn:
        conn.executemany(
            "INSERT INTO alerts (ip, failures, first_seen, last_seen) VALUES (?, ?, ?, ?)",
            rows,
        )


def fetch_all(sql, params=()):
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(sql, params).fetchall()
    return [dict(row) for row in rows]

def get_events():
    return fetch_all("SELECT * FROM events ORDER BY id")

def get_alerts():
    return fetch_all("SELECT * FROM alerts ORDER BY id")

def get_events_by_status(status: str | None = None):
    
    if status is not None:
            return fetch_all("SELECT * FROM events WHERE status = ? ORDER BY id", (status,))
    return fetch_all("SELECT * FROM events ORDER BY id")

