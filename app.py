import streamlit as st
from login import login_page, logout
from jogos import jogos_do_dia_page
from cs import cs_page
from predict import predict_page
from ha_025 import ha_025_page
from lay_zebra import lay_zebra_page
from zebra_ft import zebra_ft_page
from scalping import scalping_page
from session_state import session_state

def main():
    # Inicializa o estado da sessão
    session_state = SessionState(user_profile=0)  # Defina o valor do user_profile conforme necessário
    if not hasattr(st.session_state, "logged_in"):
        st.session_state.logged_in = False

    # Verifica se o usuário está logado ou não
    if not st.session_state.logged_in:
        login_page()
    else:
        # Barra lateral com imagem e informações
        st.sidebar.image("https://lifeisfootball22.files.wordpress.com/2021/09/data-2.png?w=660")
        st.sidebar.header("Football Data Analysis")
        
        # Mostra informações do usuário e botão de logout na barra lateral
        st.sidebar.write(f"Logado como: {st.session_state.username}")
        if st.sidebar.button("Logout", key="logout_button"):
            logout()

         # Caixa de seleção para diferentes páginas
        selected_tab = st.sidebar.selectbox("Selecione uma aba", ["Jogos do Dia", "Dutching", "HA", "Lay Goleada", "Lay Zebra HT", "Lay Zebra FT", "Predict", "Scalping"])

        # Exibe o conteúdo da página selecionada, considerando as permissões do perfil
        user_profile = st.session_state.user_profile
        
        if selected_tab == "Jogos do Dia":
            jogos_do_dia_page()
        elif selected_tab == "Dutching":
            cs_page()
        elif selected_tab == "HA" and user_profile >= 2:
            ha_025_page()
        elif selected_tab == "Lay Goleada" and user_profile >= 2:
            goleada_page()
        elif selected_tab == "Lay Zebra HT" and user_profile >= 2:
            lay_zebra_page()
        elif selected_tab == "Predict" and user_profile >= 3:
            predict_page()
        elif selected_tab == "Lay Zebra FT"and user_profile >= 2:
            zebra_ft_page()
        elif selected_tab == "Scalping" and user_profile >= 3:
            scalping_page()
       

if __name__ == "__main__":
    main()
