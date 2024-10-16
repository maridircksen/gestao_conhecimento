import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from itertools import combinations

# Estilo dos cartões de métrica
style_metric_cards(
    border_left_color="#3D5077",
    background_color="#F0F2F6",
    border_size_px=3,
    border_color = "#CECED0",
    border_radius_px = 20,
    box_shadow=True
)

# Definindo as colunas e seleções
cols = st.columns(4)
coluna = cols[0].selectbox(
    'Dimensões Coluna',
    st.session_state['dimensao']
)
conteudo = cols[1].selectbox(
    'Classe:',
    st.session_state['df'][coluna].unique()
)
medida = cols[2].selectbox(
    'Medida',
    st.session_state['medida']
)
mes = cols[3].selectbox(
    'Mês',
    st.session_state['df'][['Data']].sort_values(by='Data').drop_duplicates()['Data']
)

# Filtrando os dados pelo mês selecionado
mes_atual = st.session_state['df'][
    (st.session_state['df']['Data'] == mes)
]

# Definindo novas colunas
cols = st.columns([1,3])
cols[0].subheader(f'Métrica de {medida} no mês {mes}')

# Ajuste para evitar erro de subtração entre string e int
try:
    mes_int = int(mes)
except ValueError:
    mes_int = None

# Exibindo métricas em relação ao mês anterior e ao ano anterior
if mes_int == 1:
    cols[0].metric(
        label=f'{medida} em relação ao mês anterior',
        value=round(mes_atual[medida].sum(), 2)
    )
elif mes_int is not None:
    mes_anterior = st.session_state['df'][
        (st.session_state['df']['Data'] == str(mes_int - 1))
    ]
    cols[0].metric(
        label=f'{medida} em relação ao mês anterior',
        value=round(mes_atual[medida].sum(), 2),
        delta=str(round(mes_atual[medida].sum() - mes_anterior[medida].sum(), 2)),
    )

# Comparação com o mesmo mês do ano anterior
mes_ano_anterior = st.session_state['df'][
    (st.session_state['df']['Data'] == mes)
]
cols[0].metric(
    label=f'{medida} em relação ao mês no ano anterior',
    value=round(mes_atual[medida].sum(), 2),
    delta=str(round(mes_atual[medida].sum() - mes_ano_anterior[medida].sum(), 2)),
)

# Exibindo gráfico de boxplot
cols[0].subheader(f'Comparativo em {coluna}')
cols[0].plotly_chart(
    px.box(
        mes_atual,
        x=coluna,
        y=medida
    )
)

# Teste de Tukey se houver grupos suficientes
if len(mes_atual[coluna].unique()) > 1:
    tukeyhsd = pairwise_tukeyhsd(endog=mes_atual[medida], groups=mes_atual[coluna], alpha=0.05)
    tukey = []
    for grupo in list(combinations(tukeyhsd.groupsunique, 2)):
        tukey.insert(len(tukey), [grupo[0], grupo[1]])
    tukey = pd.DataFrame(tukey, columns=['grupo1', 'grupo2'])
    tukey['reject'] = tukeyhsd.reject
    tukey['meandiffs'] = tukeyhsd.meandiffs
    if cols[0].toggle('Todos'):
        cols[0].dataframe(tukey, use_container_width=True, hide_index=True)
    else:
        cols[0].dataframe(tukey[tukey['reject']], use_container_width=True, hide_index=True)
else:
    cols[0].text('Não há grupos suficientes para realizar a comparação múltipla com o teste de Tukey.')

# Indicador visual e gráfico de evolução temporal
with cols[1]:
    cols[1].subheader(f'Indicador de {medida} em {coluna}({conteudo}) no mês {mes}')
    meses = st.session_state['df'][
        st.session_state['df'][coluna] == conteudo
    ].groupby(['Data'])[medida].sum().reset_index()

    # Gráfico do indicador com medidor
    fig = go.Figure(
        go.Indicator(
            mode="number+gauge+delta",
            gauge={
                'shape': "bullet",
                'axis': {
                    'visible': True,
                    'range': [
                        meses[medida].min(),
                        meses[medida].max()
                    ]
                },
                'steps': [
                    {'range': [meses[medida].min(), meses[medida].quantile(0.25)], 'color': "salmon"},
                    {'range': [meses[medida].quantile(0.25), meses[medida].quantile(0.50)], 'color': "lightsalmon"},
                    {'range': [meses[medida].quantile(0.50), meses[medida].quantile(0.75)], 'color': "ivory"},
                    {'range': [meses[medida].quantile(0.75), meses[medida].max()], 'color': "linen"},
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': meses[medida].mean()
                },
                'bar': {'color': "blue"}
            },
            delta={'reference': meses[medida].mean()},
            value=mes_atual[mes_atual[coluna] == conteudo][medida].sum(),
            domain={'x': [0.2, 1], 'y': [0, 1]},
            title={'text': f'{conteudo}'},
        )
    )
    fig.update_layout(height=250)
    cols[1].plotly_chart(fig)

    # Gráfico de evolução temporal
    st.subheader(f'Evolução de {medida} em {coluna} - {conteudo}')
    evolucao = st.session_state['df'][
        (st.session_state['df'][coluna] == conteudo)
    ].groupby(['Data'])[medida].sum().reset_index()

    # Calculando média, intervalo de confiança e outliers
    media = evolucao[medida].mean()
    erro = evolucao[medida].std() * 1.96 / np.sqrt(len(evolucao))
    ls = media + erro
    li = media - erro
    iqr = evolucao[medida].quantile(0.75) - evolucao[medida].quantile(0.25)
    out_max = evolucao[medida].quantile(0.75) + (iqr * 1.5)
    out_min = evolucao[medida].quantile(0.25) - (iqr * 1.5)

    # Classificação das entradas
    evolucao['classe'] = evolucao[medida].apply(
        lambda x : 'outlier acima' if x > out_max else (
            'acima da média' if x > ls else (
                'media' if x > li else (
                    'abaixo da média' if x > out_min else 'outlier abaixo'
                )
            )
        )
    )

    # Exibindo gráfico de barras
    cols[1].plotly_chart(
        px.bar(
            evolucao,
            x='Data',
            y=medida,
            color='classe',
            hover_name=medida,
            color_discrete_map={
                "media": "yellow",
                "abaixo da média": "orange",
                "acima da média": "green",
                "outlier acima": "blue",
                "outlier abaixo": "red"
            }
        )
    )
