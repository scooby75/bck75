import streamlit as st
import datetime
import psycopg2
import bcrypt

def create_db():
    conn = psycopg2.connect(
        host="containers-us-west-64.railway.app",
        database="login",
        user="postgres",
        password="Kamk5HXHc9hcQsjsA4f2"
    )
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')

    conn.commit()
    conn.close()

def login_page():
    st.image("https://lifeisfootball22.files.wordpress.com/2021/09/data-2.png?w=660", width=240)
    st.title("Football Data Analysis")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    login_button = st.button("Entrar")

    if login_button:
        conn = psycopg2.connect(
            host="containers-us-west-64.railway.app",
            database="login",
            user="postgres",
            password="Kamk5HXHc9hcQsjsA4f2"
        )
        cursor = conn.cursor()

        cursor.execute('SELECT password FROM users WHERE username = %s', (username,))
        result = cursor.fetchone()

        if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.login_time = datetime.datetime.now()
        else:
            st.error("Credenciais inválidas ou usuário não encontrado.")

        conn.close()

    # Restante da função...

def logout():
    st.session_state.logged_in = False
    st.session_state.pop("username", None)
    st.session_state.pop("login_time", None)

def main():
    create_db()
    login_page()

if __name__ == "__main__":
    main()
