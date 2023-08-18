import streamlit as st
import pandas as pd
import datetime as dt

def predict_page():
    st.subheader("Jogos do Dia")
    st.text("A base de dados é atualizada diariamente e as odds de referência são da Bet365")

    # Load the data
    @st.cache_data(ttl=dt.timedelta(hours=24))
    def load_base():
        url = "https://github.com/scooby75/bdfootball/blob/main/Predict.csv?raw=true"
        data_jogos = pd.read_csv(url)

        # Rename the columns
        data_jogos.rename(columns={
            'Vitoria_H': 'Prob_Vitoria_Home',
            'Vitoria_A': 'Prob_Vitoria_Away',
            'Over25_H': 'Prob_Over25_Home',
            'Over25_A': 'Prob_Over25_Away',
            'MediaGols_H': 'Media_Gols_H',
            'MediaGols_A': 'Media_Gols_A',
            'PPG_H': 'PPG_H',
            'PPG_A': 'PPG_A',
        }, inplace=True)

        return data_jogos

    df2 = load_base()

    # Create sliders for filter conditions
    prob_vitoria_home_threshold = st.slider("Prob de Vitória Home", 0, 100, 0)
    prob_vitoria_away_threshold = st.slider("Prob de Vitória Away", 0, 100, 0)
    prob_over25_home_threshold = st.slider("Prob Over 2.5 Home", 0, 100, 0)
    prob_over25_away_threshold = st.slider("Prob Over 2.5 Away", 0, 100, 0)
    media_gols_h_threshold = st.slider("Media Gols H", 0.0, 10.0, 0.0)
    media_gols_a_threshold = st.slider("Media Gols A", 0.0, 10.0, 0.0)
    ppg_h_threshold = st.slider("PPG_H", 0.0, 3.0, 0.0)
    ppg_a_threshold = st.slider("PPG_A", 0.0, 3.0, 0.0)

    # Specify columns to display in the sorted data
    columns_to_display = [
        'Hora', 'Home', 'Away', 'Prob_Vitoria_Home', 'Prob_Vitoria_Away',
        'Prob_Over25_Home', 'Prob_Over25_Away', 'Media_Gols_H', 'Media_Gols_A', 'PPG_H', 'PPG_A'
    ]

    if not df2.empty:
        filtered_data = df2.copy()

        # Aplicar filtro Prob de Vitória Home
        filtered_data = filtered_data[filtered_data['Prob_Vitoria_Home'] >= prob_vitoria_home_threshold]

        # Aplicar filtro Prob de Vitória Away
        filtered_data = filtered_data[filtered_data['Prob_Vitoria_Away'] >= prob_vitoria_away_threshold]

        # Aplicar filtro Prob Over 2.5 Home
        filtered_data = filtered_data[filtered_data['Prob_Over25_Home'] >= prob_over25_home_threshold]

        # Aplicar filtro Prob Over 2.5 Away
        filtered_data = filtered_data[filtered_data['Prob_Over25_Away'] >= prob_over25_away_threshold]

        # Aplicar filtro Media Gols H
        filtered_data = filtered_data[filtered_data['Media_Gols_H'] >= media_gols_h_threshold]

        # Aplicar filtro Media Gols A
        filtered_data = filtered_data[filtered_data['Media_Gols_A'] >= media_gols_a_threshold]

        # Aplicar filtro PPG_H
        filtered_data = filtered_data[filtered_data['PPG_H'] >= ppg_h_threshold]

        # Aplicar filtro PPG_A
        filtered_data = filtered_data[filtered_data['PPG_A'] >= ppg_a_threshold]

        # Ordenar os dados filtrados por Hora
        filtered_data = filtered_data.sort_values(by='Hora')

        st.dataframe(filtered_data[columns_to_display])
    else:
        st.warning("Não existem jogos com esses critérios!")

# Chamar a função para exibir a aplicação web
predict_page()
