# login.py
import streamlit as st
import datetime
from session_state import get_or_create_session_state

# Dictionary to track active users and their session IDs
active_users = {}

# Session timeout in seconds (30 minutes)
SESSION_TIMEOUT = 120 * 60

valid_users = {
    "lsilveira": {"password": "senha123", "profile": 3},
    "lamaral": {"password": "lamaral23", "profile": 1},
    "blamim": {"password": "lamim23", "profile": 3},
    "mrodrigues": {"password": "mrodrigues23", "profile": 3},
    "user3": {"password": "password3", "profile": 3}
}

def login_page():
    st.image("https://lifeisfootball22.files.wordpress.com/2021/09/data-2.png?w=660", width=240)
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

            session_state = get_or_create_session_state()
            session_state.logged_in = True
            session_state.username = username
            session_state.login_time = datetime.datetime.now()
            session_state.user_profile = valid_users[username]["profile"]

            # Store user's session ID
            active_users[username] = session_state.session_id
        else:
            st.error("Credenciais inválidas.")

def logout():
    session_state = get_or_create_session_state()
    username = session_state.username

    # Remove user from active_users dictionary
    if username in active_users:
        active_users.pop(username)

    # Clear session state
    session_state.logged_in = False
    session_state.pop("username", None)
    session_state.pop("login_time", None)
    session_state.pop("user_profile", None)

# Check for session timeouts and remove inactive users
def check_session_timeout():
    current_time = datetime.datetime.now()
    users_to_remove = []

    for username, last_activity in active_users.items():
        if (current_time - last_activity).seconds > SESSION_TIMEOUT:
            users_to_remove.append(username)

    for username in users_to_remove:
        active_users.pop(username)

# Call this function periodically, e.g., every minute
check_session_timeout()
session_state = get_or_create_session_state()
session_state.logged_in = False
session_state.pop("username", None)
session_state.pop("login_time", None)
session_state.pop("user_profile", None)  # Clear user profile on logout
