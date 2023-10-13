# value_bets.py

import streamlit as st
import pandas as pd
import re


from session_state import SessionState

def value_bets_page():
    # Inicializa o estado da sessão
    session_state = SessionState()

    # Defina o valor de user_profile após a criação da instância
    session_state.user_profile = 2  # Ou qualquer outro valor desejado

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 2:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return

    # Carrega o dado
    url = "https://raw.githubusercontent.com/scooby75/bdfootball/main/value%20bet.csv"
    df = pd.read_csv(url)

    # Remover a coluna "Data" do DataFrame
    df = df.drop(columns=["Data"])  
        
    
    # Display the "Value Bets" DataFrame
    st.subheader("Value Bets")
    st.text("Se a Odd ofertada é maior que o valor esperado, a tendência é ser lucrativo a longo prazo")
    st.dataframe(df)

# Chamar a função para exibir a aplicação web
value_bets_page()
