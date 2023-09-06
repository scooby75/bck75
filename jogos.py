# jogos.py

import streamlit as st
import pandas as pd
import datetime as dt


from session_state import SessionState

def jogos_do_dia_page():
    # Inicializa o estado da sessão
    session_state = SessionState()

    # Defina o valor de user_profile após a criação da instância
    session_state.user_profile = 1  # Ou qualquer outro valor desejado

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 1:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return

    st.subheader("Jogos do Dia")
    st.text("A base de dados é atualizada diariamente e as odds de referência são da Bet365")

    # Load the data
    @st.cache_data(ttl=23200.0)  # 24 hours in seconds
    def load_base():
        url = "https://github.com/scooby75/bdfootball/blob/main/Jogos_do_Dia_FS.csv?raw=true"
        data_jogos = pd.read_csv(url)

        # Especifique o formato das datas como DD/MM/AAAA
        formato_data = "%d/%m/%Y"

        # Convert the 'Hora' column to a datetime object
        data_jogos['Time'] = pd.to_datetime(data_jogos['Time'], format='%H:%M')
       

        # Criar um intervalo de tempo de 3 horas
        offset_tempo = pd.Timedelta(hours=3)

        # Subtrair o intervalo de tempo da coluna 'Time'
        data_jogos['Time'] = pd.to_datetime(data_jogos['Time'], format='%H:%M') - offset_tempo
        data_jogos['Time'] = data_jogos['Time'].dt.strftime('%H:%M')

        # Rename the columns and process 'Rodada'
        data_jogos.rename(columns={
            'Odd_H': 'FT_Odd_H',
            'Odd_D': 'FT_Odd_D',
            'Odd_A': 'FT_Odd_A',
            'Odd_Over25': 'FT_Odd_Over25',
            'Odd_Under25': 'FT_Odd_Under25',
            'Odd_BTTS_Yes': 'FT_Odd_BTTS_Yes',
            'CS_Goleada_H': 'Lay_Goleada_H',
            'CS_Goleada_A': 'Lay_Goleada_A',
            'League': 'Liga',
            'Time': 'Hora',            
        }, inplace=True)
        
        
        return data_jogos

    df2 = load_base()

    # Define columns to display
    columns_to_display = [
        'Date', 'Hora', 'Liga', 'Home', 'Away', 'Rodada',
        'FT_Odd_H', 'FT_Odd_D', 'FT_Odd_A',
        'FT_Odd_Over25', 'FT_Odd_Under25', 'FT_Odd_BTTS_Yes', 'Lay_Goleada_H', 'Lay_Goleada_A'
    ]

    # Create filters for selected columns
    filter_values = {}
    filter_columns = [
        ('FT Odds Home', 'selected_ft_odd_h'),
        ('FT Odds Draw', 'selected_ft_odd_d'),
        ('FT Odds Away', 'selected_ft_odd_a'),
        ('FT Odds Over 2.5', 'selected_ft_odd_over25'),
        ('FT Odds Under 2.5', 'selected_ft_odd_under25'),
        ('FT Odds BTTS Yes', 'selected_ft_odd_btts_yes'),
        ('Lay Goleada Casa', 'selected_lay_goleada_h'),
        ('Lay Goleada Visitante', 'selected_lay_goleada_a'),
        
    ]

    # Create number inputs for filter conditions
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_ft_odd_h_min = st.number_input("FT Odds Home (min)", 0.0, 10.0, 0.0)
        selected_ft_odd_h_max = st.number_input("FT Odds Home (max)", selected_ft_odd_h_min, 15.0, 15.0)
        selected_ft_odd_d_min = st.number_input("FT Odds Draw (min)", 0.0, 10.0, 0.0)
        selected_ft_odd_d_max = st.number_input("FT Odds Draw (max)", selected_ft_odd_d_min, 15.0, 15.0)
        selected_ft_odd_a_min = st.number_input("FT Odds Away (min)", 0.0, 10.0, 0.0)
        selected_ft_odd_a_max = st.number_input("FT Odds Away (max)", selected_ft_odd_a_min, 15.0, 15.0)

    with col2:
        selected_ft_odd_over25_min = st.number_input("FT Odds Over 2.5 (min)", 0.0, 10.0, 0.0)
        selected_ft_odd_over25_max = st.number_input("FT Odds Over 2.5 (max)", selected_ft_odd_over25_min, 10.0, 10.0)
        selected_ft_odd_under25_min = st.number_input("FT Odds Under 2.5 (min)", 0.0, 10.0, 0.0)
        selected_ft_odd_under25_max = st.number_input("FT Odds Under 2.5 (max)", selected_ft_odd_under25_min, 10.0, 10.0)
        selected_ft_odd_btts_yes_min = st.number_input("FT Odds BTTS Yes (min)", 0.0, 10.0, 0.0)
        selected_ft_odd_btts_yes_max = st.number_input("FT Odds BTTS Yes (max)", selected_ft_odd_btts_yes_min, 10.0, 10.0)

    with col3:
        selected_lay_goleada_h_min = st.number_input("Lay Goleada Casa (min)", 0.0, 50.0, 0.0)
        selected_lay_goleada_h_max = st.number_input("Lay Goleada Casa (max)", 0.0, 50.0, 0.0)
        selected_lay_goleada_a_min = st.number_input("Lay Goleada Visitante (min)", 0.0, 50.0, 0.0)
        selected_lay_goleada_a_max = st.number_input("Lay Goleada Visitante (max)", 0.0, 50.0, 0.0)

    

    # Apply filters to the DataFrame
    filtered_data = df2[
        (df2['FT_Odd_H'] >= selected_ft_odd_h_min) &
        (df2['FT_Odd_H'] <= selected_ft_odd_h_max) &
        (df2['FT_Odd_D'] >= selected_ft_odd_d_min) &
        (df2['FT_Odd_D'] <= selected_ft_odd_d_max) &
        (df2['FT_Odd_A'] >= selected_ft_odd_a_min) &    
        (df2['FT_Odd_A'] <= selected_ft_odd_a_max) &
        (df2['FT_Odd_Over25'] >= selected_ft_odd_over25_min) &
        (df2['FT_Odd_Over25'] <= selected_ft_odd_over25_max) &
        (df2['FT_Odd_Under25'] >= selected_ft_odd_under25_min) &
        (df2['FT_Odd_Under25'] <= selected_ft_odd_under25_max) &
        (df2['FT_Odd_BTTS_Yes'] >= selected_ft_odd_btts_yes_min) &
        (df2['FT_Odd_BTTS_Yes'] <= selected_ft_odd_btts_yes_max) &
        (df2['Lay_Goleada_H'] >= selected_lay_goleada_h_min) &
        (df2['Lay_Goleada_H'] <= selected_lay_goleada_h_max) &
        (df2['Lay_Goleada_A'] >= selected_lay_goleada_a_min) &
        (df2['Lay_Goleada_A'] <= selected_lay_goleada_a_max) 
    ]

    if not filtered_data.empty:
        sorted_filtered_data = filtered_data.sort_values(by='Hora')
        st.dataframe(sorted_filtered_data[columns_to_display])
    else:
        st.warning("Não existem jogos com esses critérios!")

# Chamar a função para exibir a aplicação web
jogos_do_dia_page()
