import streamlit as st
import pandas as pd
import datetime as dt

def jogos_do_dia_page():
    st.subheader("Jogos do Dia")
    st.text("A base de dados é atualizada diariamente e as odds de referência são da Bet365")

    # Load the data
    @st.cache_data(ttl=86400.0)  # 24 hours in seconds
    def load_base():
        url = "https://github.com/scooby75/bdfootball/blob/main/jogos_do_dia.xlsx?raw=true"
        data_jogos = pd.read_excel(url)

        # Rename the columns and process 'Rodada'
        data_jogos.rename(columns={
            'FT_Odds_H': 'FT_Odd_H',
            'FT_Odds_D': 'FT_Odd_D',
            'FT_Odds_A': 'FT_Odd_A',
            'FT_Odds_Over25': 'FT_Odd_Over25',
            'FT_Odds_Under25': 'FT_Odd_Under25',
            'Odds_BTTS_Yes': 'FT_Odd_BTTS_Yes',
            'ROUND': 'Rodada',
        }, inplace=True)
        data_jogos['Rodada'] = data_jogos['Rodada'].str.replace('ROUND', '').str.strip()

        return data_jogos

    df2 = load_base()

    # Define columns to display
    columns_to_display = [
        'Date', 'Time', 'Country', 'Paises', 'Home', 'Away', 'Rodada',
        'FT_Odd_H', 'FT_Odd_D', 'FT_Odd_A',
        'FT_Odd_Over25', 'FT_Odd_Under25', 'FT_Odd_BTTS_Yes'
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
        ('Rodada', 'selected_rodada')
    ]

    # Create number inputs for filter conditions
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_ft_odd_h_min = st.number_input("FT Odds Home (min)", 0.0, 10.0, 0.0)
        selected_ft_odd_h_max = st.number_input("FT Odds Home (max)", selected_ft_odd_h_min, 10.0, 10.0)
        selected_ft_odd_d_min = st.number_input("FT Odds Draw (min)", 0.0, 10.0, 0.0)
        selected_ft_odd_d_max = st.number_input("FT Odds Draw (max)", selected_ft_odd_d_min, 10.0, 10.0)
        selected_ft_odd_a_min = st.number_input("FT Odds Away (min)", 0.0, 10.0, 0.0)
        selected_ft_odd_a_max = st.number_input("FT Odds Away (max)", selected_ft_odd_a_min, 10.0, 10.0)

    with col2:
        selected_ft_odd_over25_min = st.number_input("FT Odds Over 2.5 (min)", 0.0, 10.0, 0.0)
        selected_ft_odd_over25_max = st.number_input("FT Odds Over 2.5 (max)", selected_ft_odd_over25_min, 10.0, 10.0)
        selected_ft_odd_under25_min = st.number_input("FT Odds Under 2.5 (min)", 0.0, 10.0, 0.0)
        selected_ft_odd_under25_max = st.number_input("FT Odds Under 2.5 (max)", selected_ft_odd_under25_min, 10.0, 10.0)

    with col3:
        selected_ft_odd_btts_yes_min = st.number_input("FT Odds BTTS Yes (min)", 0.0, 10.0, 0.0)
        selected_ft_odd_btts_yes_max = st.number_input("FT Odds BTTS Yes (max)", selected_ft_odd_btts_yes_min, 10.0, 10.0)
        selected_rodada_min = st.number_input("Rodada (min)", 0.0, 1.0, 0.0)  # Change 1 to 1.0 (float)
        selected_rodada_max = st.number_input("Rodada (max)", selected_rodada_min, 40.0, 10.0)

    # Convert 'Rodada' column to integers
    df2['Rodada'] = pd.to_numeric(df2['Rodada'], errors='coerce')

# Apply filters to the DataFrame
    filtered_data = df2[
        (df2['FT_Odd_H'] >= selected_ft_odd_h_min) &
        (df2['FT_Odd_D'] >= selected_ft_odd_d_min) &
        (df2['FT_Odd_A'] >= selected_ft_odd_a_min) &
        (df2['FT_Odd_Over25'] >= selected_ft_odd_over25_min) &
        (df2['FT_Odd_Under25'] >= selected_ft_odd_under25_min) &
        (df2['FT_Odd_BTTS_Yes'] >= selected_ft_odd_btts_yes_min) &
        (df2['Rodada'] >= selected_rodada_min) &
        (df2['Rodada'] <= selected_rodada_max)
    ]

    if not filtered_data.empty:
        sorted_filtered_data = filtered_data.sort_values(by='Time')
        st.dataframe(sorted_filtered_data[columns_to_display])
    else:
        st.warning("Não existem jogos com esses critérios!")

# Call the function to display the web application
jogos_do_dia_page()
