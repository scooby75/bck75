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

    col1, col2 = st.columns(2)

    # Filters for selected columns
    with col1:
        selected_ft_odd_h_min = st.number_input("Min FT Odds Home:", min_value=1.0)
        selected_ft_odd_h_max = st.number_input("Max FT Odds Home:", max_value=10.0)
        selected_ft_odd_d_min = st.number_input("Min FT Odds Draw:", min_value=1.0)
        selected_ft_odd_d_max = st.number_input("Max FT Odds Draw:", max_value=10.0)
        selected_ft_odd_a_min = st.number_input("Min FT Odds Away:", min_value=1.0)
        selected_ft_odd_a_max = st.number_input("Max FT Odds Away:", max_value=10.0)

    with col2:
        selected_ft_odd_over25_min = st.number_input("Min FT Odds Over 2.5:", min_value=1.0)
        selected_ft_odd_over25_max = st.number_input("Max FT Odds Over 2.5:", max_value=10.0)
        selected_ft_odd_under25_min = st.number_input("Min FT Odds Under 2.5:", min_value=1.0)
        selected_ft_odd_under25_max = st.number_input("Max FT Odds Under 2.5:", max_value=10.0)
        selected_ft_odd_btts_yes_min = st.number_input("Min FT Odds BTTS Yes:", min_value=1.0)
        selected_ft_odd_btts_yes_max = st.number_input("Max FT Odds BTTS Yes:", max_value=10.0)

    filtered_data = df2[
        (df2['FT_Odd_H'] >= selected_ft_odd_h_min) & (df2['FT_Odd_H'] <= selected_ft_odd_h_max) &
        (df2['FT_Odd_D'] >= selected_ft_odd_d_min) & (df2['FT_Odd_D'] <= selected_ft_odd_d_max) &
        (df2['FT_Odd_A'] >= selected_ft_odd_a_min) & (df2['FT_Odd_A'] <= selected_ft_odd_a_max) &
        (df2['FT_Odd_Over25'] >= selected_ft_odd_over25_min) & (df2['FT_Odd_Over25'] <= selected_ft_odd_over25_max) &
        (df2['FT_Odd_Under25'] >= selected_ft_odd_under25_min) & (df2['FT_Odd_Under25'] <= selected_ft_odd_under25_max) &
        (df2['FT_Odd_BTTS_Yes'] >= selected_ft_odd_btts_yes_min) & (df2['FT_Odd_BTTS_Yes'] <= selected_ft_odd_btts_yes_max)
    ]

    if not filtered_data.empty:
        st.dataframe(filtered_data[columns_to_display])
    else:
        st.warning("No matches found for the selected filters.")

# Call the function to display the web application
jogos_do_dia_page()
