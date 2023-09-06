# cs.py
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta

from session_state import SessionState

# Função para calcular a probabilidade de um certo número de gols usando a distribuição de Poisson
def poisson_prob(media, k):
    return (np.exp(-media) * media ** k) / np.math.factorial(k)

def cs_page():
    # Inicializa o estado da sessão
    session_state = SessionState()

    # Defina o valor de user_profile após a criação da instância
    session_state.user_profile = 2  # Ou qualquer outro valor desejado

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 2:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return

    st.subheader("Probabilidade de Placar")
    st.text("A base de dados é atualizada diariamente e as odds de referência são da Bet365")
    
    # Carregar os dados CSV a partir das URLs para DataFrames
    url_bdgeral = "https://github.com/scooby75/bdfootball/blob/main/BD_Geral.csv?raw=true"
    url_jogosdodia = "https://github.com/scooby75/bdfootball/blob/main/Jogos_do_Dia_FS.csv?raw=true"

    bdgeral = pd.read_csv(url_bdgeral)
    jogosdodia = pd.read_csv(url_jogosdodia)

    # Excluir jogos com palavras-chave "U19", "U20", "U21" e "U23"
    keywords_to_exclude = ["U19", "U20", "U21", "U23"]
    bdgeral = bdgeral[~bdgeral['Home'].str.contains('|'.join(keywords_to_exclude)) & ~bdgeral['Away'].str.contains('|'.join(keywords_to_exclude))]

    # Calcular a média de gols marcados em casa (Home)
    df_media_gols_casa = bdgeral.groupby('Home').agg({'FT_Goals_H': 'mean'}).reset_index()
    df_media_gols_casa.rename(columns={'FT_Goals_H': 'Media_Gols_Casa'}, inplace=True)

    # Calcular a média de gols marcados fora de casa (Away)
    df_media_gols_fora = bdgeral.groupby('Away').agg({'FT_Goals_A': 'mean'}).reset_index()
    df_media_gols_fora.rename(columns={'FT_Goals_A': 'Media_Gols_For'}, inplace=True)

    # Combinar os jogos filtrados com os dados de média de gols calculados
    jogosdodia = jogosdodia.merge(df_media_gols_casa, left_on='Home', right_on='Home')
    jogosdodia = jogosdodia.merge(df_media_gols_fora, left_on='Away', right_on='Away')

    # Filtrar jogos com FT_Odd_H e FT_Odd_A >= 1.80 e Odd_Over25 >= 2.10
    jogos_filtrados_odds = jogosdodia[
        (jogosdodia['FT_Odd_H'] >= 1.80) &
        (jogosdodia['FT_Odd_A'] >= 1.80) &
        (jogosdodia['Odd_Over25'] >= 2.10)
    ]

    # Exibir os resultados para cada jogo usando o Streamlit
    for index, row in jogos_filtrados_odds.iterrows():
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
        
        # Exibir os resultados usando st.dataframe
        st.write(pd.DataFrame(resultados_jogo))

# Chamar a função para executar o app
cs_page()
