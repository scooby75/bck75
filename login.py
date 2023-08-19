import streamlit as st
import datetime
import sqlite3
import bcrypt

def create_db():
    # Criar e conectar ao banco de dados
    conn = sqlite3.connect("user_credentials.db")
    cursor = conn.cursor()

    # Criar a tabela se ela ainda não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')

    # Salvar as mudanças e fechar a conexão
    conn.commit()
    conn.close()

def login_page():
    st.image("https://lifeisfootball22.files.wordpress.com/2021/09/data-2.png?w=660", width=240)
    st.title("Football Data Analysis")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    login_button = st.button("Entrar")

    if login_button:
        conn = sqlite3.connect("user_credentials.db")
        cursor = conn.cursor()

        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()

        if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.login_time = datetime.datetime.now()
        else:
            st.error("Credenciais inválidas ou usuário não encontrado.")

        conn.close()

    new_user = st.checkbox("Criar novo usuário")

    if new_user:
        new_username = st.text_input("Novo usuário")
        new_password = st.text_input("Nova senha", type="password")
        confirm_password = st.text_input("Confirmar senha", type="password")

        if new_username and new_password and new_password == confirm_password:
            conn = sqlite3.connect("user_credentials.db")
            cursor = conn.cursor()

            cursor.execute('SELECT username FROM users WHERE username = ?', (new_username,))
            existing_user = cursor.fetchone()

            if existing_user:
                st.error("Este usuário já existe.")
            else:
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (new_username, hashed_password))
                conn.commit()
                st.success("Novo usuário criado com sucesso.")

            conn.close()

def logout():
    st.session_state.logged_in = False
    st.session_state.pop("username", None)
    st.session_state.pop("login_time", None)

def main():
    create_db()
    login_page()

if __name__ == "__main__":
    main()
