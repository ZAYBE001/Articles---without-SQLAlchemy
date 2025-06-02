# setup_db.py
import sqlite3

def initialize_database():
    conn = sqlite3.connect("magazine.db")
    with open("schema.sql") as f:
        conn.executescript(f.read())
    conn.close()

if __name__ == "__main__":
    initialize_database()
