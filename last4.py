import streamlit as st
import pandas as pd
import io
import requests

from session_state import SessionState

def last4_page():
    # Inicializa o estado da sessão
    session_state = SessionState()

    # Defina o valor de user_profile após a criação da instância
    session_state.user_profile = 2  # Ou qualquer outro valor desejado

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 2:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return

    # Fazer o download do arquivo CSV da URL
    url = "https://raw.githubusercontent.com/scooby75/bdfootball/main/last4_geral.csv"
    response = requests.get(url)
    data = response.content.decode("utf-8")

    # Carregar o CSV em um dataframe
    df = pd.read_csv(io.StringIO(data))

    # Renomear as colunas
    df.rename(columns={'GF': 'Gols_Feitos', 'GA': 'Gols_Tomados', 'GD': 'Saldo_Gols'}, inplace=True)

    # Filtrar as equipes com 4 vitórias para o "Top Equipes"
    top_equipes = df[df['W'] == 4]

    # Filtrar as equipes com 0 vitórias para o "Piores Equipes"
    piores_equipes = df[df['W'] == 0]

    # Criar um aplicativo Streamlit
    st.title("Top e Piores Equipes de Futebol")

    # Exibir "Top Equipes" em uma tabela interativa
    st.subheader("Top Equipes:")
    st.dataframe(top_equipes[["Equipe", "Gols_Feitos", "Gols_Tomados", "Saldo_Gols"]])

    # Exibir "Piores Equipes" em uma tabela interativa
    st.subheader("Piores Equipes:")
    st.dataframe(piores_equipes[["Equipe", "Gols_Feitos", "Gols_Tomados", "Saldo_Gols"]])

# Chamar a função para iniciar o aplicativo
last4_page()
