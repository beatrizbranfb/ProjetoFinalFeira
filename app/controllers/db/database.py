from config import DATABASE
import sqlite3


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        with open('app/controllers/db/schema.sql', mode='r') as a:
            db.cursor().executescript(a.read())
        db.commit()

if __name__ == "__main__":
    init_db()
    print(".")
