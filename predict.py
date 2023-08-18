import streamlit as st
import pandas as pd
import datetime as dt

def predict_page():
    st.subheader("Jogos do Dia")
    st.text("A base de dados é atualizada diariamente e as odds de referência são da Bet365")

    # Load the data
    @st.cache_data(ttl=dt.timedelta(hours=24))
    def load_base():
        url = "https://github.com/scooby75/bdfootball/blob/main/predict.xlsx?raw=true"
        data_jogos = pd.read_excel(url)

        # Rename the columns
        data_jogos.rename(columns={
            'GP_H': 'Rodada_Home',
            'GP_A': 'Rodada_Away',
            'Vitoria_H': 'Prob_Vitoria_Home',
            'Vitoria_A': 'Prob_Vitoria_Away',
            'Over25_H': 'Prob_Over25_Home',
            'Over25_A': 'Prob_Over25_Away',
            'BTTS_H': 'Prob_BTTS_H',
            'BTTS_A': 'Prob_BTTS_A',
            'GolsMarcados_H': 'Gols_Marcados_H',
            'GolsSofridos_H': 'Gols_Sofridos_H',
            'GolsMarcados_A': 'Gols_Marcados_A',
            'GolsSofridos_A': 'Gols_Sofridos_A',
            'MediaGols_H': 'Media_Gols_H',
            'MediaGols_A': 'Media_Gols_A',
            'PPG_H': 'PPG_H',
            'PPG_A': 'PPG_A',
        }, inplace=True)

        return data_jogos

    df2 = load_base()

    # Create sliders for filter conditions
    prob_vitoria_home_threshold = st.slider("Prob de Vitória Home", 0, 100, 50)
    prob_vitoria_away_threshold = st.slider("Prob de Vitória Away", 0, 100, 50)
    prob_over25_home_threshold = st.slider("Prob Over 2.5 Home", 0, 100, 60)
    prob_over25_away_threshold = st.slider("Prob Over 2.5 Away", 0, 100, 60)
    media_gols_h_threshold = st.slider("Media Gols H", 0, 10, 3)
    media_gols_a_threshold = st.slider("Media Gols A", 0, 10, 3)

    # Apply filters to the DataFrame
    filtered_data = df2[
        (df2['Prob_Vitoria_Home'] > prob_vitoria_home_threshold) &
        (df2['Prob_Vitoria_Away'] > prob_vitoria_away_threshold) &
        (df2['Prob_Over25_Home'] > prob_over25_home_threshold) &
        (df2['Prob_Over25_Away'] > prob_over25_away_threshold) &
        (df2['Media_Gols_H'] > media_gols_h_threshold) &
        (df2['Media_Gols_A'] > media_gols_a_threshold)
    ]

    # Specify columns to display in the sorted data
    columns_to_display = [
        'Time', 'Rodada_Home', 'Rodada_Away', 'Prob_Vitoria_Home', 'Prob_Vitoria_Away',
        'Prob_Over25_Home', 'Prob_Over25_Away', 'Gols_Marcados_H', 'Gols_Marcados_A'
    ]

    if not filtered_data.empty:
        sorted_filtered_data = filtered_data.sort_values(by='Time')
        st.dataframe(sorted_filtered_data[columns_to_display])
    else:
        st.warning("Não existem jogos com esses critérios!")

# Call the function to display the web application
predict_page()
