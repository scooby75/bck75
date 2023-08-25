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
    selected_leagues = st.multiselect("Selecionar Liga(s)", bck_home_df['League'].unique(), default=bck_home_df['League'].unique())

    # Filter by Season
    selected_seasons = st.multiselect("Selecionar Temporada(s)", bck_home_df['Season'].unique(), default=bck_home_df['Season'].unique())

    # Filter by Round
    selected_round = st.number_input("Selecionar Rodada", min_value=1, max_value=bck_home_df['Round'].max(), value=1)

    # ... Add number_input or other appropriate filters for other columns ...

    # Apply filters
    filtered_df = bck_home_df[
        (bck_home_df['League'].isin(selected_leagues)) &
        (bck_home_df['Season'].isin(selected_seasons)) &
        (bck_home_df['Round'] == selected_round)
        # Add more filtering conditions for other columns here...
    ]

    # Display filtered data
    st.dataframe(filtered_df)

# Execute the function to create the page
bck_home_page()
