import streamlit as st
import pandas as pd

def bck_home_page():
    ##### PÁGINA BCK HOME ######

    # Carregar os dados
    @st.cache(ttl=86400.0)  # 24 horas em segundos
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
    selected_leagues = st.multiselect("Selecionar Liga(s)", [all_leagues] + list(bck_home_df['League'].unique()), default=[all_leagues])

    # Filter by Season
    all_seasons = "Todos"
    selected_seasons = st.multiselect("Selecionar Temporada(s)", [all_seasons] + list(bck_home_df['Season'].unique()), default=[all_seasons])

    # Multiselect for Round
    all_rounds = "Todos"
    selected_rounds = st.multiselect("Selecionar Rodada(s)", [all_rounds] + list(bck_home_df['Round'].unique()), default=[all_rounds])

    # ... Add other filters ...

    # Apply filters
    filtered_df = bck_home_df[
        (bck_home_df['League'].isin(selected_leagues) if all_leagues not in selected_leagues else True) &
        (bck_home_df['Season'].isin(selected_seasons) if all_seasons not in selected_seasons else True) &
        (bck_home_df['Round'].isin(selected_rounds) if all_rounds not in selected_rounds else True)
        # Add more filtering conditions for other columns here...
    ]

    # Display filtered data
    st.dataframe(filtered_df)

# Execute the function to create the page
bck_home_page()
