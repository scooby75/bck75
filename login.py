# login.py
import sqlite3

DATABASE_FILE = "user_sessions.db"

def initialize_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            last_activity TIMESTAMP,
            active INTEGER
        )
    """)
    conn.commit()
    conn.close()

def login(username):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO users (username, last_activity, active) VALUES (?, datetime('now'), 1)", (username,))
    conn.commit()
    conn.close()

def logout(username):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET active = 0 WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def check_session_timeout():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET active = 0 WHERE strftime('%s', datetime('now')) - strftime('%s', last_activity) > ?", (SESSION_TIMEOUT,))
    conn.commit()
    conn.close()

def main():
    initialize_database()
    st.timer(interval=60, key="session_timeout_check")
    login_page()

if __name__ == "__main__":
    main()
