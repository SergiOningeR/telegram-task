import sqlite3

def get_connection():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            comment TEXT,
            phone TEXT,
            urgency TEXT,
            status TEXT,
            creator_id INTEGER,
            creator_name TEXT,
            finish_comment TEXT,
            photo_id TEXT
        )
    """)
    conn.commit()
    conn.close()