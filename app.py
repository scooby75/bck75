import streamlit as st

# Dados de exemplo para simular o login (substitua por um mecanismo seguro em um ambiente de produção)
valid_users = {
    "usuario1": "senha123",
    "usuario2": "senha456"
}

def login_page():
    st.title("Página de Login")
    username = st.text_input("Nome de usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if username in valid_users and valid_users[username] == password:
            st.success("Login bem-sucedido!")
            return True
        else:
            st.error("Credenciais inválidas.")
    return False

def jogos_do_dia_page():
    st.title("Jogos do Dia")
    # Coloque aqui a lógica e o conteúdo da página de jogos do dia

def cs_page():
    st.title("CS")
    # Coloque aqui a lógica e o conteúdo da página de CS

def tips_page():
    st.title("Tips")
    # Coloque aqui a lógica e o conteúdo da página de Tips

def main():
    st.set_page_config(page_title="Meu Sistema", layout="wide")
    if login_page():
        st_tabs = st.tabs(["Jogos do Dia", "CS", "Tips"])
        if st_tabs == "Jogos do Dia":
            jogos_do_dia_page()
        elif st_tabs == "CS":
            cs_page()
        elif st_tabs == "Tips":
            tips_page()

if __name__ == "__main__":
    main()
