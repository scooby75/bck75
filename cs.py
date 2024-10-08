import streamlit as st
import pandas as pd
from scipy.stats import poisson
from session_state import SessionState
from datetime import datetime
from io import StringIO, BytesIO

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

    # Excluir linhas em que 'Home' ou 'Away' contenham substrings específicas
    substrings_para_excluir = ['U16', 'U17', 'U18', 'U19', 'U20', '21', 'U22', 'U23', 'Women', 'reserve']
    mask = ~df['Home'].str.contains('|'.join(substrings_para_excluir), case=False) & \
           ~df['Away'].str.contains('|'.join(substrings_para_excluir), case=False)
    df = df[mask]

    # Excluir linhas em que 'League' contenha 'WOMEN'
    substring_para_excluir = ['WOMEN', 'Reserve']
    mask = ~df['Liga'].str.contains('|'.join(substring_para_excluir), case=False)
    df = df[mask]

    # Filtrar jogos com round maior ou igual a 10
    df = df[df['Rodada'] >= 10]

    # Filtrar jogos com home menor ou igual a 1.90
    df = df[(df['FT_Odd_H'] >= 1.80) & (df['FT_Odd_H'] <= 2.4)]

    # Filtrar jogos com home menor ou igual a 1.90
    df = df[(df['FT_Odd_Under25'] <= 2)]

    # Placares para os quais você deseja calcular a probabilidade
    placares = ['1x0', '0x1', '1x1', '2x0', '0x2', '2x1', '1x2', '2x2']

    # Lista de dicionários para armazenar os resultados de todos os jogos do dia
    linhas_resultados = []

    # Iterar sobre os jogos e calcular as probabilidades para cada placar
    for index, row in df.iterrows():
        # Calcular as médias de gols esperados para cada time e o total esperado
        lambda_home = row['XG_Home']
        lambda_away = row['XG_Away']
        lambda_total = row['Media_Gols']

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

        # Criar um dicionário para o resultado deste jogo
        linha_resultado = {
            'Date': row['Date'],
            'Hora': row['Hora'],
            'Pais': row['Pais'],
            'Liga': row['Liga'],
            'Home': row['Home'],
            'Away': row['Away'],
            'Odd Casa': row['FT_Odd_H'],
            'Odd Empate': row['FT_Odd_D'],
            'Odd Visitante': row['FT_Odd_A']
        }

        for i, placar in enumerate(placares):
            # Formatar a probabilidade com uma casa decimal e em formato de porcentagem
            prob_formatada = f"{probabilidades[i] * 100:.1f}%"
            linha_resultado[placar] = prob_formatada

        # Adicionar o dicionário à lista
        linhas_resultados.append(linha_resultado)

    # Criar um DataFrame com os resultados
    resultado_global = pd.DataFrame(linhas_resultados)

    # Iniciar aplicativo Streamlit
    st.subheader("Dutching CS")

    # Exibir o DataFrame com os resultados
    st.write(resultado_global)

    # Obter a data atual no formato desejado
    data_atual = datetime.now().strftime('%d/%m/%Y')

    # Criar um link para download do CSV
    csv_link_cs = resultado_global.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="Baixar CSV",
        data=csv_link_cs,
        file_name=f"dutching_cs_{data_atual}.csv",
        key="dutching_cs_csv"
    )

# Chamar a função para executar o aplicativo
cs_page()
