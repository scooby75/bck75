import streamlit as st
import pandas as pd
import re

from session_state import SessionState

def zebra_ft_page():
    # Inicializa o estado da sessão
    session_state = SessionState(user_profile=2)

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 2:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return
    # URL do arquivo CSV
### Lay Zebra FT ####

# URL do arquivo CSV
    # Load the data
    #@st.cache_data(ttl=86400.0)  # 24 hours in seconds
    def load_base():
        url = "https://github.com/scooby75/bdfootball/blob/main/Jogos_do_Dia_FS.csv?raw=true"
        
        df = pd.read_csv(url)
        
        # Convert the 'Hora' column to a datetime object
        df['Time'] = pd.to_datetime(df['Time'])
        
        # Convert the game times to the local time zone (subtracting 3 hours)
        df['Time'] = df['Time'] - pd.to_timedelta('3 hours')

        # Rename the columns
        df.rename(columns={
            'FT_Odds_H': 'FT_Odd_H',
            'FT_Odds_D': 'FT_Odd_D',
            'FT_Odds_A': 'FT_Odd_A',
            'FT_Odds_Over25': 'FT_Odd_Over25',
            'FT_Odds_Under25': 'FT_Odd_Under25',
            'Odds_BTTS_Yes': 'FT_Odd_BTTS_Yes',        
            'ROUND': 'Rodada',
        }, inplace=True)

        # Apply the function to extract the round number and create a new column "Rodada_Num"
        df["Rodada_Num"] = df["Rodada"].apply(extrair_numero_rodada)

        return df

    # Função para extrair o número do texto "ROUND N"
    def extrair_numero_rodada(text):
        if isinstance(text, int):
            return text
        match = re.search(r'\d+', text)
        if match:
            return int(match.group())
        return None

    # Call the load_base function to load the data
    df = load_base()

# Filtrando os jogos com valores de "FT_Odd_H" eh menor que 1.50 e "Round_Num" maior ou igual a 10
    layzebraft_df = df[
    (df["FT_Odd_H"] >= 1.4) & (df["FT_Odd_H"] <= 2.1) &
    (df["FT_Odd_A"] >= 5) & (df["FT_Odd_A"] <= 10) &
    (df["Rodada_Num"] >= 10)
    ]

# Selecionar apenas as colunas desejadas: Date, Time, League, Home e Away
    colunas_desejadas = ["Date", "Time", "League", "Home", "Away"]
    layzebraft_df = layzebraft_df[colunas_desejadas]

# Exibir o dataframe "Lay Zebra FT"
    st.subheader("Lay Zebra FT")
    st.text("Apostar em Lay visitante, Odd máxima 6")
    st.dataframe(layzebraft_df)


# Chamar a função para iniciar o aplicativo
zebra_ft_page()

    

