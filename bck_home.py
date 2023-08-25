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

    # Filter by League
    all_leagues = "Todos"
    selected_leagues = st.multiselect("Selecionar Liga(s)", [all_leagues] + list(bck_home_df['League'].unique()), default=all_leagues)
    if all_leagues in selected_leagues:
        selected_leagues.remove(all_leagues)

    # Filter by Season
    all_seasons = "Todos"
    selected_seasons = st.multiselect("Selecionar Temporada(s)", [all_seasons] + list(bck_home_df['Season'].unique()), default=all_seasons)
    if all_seasons in selected_seasons:
        selected_seasons.remove(all_seasons)

    # Group all rounds together
    all_rounds = "Todos"
    selected_round = st.selectbox("Selecionar Rodada", [all_rounds] + list(bck_home_df['Round'].unique()))
    if selected_round == all_rounds:
        selected_rounds = list(bck_home_df['Round'].unique())
    else:
        selected_rounds = [selected_round]

    # ... Add other filters ...

    # Apply filters
    filtered_df = bck_home_df[
        (bck_home_df['League'].isin(selected_leagues) | (all_leagues in selected_leagues)) &
        (bck_home_df['Season'].isin(selected_seasons) | (all_seasons in selected_seasons)) &
        (bck_home_df['Round'].isin(selected_rounds))
        # Add more filtering conditions for other columns here...
    ]

    # Display filtered data
    st.dataframe(filtered_df)

# Execute the function to create the page
bck_home_page()
