import sqlite3

conn = sqlite3.connect("data.db")

c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        white_player TEXT,
        white_rating INTEGER,
        black_player TEXT,
        black_rating INTEGER,
        result TEXT,
        time_control TEXT,
        year INTEGER,
        month INTEGER, 
        url TEXT UNIQUE
    )
""")

conn.commit()

