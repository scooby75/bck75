import streamlit as st
import pandas as pd
from scipy.stats import poisson
from streamlit import SessionState

from session_state import SessionState

def cs_page():
    # Inicializa o estado da sessão
    session_state = SessionState()

    # Defina o valor de user_profile após a criação da instância
    session_state.user_profile = 2  # Ou qualquer outro valor desejado

    # Verifica se o usuário tem permissão para acessar a página
    if session_state.user_profile < 2:
        st.error("Você não tem permissão para acessar esta página. Faça um upgrade do seu plano!!")
        return

    # URL do arquivo CSV com os dados dos jogos
    url = "https://raw.githubusercontent.com/scooby75/bdfootball/main/Jogos_do_Dia_FS.csv"

    # Carregar os dados do arquivo CSV em um DataFrame
    df = pd.read_csv(url)

    # Filtrar jogos com rodada maior ou igual a 10
    df_filtrado = df[df['Rodada'] >= 10]

    # Filtrar jogos com cotação (odd) da equipe da casa entre 1.40 e 2.4
    df_filtrado = df_filtrado[(df_filtrado['FT_Odd_H'] >= 1.40) & (df_filtrado['FT_Odd_H'] <= 2.4)]

    # Filtrar jogos com cotação (odd) de menos de 2.5 gols
    df_filtrado = df_filtrado[df_filtrado['FT_Odd_Under25'] <= 2]

    # Placares para os quais você deseja calcular a probabilidade
    placares = ['0x0', '1x0', '0x1', '1x1', '2x0', '0x2', '2x1', '1x2', '2x2', '3x0', '3x1', '0x3', '3x2', '3x3', '1x3','2x3']

    # Lista para armazenar as linhas dos resultados
    linhas_resultados = []

    # Iterar sobre os jogos filtrados e calcular as probabilidades para cada placar
    for index, row in df_filtrado.iterrows():
        # Calcular as médias de gols esperados para cada time e o total esperado
        lambda_home = row['XG_Home']
        lambda_away = row['XG_Away']
        lambda_total = row['Average Goals']

        # Calcular as probabilidades usando a distribuição de Poisson
        probabilidades = []
        total_prob = 0  # Total de probabilidade para normalização

        for placar in placares:
            placar_split = placar.split('x')
            gols_home = int(placar_split[0])
            gols_away = int(placar_split[1])

            prob_home = poisson.pmf(gols_home, lambda_home)
            prob_away = poisson.pmf(gols_away, lambda_away)
            prob_total = poisson.pmf(gols_home + gols_away, lambda_total)

            # Aplicar o ajuste de zero inflado para placares "estranhos"
            if (lambda_home < gols_home) or (lambda_away < gols_away):
                prob_placar = prob_home * prob_away * prob_total * 1.50
            else:
                prob_placar = prob_home * prob_away * prob_total

            total_prob += prob_placar
            probabilidades.append(prob_placar)

        # Normalizar as probabilidades para que a soma seja 100%
        probabilidades = [prob / total_prob for prob in probabilidades]

        # Selecionar os 8 placares mais prováveis
        top_placares = sorted(range(len(probabilidades)), key=lambda i: -probabilidades[i])[:8]

        # Verificar se o primeiro placar mais provável é maior ou igual a 16%
        if probabilidades[top_placares[0]] >= 16:
            # Criar uma linha para o resultado deste jogo
            linha_resultado = {
                'Hora': row['Hora'],
                'Home': row['Home'],
                'Away': row['Away'],
                'FT_Odd_H': row['FT_Odd_H'],
                'FT_Odd_D': row['FT_Odd_D'],
                'FT_Odd_A': row['FT_Odd_A']
            }

            for i in top_placares:
                placar = placares[i]
                prob = round(probabilidades[i] * 100, 2)
                linha_resultado[placar] = prob

            linhas_resultados.append(linha_resultado)

    # Criar um novo DataFrame com os resultados
    resultado_df = pd.DataFrame(linhas_resultados)

    # Se houver jogos que atendam às condições originais, exibir o DataFrame de resultados
    if not resultado_df.empty:
        st.subheader("Probabilidade de Placar")
        st.dataframe(resultado_df)

# Chamar a função para executar o aplicativo
cs_page()
