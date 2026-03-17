import sqlite3

DB_NAME = "books.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        genre TEXT,
        year INTEGER,
        description TEXT,
        is_read INTEGER DEFAULT 0,
        is_favorite INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()
