import sqlite3

DB_PATH = "data/chat_history.db"


def initialize_database():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
def get_history():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT role, message
    FROM chats
    ORDER BY id DESC
    LIMIT 20
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows
def get_recent_messages(limit=10):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT role, message
    FROM chats
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    rows.reverse()

    return rows
def save_message(role, message):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chats(role,message)
        VALUES(?,?)
        """,
        (role, message)
    )

    conn.commit()
    conn.close()