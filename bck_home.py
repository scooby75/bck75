import streamlit as st
import pandas as pd

def bck_home_page():
    ##### PÁGINA BCK HOME ######

    # Carregar os dados
    @st.cache_data(ttl=86400.0)  # 24 horas em segundos
    def load_base():
        url = "https://github.com/scooby75/bdfootball/blob/main/BD_Geral.csv?raw=true"
        df = pd.read_csv(url)
        return df
        
    # Chamar a função para carregar os dados
    bck_home_df = load_base()

    # Filtros interativos
    st.header("Filtros")

    # Organize filters into columns
    col1, col2, col3 = st.columns(3)

    # Filter by League
    with col1:
        all_leagues = "Todos"
        selected_leagues = st.multiselect("Selecionar Liga(s)", [all_leagues] + list(bck_home_df['League'].unique()))

    # Filter by Season
    with col2:
        all_seasons = "Todos"
        selected_seasons = st.multiselect("Selecionar Temporada(s)", [all_seasons] + list(bck_home_df['Season'].unique()))

        # Filter for Odd_Home (FT_Odd_H) range
        odd_h_min = st.number_input("Odd_Home Mínimo", value=0.0)
        odd_h_max = st.number_input("Odd_Home Máximo", value=10.0)

    # Multiselect for Round
    with col3:
        all_rounds = "Todos"
        selected_rounds = st.multiselect("Selecionar Rodada(s)", [all_rounds] + list(bck_home_df['Round'].unique()))

    # Multiselect for Home
    home_teams = bck_home_df['Home'].unique()  # Get unique teams from 'Home' column
    selected_home = st.multiselect("Selecionar Mandante", home_teams)

    # ... Add other filters ...

    # Apply filters
    filtered_df = bck_home_df[
        (bck_home_df['League'].isin(selected_leagues) if all_leagues not in selected_leagues else True) &
        (bck_home_df['Season'].isin(selected_seasons) if all_seasons not in selected_seasons else True) &
        (bck_home_df['Round'].isin(selected_rounds) if all_rounds not in selected_rounds else True) &
        (bck_home_df['Home'].isin(selected_home) if selected_home else True) &
        (bck_home_df['FT_Odd_H'] >= odd_h_min) &
        (bck_home_df['FT_Odd_H'] <= odd_h_max)
        # Add more filtering conditions for other columns here...
    ]

    # Display selected columns from the filtered data
    selected_columns = [
        "Date", "League", "Season", "Round", "Home", "Away",
        "FT_Odd_H", "FT_Odd_D", "FT_Odd_A", "Placar_HT", "Placar_FT"
    ]
    st.dataframe(filtered_df[selected_columns])

# Execute the function to create the page
bck_home_page()
