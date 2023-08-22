import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta  

def cs_page():
    # Carregar os dados CSV a partir das URLs para DataFrames
    url = "https://github.com/scooby75/bdfootball/blob/main/bd%202019_2023%20com%20placar.csv?raw=true"
    bdgeral = pd.read_csv(url)

    # Calcular a média de gols marcados em casa (Home)
    df_media_gols_casa = bdgeral.groupby('Home').agg({'FT_Goals_H': 'mean'}).reset_index()
    df_media_gols_casa.rename(columns={'FT_Goals_H': 'Media_Gols_Casa'}, inplace=True)

    # Calcular a média de gols marcados fora de casa (Away)
    df_media_gols_fora = bdgeral.groupby('Away').agg({'FT_Goals_A': 'mean'}).reset_index()
    df_media_gols_fora.rename(columns={'FT_Goals_A': 'Media_Gols_For'}, inplace=True)

    # Carregar os dados CSV de outra URL para um DataFrame
    url = "https://github.com/scooby75/bdfootball/blob/main/2023-08-22_Jogos_do_Dia_FS.csv?raw=true"
    jogosdodia = pd.read_csv(url)

    # Combinar os jogos filtrados com os dados de média de gols calculados
    jogos_filtrados = jogosdodia.merge(df_media_gols_casa, left_on='Home', right_on='Home')
    jogos_filtrados = jogos_filtrados.merge(df_media_gols_fora, left_on='Away', right_on='Away')

    # Função para calcular a probabilidade de um certo número de gols usando a distribuição de Poisson
    def poisson_prob(media, k):
        return (np.exp(-media) * media ** k) / np.math.factorial(k)

    # Loop para prever os 6 placares mais prováveis para cada jogo
    for index, row in jogos_filtrados.iterrows():
        time_casa = row['Home']
        time_visitante = row['Away']
        data_jogo = row['Date']
        hora_jogo = row['Time']
        media_gols_casa = row['Media_Gols_Casa']
        media_gols_fora = row['Media_Gols_For']

        # Converter a hora do jogo em um objeto de hora
        hora_jogo_obj = datetime.strptime(hora_jogo, '%H:%M').time()

        # Subtrair 3 horas para ajustar para o horário local (time - 3)
        hora_jogo_obj_local = (datetime.combine(datetime.today(), hora_jogo_obj) - timedelta(hours=3)).time()

        placares_previstos = []
        for gols_casa in range(7):
            for gols_fora in range(7):
                prob_gols_casa = poisson_prob(media_gols_casa, gols_casa)
                prob_gols_fora = poisson_prob(media_gols_fora, gols_fora)
                prob_total = prob_gols_casa * prob_gols_fora
                placares_previstos.append((gols_casa, gols_fora, prob_total))

        # Ordenar os placares previstos por probabilidade em ordem decrescente
        placares_previstos.sort(key=lambda x: x[2], reverse=True)

        # Exibir os resultados para cada jogo usando o Streamlit
        st.write(f"**{time_casa} vs {time_visitante} - {data_jogo} {hora_jogo_obj_local.strftime('%H:%M')} (Horário Local)**")
        
        # Criar uma lista para os resultados do jogo
        resultados_jogo = []
        for i in range(6):
            prob_porcentagem = f"{placares_previstos[i][2] * 100:.2f}%"
            resultados_jogo.append({'Placar': f"{placares_previstos[i][0]} - {placares_previstos[i][1]}",
                                 'Probabilidade': prob_porcentagem})
        
        # Organizar os resultados em ordem decrescente de probabilidade
        resultados_jogo = sorted(resultados_jogo, key=lambda x: float(x['Probabilidade'][:-1]), reverse=True)

        # Excluindo jogos com as palavras-chave "U19", "U20", "U21" e "U23"
        jogos_filtrados_sem_keywords = [jogo for jogo in jogos_filtrados if all(keyword not in jogo['Home'] and keyword not in jogo['Away'] for keyword in ["U19", "U20", "U21", "U23"])]

        # Exibindo os resultados filtrados usando st.dataframe
        st.write(pd.DataFrame(resultados_jogo))  # Mostrar os resultados filtrados
   

# Chamar a função para executar o app
cs_page()
