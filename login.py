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

def login_page():
    st.image("https://lifeisfootball22.files.wordpress.com/2021/09/data-2.png?w=660")
    st.title("Football Data Analysis")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    login_button = st.button("Entrar")

    if login_button:
        if username in valid_users and valid_users[username]["password"] == password:
            # Check if user is already logged in
            if username in active_users:
                st.error("Esse usuário já está logado em outro dispositivo.")
                return

            # Store user's session ID and last activity time
            active_users[username] = datetime.datetime.now()
            user_profile = valid_users[username]["profile"]
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.user_profile = user_profile
        else:
            st.error("Credenciais inválidas.")

def logout(username):
    # Restante do seu código para a função logout

def check_session_timeout():
    # Restante do seu código para verificar o timeout da sessão

if __name__ == "__main__":
    initialize_database()
    st.timer(interval=60, key="session_timeout_check")
