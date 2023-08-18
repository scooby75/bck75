import streamlit as st
import pandas as pd
import datetime as dt

def jogos_do_dia_page():
    st.subheader("Jogos do Dia")
    st.text("A base de dados é atualizada diariamente e as odds de referência são da Bet365")

    # Load the data
    @st.cache_data(ttl=dt.timedelta(hours=24))
    def load_base():
        url = "https://github.com/scooby75/bdfootball/blob/main/jogos_do_dia.xlsx?raw=true"
        data_jogos = pd.read_excel(url)

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

    # Filters for selected columns
    filter_values = {}
    filter_columns = [
        ('FT Odds Home', 'selected_ft_odd_h'),
        ('FT Odds Draw', 'selected_ft_odd_d'),
        ('FT Odds Away', 'selected_ft_odd_a'),
        ('FT Odds Over 2.5', 'selected_ft_odd_over25'),
        ('FT Odds Under 2.5', 'selected_ft_odd_under25'),
        ('FT Odds BTTS Yes', 'selected_ft_odd_btts_yes')
    ]

    col1, col2 = st.columns(2)

    for i, (label, var_name) in enumerate(filter_columns):
        with col1 if i < len(filter_columns) // 2 else col2:
            min_val, max_val = st.slider(f"Filter by {label}:", 0.0, 10.0, (0.0, 10.0))
            filter_values[var_name] = (min_val, max_val)

    # Apply filters to the DataFrame
    filtered_data = df2[
        (df2['FT_Odd_H'].between(*filter_values['selected_ft_odd_h'])) &
        (df2['FT_Odd_D'].between(*filter_values['selected_ft_odd_d'])) &
        (df2['FT_Odd_A'].between(*filter_values['selected_ft_odd_a'])) &
        (df2['FT_Odd_Over25'].between(*filter_values['selected_ft_odd_over25'])) &
        (df2['FT_Odd_Under25'].between(*filter_values['selected_ft_odd_under25'])) &
        (df2['FT_Odd_BTTS_Yes'].between(*filter_values['selected_ft_odd_btts_yes']))
    ]

    if not filtered_data.empty:
        st.dataframe(filtered_data[columns_to_display])
    else:
        st.warning("No matches found for the selected filters.")

# Call the function to display the web application
jogos_do_dia_page()

