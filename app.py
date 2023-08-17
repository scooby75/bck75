import streamlit as st
from pages import login, page1, page2, page3

# Função principal
def main():
    st.set_page_config(page_title="Controle de Acesso", layout="wide")

    if not st.session_state.logged_in:
        st.session_state.logged_in = login.login()

    if st.session_state.logged_in:
        st.write("Menu de Navegação")
        page = st.selectbox("Selecione a página", ["Página 1", "Página 2", "Página 3"])

        if page == "Página 1":
            page1.show_content()
        elif page == "Página 2":
            page2.show_content()
        elif page == "Página 3":
            page3.show_content()

if __name__ == "__main__":
    main()

