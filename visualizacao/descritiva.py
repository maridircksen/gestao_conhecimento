import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Definindo as colunas e medidas
cols = st.columns(3)
colunas = cols[0].multiselect(
    'Dimensões Coluna',
    st.session_state['dimensao'] + st.session_state['dimensao_tempo']
)
valor = cols[1].selectbox(
    'Medidas',
    st.session_state['medida']
)
cor = cols[2].selectbox(
    'Cor',
    colunas
)

# Criando abas para as visualizações
tabs = st.tabs(['Treemap', 'Sunburst', 'Sankey', 'TimeSeries'])

# Verifica se mais de duas colunas foram selecionadas
if len(colunas) > 2:
    with tabs[0]:
        # Gráfico Treemap
        fig = px.treemap(
            st.session_state['df'],
            path=colunas,
            values=valor,
            color=cor,
            height=800,
            width=1200
        )
        fig.update_traces(textinfo='label+value')
        st.plotly_chart(fig)

    with tabs[1]:
        # Gráfico Sunburst
        fig = px.sunburst(
            st.session_state['df'],
            path=colunas,
            values=valor,
            color=cor,
            height=800,
            width=1200
        )
        fig.update_traces(textinfo='label+value')
        st.plotly_chart(fig)

    with tabs[2]:
        # Gráfico Sankey
        grupo = st.session_state['df'].groupby(colunas)[valor].sum().reset_index().copy()
        rotulos, codigo = [], 0
        for coluna in colunas:
            for conteudo in grupo[coluna].unique():
                rotulos.append([codigo, conteudo])
                codigo += 1
        rotulos = pd.DataFrame(rotulos, columns=['codigo', 'conteudo'])
        rotulos['codigo'] = rotulos['codigo'].astype(int)
        sankey = []
        for i in range(len(colunas) - 1):
            for index, row in grupo.iterrows():
                sankey.append(
                    [
                        rotulos[rotulos['conteudo'] == row[colunas[i]]]['codigo'].values[0],
                        rotulos[rotulos['conteudo'] == row[colunas[i+1]]]['codigo'].values[0],
                        row[valor],
                        row[valor]
                    ]
                )
        sankey = pd.DataFrame(sankey, columns=['source', 'target', 'value', 'label'])
        data_trace = dict(
            type='sankey', domain=dict(x=[0, 1], y=[0, 1]),
            orientation="h",
            valueformat=".2f",
            node=dict(pad=10, thickness=30, line=dict(color="black", width=0.5),
                label=rotulos['conteudo'].to_list()
            ),
            link=dict(
                source=sankey['source'].dropna(axis=0, how='any'),
                target=sankey['target'].dropna(axis=0, how='any'),
                value=sankey['value'].dropna(axis=0, how='any'),
                label=sankey['label'].dropna(axis=0, how='any'),
            )
        )
        layout = dict(
            title="Hierarquias",
            height=800,
            width=1200,
            font=dict(size=10),
        )
        fig = go.Figure(dict(data=[data_trace], layout=layout))
        st.plotly_chart(fig)

    with tabs[3]:
        # Série temporal
        for coluna in colunas:
            base = st.session_state['df'][
                (st.session_state['df']['Data'] == st.session_state['df']['Data'].max()) &
                (st.session_state['df']['Time da Casa'] == st.session_state['df']['Time da Casa'].max())
            ].pivot_table(index='Data', columns=coluna, values=valor, aggfunc='sum').reset_index()
            st.plotly_chart(
                px.line(
                    base,
                    x='Data',
                    y=base.columns,
                )
            )
