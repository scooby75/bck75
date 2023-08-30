# login.py
import sqlite3
import datetime

# Database file
DATABASE_FILE = "user_sessions.db"

# Session timeout in seconds (30 minutes)
SESSION_TIMEOUT = 30 * 60

def initialize_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users_credentials (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS active_users (
            username TEXT PRIMARY KEY,
            last_activity TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users_credentials(username)
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users_credentials (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def login(username):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO active_users (username, last_activity) VALUES (?, datetime('now'))", (username,))
    conn.commit()
    conn.close()

def logout(username):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM active_users WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def check_session_timeout():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM active_users WHERE strftime('%s', datetime('now')) - strftime('%s', last_activity) > ?", (SESSION_TIMEOUT,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    st.timer(interval=60, key="session_timeout_check")
