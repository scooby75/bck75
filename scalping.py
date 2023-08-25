import streamlit as st
import pandas as pd
import re
from session_state import SessionState

def extrair_numero_rodada(text):
    if isinstance(text, int):
        return text
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    return None

def scalping_page():
    # Inicializa o estado da sessão
    session_state = SessionState(user_profile=3)

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 3:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return

    # Definir URLs para os arquivos CSV
    url_jogosdodia = 'https://github.com/scooby75/bdfootball/blob/main/Jogos_do_Dia_FS.csv?raw=true'

    try:
        # Carregar dados CSV
        jogosdodia = pd.read_csv(url_jogosdodia)
        
        # Extrair número da rodada
        jogosdodia["Rodada_Num"] = jogosdodia["ROUND"].apply(extrair_numero_rodada)

        # Filtrar jogos com critérios específicos
        filtered_games = jogosdodia[
            (jogosdodia['0_15_mar_home'] == 0) & (jogosdodia['0_15_sofri_home'] == 0) &
            (jogosdodia['0_15_mar_away'] == 0) & (jogosdodia['0_15_sofri_away'] == 0)
        ]

        # Extrair número da rodada e filtrar com condição
        filtered_games = filtered_games[filtered_games["Rodada_Num"] >= 5]

        # Selecionar colunas relevantes e renomear
        result_df = filtered_games[['Home', 'Away', 'FT_Odd_H', 'FT_Odd_A', 'FT_Odd_Over25']]

        # App Streamlit
        st.subheader("Lay Over 25FT")
        st.text("Apostar em Lay Over 25FT e fechar posição com 3% ou 5min de exposição.")
        st.dataframe(result_df)

    except Exception as e:
        st.error("Ocorreu um erro: " + str(e))

# Chamar a função para iniciar o aplicativo Streamlit
scalping_page()
