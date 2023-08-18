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
    prob_vitoria_home_min = st.slider("Prob de Vitória Home (mínimo)", 0, 100, 0)
    prob_vitoria_home_max = st.slider("Prob de Vitória Home (máximo)", prob_vitoria_home_min, 100, 100)
    
    prob_vitoria_away_min = st.slider("Prob de Vitória Away (mínimo)", 0, 100, 0)
    prob_vitoria_away_max = st.slider("Prob de Vitória Away (máximo)", prob_vitoria_away_min, 100, 100)

    prob_over25_home_min = st.slider("Prob Over 2.5 Home (mínimo)", 0, 100, 0)
    prob_over25_home_max = st.slider("Prob Over 2.5 Home (máximo)", prob_over25_home_min, 100, 100)
    
    prob_over25_away_min = st.slider("Prob Over 2.5 Away (mínimo)", 0, 100, 0)
    prob_over25_away_max = st.slider("Prob Over 2.5 Away (máximo)", prob_over25_away_min, 100, 100)

    media_gols_h_min = st.slider("Media Gols H (mínimo)", 0.0, 10.0, 0.0)
    media_gols_h_max = st.slider("Media Gols H (máximo)", media_gols_h_min, 10.0, 10.0)
    
    media_gols_a_min = st.slider("Media Gols A (mínimo)", 0.0, 10.0, 0.0)
    media_gols_a_max = st.slider("Media Gols A (máximo)", media_gols_a_min, 10.0, 10.0)

    ppg_h_min = st.slider("PPG_H (mínimo)", 0.0, 3.0, 0.0)
    ppg_h_max = st.slider("PPG_H (máximo)", ppg_h_min, 3.0, 3.0)
    
    ppg_a_min = st.slider("PPG_A (mínimo)", 0.0, 3.0, 0.0)
    ppg_a_max = st.slider("PPG_A (máximo)", ppg_a_min, 3.0, 3.0)

    # Specify columns to display in the sorted data
    columns_to_display = [
        'Hora', 'Home', 'Away', 'Prob_Vitoria_Home', 'Prob_Vitoria_Away',
        'Prob_Over25_Home', 'Prob_Over25_Away', 'Media_Gols_H', 'Media_Gols_A', 'PPG_H', 'PPG_A'
    ]

    if not df2.empty:
        filtered_data = df2.copy()

        # Apply filters with ranges
        filtered_data = filtered_data[
            (filtered_data['Prob_Vitoria_Home'] >= prob_vitoria_home_min) &
            (filtered_data['Prob_Vitoria_Home'] <= prob_vitoria_home_max) &
            (filtered_data['Prob_Vitoria_Away'] >= prob_vitoria_away_min) &
            (filtered_data['Prob_Vitoria_Away'] <= prob_vitoria_away_max) &
            (filtered_data['Prob_Over25_Home'] >= prob_over25_home_min) &
            (filtered_data['Prob_Over25_Home'] <= prob_over25_home_max) &
            (filtered_data['Prob_Over25_Away'] >= prob_over25_away_min) &
            (filtered_data['Prob_Over25_Away'] <= prob_over25_away_max) &
            (filtered_data['Media_Gols_H'] >= media_gols_h_min) &
            (filtered_data['Media_Gols_H'] <= media_gols_h_max) &
            (filtered_data['Media_Gols_A'] >= media_gols_a_min) &
            (filtered_data['Media_Gols_A'] <= media_gols_a_max) &
            (filtered_data['PPG_H'] >= ppg_h_min) &
            (filtered_data['PPG_H'] <= ppg_h_max) &
            (filtered_data['PPG_A'] >= ppg_a_min) &
            (filtered_data['PPG_A'] <= ppg_a_max)
        ]

        # Sort the filtered data by 'Hora'
        filtered_data = filtered_data.sort_values(by='Hora')

        # Display the filtered data
        st.dataframe(filtered_data[columns_to_display])
    else:
        st.warning("Não existem jogos com esses critérios!")

# Call the function to display the web application
predict_page()

