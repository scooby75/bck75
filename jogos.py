import streamlit as st
import pandas as pd
import datetime as dt

def jogos_do_dia_page():
    st.subheader("Jogos do Dia")
    st.text("A base de dados é atualizada diariamente e as odds de referência são da Bet365")

    @st.cache_data(ttl=dt.timedelta(hours=24))
    def load_base():
        url = "https://github.com/scooby75/bdfootball/blob/main/jogos_do_dia.csv?raw=true"
        data_jogos = pd.read_csv(url)

        # Rename the columns
        data_jogos.rename(columns={
            'FT_Odds_H': 'FT_Odd_H',
            'FT_Odds_D': 'FT_Odd_D',
            'FT_Odds_A': 'FT_Odd_A',
            'FT_Odds_Over25': 'FT_Odd_Over25',
            'FT_Odds_Under25': 'FT_Odd_Under25',
            'Odds_BTTS_Yes': 'FT_Odd_BTTS_Yes',
            'Rodada': 'Round',
        }, inplace=True)

        return data_jogos

    df2 = load_base()

    # Select the specific columns to display in the "Jogos Filtrados" table
    columns_to_display = [
        'Date', 'Time', 'League', 'Home', 'Away', 'Round',
        'FT_Odd_H', 'FT_Odd_D', 'FT_Odd_A',
        'FT_Odd_Over25', 'FT_Odd_Under25', 'FT_Odd_BTTS_Yes'
    ]

    col1, col2, col3 = st.beta_columns(3)

    # Filters for selected columns
    with col1:
        selected_ft_odd_h = st.number_input("Filter by FT Odds Home:", min_value=1.0)
        selected_ft_odd_over25 = st.number_input("Filter by FT Odds Over 2.5:", min_value=1.0)

    with col2:
        selected_ft_odd_d = st.number_input("Filter by FT Odds Draw:", min_value=1.0)
        selected_ft_odd_under25 = st.number_input("Filter by FT Odds Under 2.5:", min_value=1.0)

    with col3:
        selected_ft_odd_a = st.number_input("Filter by FT Odds Away:", min_value=1.0)
        selected_ft_odd_btts_yes = st.number_input("Filter by FT Odds BTTS Yes:", min_value=1.0)

    filtered_data = df2[
        (df2['FT_Odd_H'] >= selected_ft_odd_h) &
        (df2['FT_Odd_D'] >= selected_ft_odd_d) &
        (df2['FT_Odd_A'] >= selected_ft_odd_a) &
        (df2['FT_Odd_Over25'] >= selected_ft_odd_over25) &
        (df2['FT_Odd_Under25'] >= selected_ft_odd_under25) &
        (df2['FT_Odd_BTTS_Yes'] >= selected_ft_odd_btts_yes)
    ]

    st.dataframe(filtered_data[columns_to_display])

# Call the function to display the web application
jogos_do_dia_page()
