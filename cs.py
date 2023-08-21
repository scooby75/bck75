import streamlit as st
import pandas as pd
from scipy.stats import poisson

def cs_page():
   # URL do arquivo CSV
    url = "https://github.com/scooby75/bdfootball/blob/main/2023-08-22_Jogos_do_Dia_FS.csv?raw=true"
  
    # Carregar o arquivo CSV em um dataframe
    df = pd.read_csv(url)

    # Rename the columns
    df.rename(columns={
        'FT_Odds_H': 'FT_Odd_H',
        'FT_Odds_D': 'FT_Odd_D',
        'FT_Odds_A': 'FT_Odd_A',
        'FT_Odds_Over25': 'FT_Odd_Over25',
        'FT_Odds_Under25': 'FT_Odd_Under25',
        'Odds_BTTS_Yes': 'FT_Odd_BTTS_Yes',
        'ROUND': 'Rodada',
    }, inplace=True)

    # Função para extrair o número do texto "RODADA N"
    def extrair_numero_rodada(text):
        if isinstance(text, int):
            return text
        match = re.search(r'\d+', text)
        if match:
            return int(match.group())
        return None

    # Aplicando a função para extrair o número do "Rodada" e criando uma nova coluna "Rodada_Num"
    df["Rodada_Num"] = df["Rodada"].apply(extrair_numero_rodada)

    # Filtrar jogos com round maior ou igual a 10
    df = df[df['Rodada'] >= 10]

    # Filtrar jogos com home menor ou igual a 1.90
    df = df[(df['FT_Odds_H'] >= 1.4) & (df['FT_Odds_H'] <= 2)]

    # Filtrar jogos com home menor ou igual a 1.80
    df = df[(df['FT_Odds_Under25'] <= 1.80)]

    # Filtrar jogos com XG entre 1 e 1.6 e total XG menor ou igual a 1.60
    df = df[(df['XG_Home_Pre'] >= 1) & (df['XG_Home_Pre'] <= 1.6)]
    df = df[(df['XG_Away_Pre'] >= 1) & (df['XG_Away_Pre'] <= 1.6)]

    # Placares para os quais você deseja calcular a probabilidade
    placares = ['0x0', '1x0', '0x1', '1x1', '2x0', '0x2', '2x1', '1x2', '2x2', '3x0', '0x3', '3x2', '3x3', '4x0', '4x1', '4x2', '4x3', '4x4', '5x0', '5x1', '5x2', '5x3']

    # Lista para armazenar as linhas dos resultados
    linhas_resultados = []

    # Iterar sobre os jogos e calcular as probabilidades para cada placar
    for index, row in df.iterrows():
        # Calcular as médias de gols esperados para cada time e o total esperado
        lambda_home = row['XG_Home_Pre']
        lambda_away = row['XG_Away_Pre']
        

        # Calcular as probabilidades usando a distribuição de Poisson
        probabilidades = []
        total_prob = 0  # Total de probabilidade para normalização

        for placar in placares:
            placar_split = placar.split('x')
            gols_home = int(placar_split[0])
            gols_away = int(placar_split[1])

            prob_home = poisson.pmf(gols_home, lambda_home)
            prob_away = poisson.pmf(gols_away, lambda_away)
            

            # Aplicar o ajuste de zero inflado para placares "estranhos"
            if (lambda_home < gols_home) or (lambda_away < gols_away):
                prob_placar = prob_home * prob_away * 2
            else:
                prob_placar = prob_home * prob_away 

            total_prob += prob_placar
            probabilidades.append(prob_placar)

        # Normalizar as probabilidades para que a soma seja 100%
        probabilidades = [prob / total_prob for prob in probabilidades]

        # Criar uma linha para o resultado deste jogo
        linha_resultado = {
            'Date': row['Date'],
            'Time': row['Time'],
            'League': row['League'],
            'Home': row['Home'],
            'Away': row['Away'],
            'FT_Odds_H': row['FT_Odds_H'],
            'FT_Odds_D': row['FT_Odds_D'],
            'FT_Odds_A': row['FT_Odds_A']
        }

        for i, placar in enumerate(placares):
            linha_resultado[placar] = round(probabilidades[i] * 100, 2)

        linhas_resultados.append(linha_resultado)

    # Criar um novo DataFrame com os resultados
    resultado_df = pd.DataFrame(linhas_resultados)

    # Iniciar aplicativo Streamlit
    st.subheader("Probabilidade de Placar")

    # Loop para exibir os detalhes e a tabela
    for index, row in resultado_df.iterrows():
        details1 = f"**Hora:** {row['Time']}  |  **Home:** {row['Home']}  |  **Away:** {row['Away']}"
        details2 = f"**Odd Casa:** {row['FT_Odds_H']} |  **Odd Empate:** {row['FT_Odds_D']} |  **Odd Visitante:** {row['FT_Odds_A']}"
        st.write(details1)
        #st.write(details2)

        # Criar um DataFrame temporário apenas com as probabilidades para o jogo atual
        prob_game_df = resultado_df[placares].iloc[[index]]

        # Selecionar os 6 placares mais prováveis
        top_placares = prob_game_df.T.nlargest(8, index)[index].index

        # Filtrar o DataFrame temporário para incluir apenas os 6 placares mais prováveis
        prob_game_df = prob_game_df[top_placares]

        # Formatar e exibir a tabela
        formatted_df = prob_game_df.applymap(lambda x: f"{x:.1f}%")
        st.dataframe(formatted_df)

# Chamar a função para executar o aplicativo
cs_page()


