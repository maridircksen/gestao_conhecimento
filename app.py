import pandas as pd
import streamlit as st

# Função para carregar a base de dados
@st.cache_data
def load_database():
    # Carrega os dados do Excel
    df = pd.read_excel('data/Cup.Russia.Matches.xlsx')
    # Converte as colunas de Horário no Brasil e Data para string
    df['Horário no Brasil'] = df['Horário no Brasil'].astype(str)
    df['Data'] = df['Data'].astype(str)
    return df

# Carrega o dataframe no estado da sessão
st.session_state['df'] = load_database()

# Definição das dimensões, medidas e agregadores
st.session_state['dimensao'] = [
    'Grupo', 'Estádio', 'Cidade', 'Time da Casa', 'Time Visitante', 
    'Condições de Vitória', 'Vencedor'
]
st.session_state['dimensao_tempo'] = ['Horário no Brasil', 'Data']
st.session_state['medida'] = [
    'Gols Time da Casa', 'Gols Time Visitante', 'Total de Gols', 'Presença'
]
st.session_state['agregador'] = ['sum', 'mean', 'count', 'min', 'max']

# Título da aplicação
st.title('Copa do Mundo de 2018')

# Estrutura de navegação do app
pg = st.navigation(
    {
        "Introdução": [
            st.Page(page='introducao/tabela.py', title='Tabela', icon=':material/house:'),
            st.Page(page='introducao/cubo.py', title='Cubo', icon=':material/help:'),
            st.Page(page='introducao/dashboard.py', title='Dashboard', icon=':material/help:'),
            st.Page(page='introducao/visualizacao.py', title='Visualização', icon=':material/help:'),
        ],

        "Visualização":[
            st.Page(page='visualizacao/descritiva.py', title='Descritiva', icon=':material/help:'),
            st.Page(page='visualizacao/diagnostica.py', title='Diagnóstica', icon=':material/help:'),
        ]
    }
)

# Executa o sistema de navegação
pg.run()
