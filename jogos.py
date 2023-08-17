import streamlit as st

def jogos_do_dia_page():
    st.set_page_config(page_title="Football Data Analysis", layout="wide")
    st.title("Jogos do Dia")

    # Carregar os dados dos jogos (substitua esta parte com seus dados reais)
    jogos = [
        {"Time": "14:00", "Equipe 1": "Time A", "Equipe 2": "Time B", "Placar": "2 - 1"},
        {"Time": "16:00", "Equipe 1": "Time C", "Equipe 2": "Time D", "Placar": "0 - 0"},
        # ... adicione mais jogos
    ]

    # Exibir a tabela de jogos
    st.write("Próximos Jogos:")
    for jogo in jogos:
        st.write(f"{jogo['Time']} - {jogo['Equipe 1']} vs {jogo['Equipe 2']}, Placar: {jogo['Placar']}")

    # Componente interativo: filtro por liga
    ligas = ["Premier League", "La Liga", "Serie A", "Bundesliga"]
    selected_liga = st.selectbox("Filtrar por Liga:", ligas)
    st.write(f"Exibindo jogos da liga: {selected_liga}")

    # Componente interativo: filtro por rodada
    rodadas = [1, 2, 3, 4, 5]  # Exemplo de rodadas (substitua com suas rodadas reais)
    selected_rodada = st.selectbox("Filtrar por Rodada:", rodadas)
    st.write(f"Exibindo jogos da rodada: {selected_rodada}")

    # Créditos
    st.text("Desenvolvido por Lyssandro Silveira")
    st.markdown("Fale Comigo [link](https://t.me/Lyssandro)")

# Run the Streamlit app
if __name__ == '__main__':
    jogos_do_dia_page()

