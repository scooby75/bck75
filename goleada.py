import streamlit as st
import pandas as pd
import re

from session_state import get_or_create_session_state

# Função para extrair o número do texto "ROUND N"
def extrair_numero_rodada(text):
    if isinstance(text, int):
        return text
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    return None

def load_base():
    url = "https://github.com/scooby75/bdfootball/blob/main/Jogos_do_Dia_FS.csv?raw=true"
    df = pd.read_csv(url)  # Carregar os dados do CSV
    
    # Converter a coluna 'Date' para um objeto de data
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')
    
    # Converter a coluna 'Time' para um objeto de hora
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M')
    
    # Subtrair 3 horas da coluna 'Time'
    df['Time'] = df['Time'] - pd.DateOffset(hours=3)
    
    # Formatar a coluna 'Time' no formato HH:MM
    df['Time'] = df['Time'].dt.strftime('%H:%M')
    
    # Rename the columns
    df.rename(columns={
        'FT_Odd_H': 'FT_Odd_H',
        'FT_Odd_D': 'FT_Odd_D',
        'FT_Odd_A': 'FT_Odd_A',
        'FT_Odd_Over25': 'FT_Odd_Over25',
        'FT_Odd_Under25': 'FT_Odd_Under25',
        'Odds_BTTS_Yes': 'FT_Odd_BTTS_Yes',        
        'ROUND': 'Rodada',
        'Time': 'Hora',
    }, inplace=True)

    # Apply the function to extract the round number and create a new column "Rodada_Num"
    df["Rodada_Num"] = df["Rodada"].apply(extrair_numero_rodada)

    return df

def goleada_page():
    # Inicializa o estado da sessão
    session_state = get_or_create_session_state(user_profile=3)

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 3:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return   

    # Load the data
    df = load_base()

    # Filtrando os jogos com valores de "FT_Odd_H" entre 1.40 e 2.0 e "Rodada_Num" maior ou igual a 10
    eventos_raros_df = df[(df["FT_Odd_H"] >= 1.71) & (df["FT_Odd_H"] <= 2.4) & (df["FT_Odd_Over25"] >= 2.01) & (df["Rodada_Num"] >= 10)]

    # Exibir o dataframe "Eventos Raros"
    st.subheader("Lay Goleada Casa")
    st.text("Apostar em Lay Goleada Casa, Odd máxima 30")
    display_columns = ["Date", "Hora", "League", "Home", "Away"]  # Columns to display
    st.dataframe(eventos_raros_df[display_columns])

    # Filtrando os jogos com valores de "FT_Odd_A" entre 1.40 e 2.0 e "Rodada_Num" maior ou igual a 10
    eventos_raros2_df = df[(df["FT_Odd_A"] >= 1.71) & (df["FT_Odd_A"] <= 2.4) & (df["FT_Odd_Over25"] >= 2.01) & (df["Rodada_Num"] >= 10)]
    
    # Exibir o dataframe "Eventos Raros"
    st.subheader("Lay Goleada Visitante")
    st.text("Apostar em Lay Goleada Visitante, Odd máxima 30")
    st.dataframe(eventos_raros2_df[display_columns])

# Chamar a função para iniciar o aplicativo
goleada_page()
