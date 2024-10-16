import streamlit as st
import plotly.express as px

# Criação de colunas para selecionar as variáveis
cols = st.columns(3)

# Multiseleção para medidas (Gols)
meds = cols[0].multiselect(
    'Medidas', [
        'Gols Time da Casa',
        'Gols Time Visitante',
        'Total de Gols',
        'Presença'
    ]
)

# Seleção de dimensões categóricas
dims = cols[1].selectbox(
    'Dimensões', [
        'Grupo', 'Estádio', 'Cidade', 'Time da Casa', 'Time Visitante', 'Condições de Vitória', 'Vencedor'
    ]
)

# Seleção de dimensões temporais
time = cols[2].selectbox(
    'Dimensões Tempo', [
        'Horário no Brasil', 'Data'
    ]
)

st.text('Visualização')

# Verifica se há medidas selecionadas
if len(meds) > 0:
    if len(meds) >= 1:
        st.subheader('Distribuição - Histograma')
        st.plotly_chart(
            px.histogram(st.session_state['df'], x=meds)
        )
    
    if len(meds) >= 2:
        st.subheader('Relacionamento - Pontos/Dispersão')
        st.plotly_chart(
            px.scatter(
                st.session_state['df'], x=meds[0], y=meds[1]
            )
        )
    
    if len(meds) == 3:
        st.subheader('Relacionamento - Bolhas')
        try:
            st.plotly_chart(
                px.scatter(st.session_state['df'],
                    x=meds[0], y=meds[1], size=meds[2]
                )
            )
        except ValueError:
            st.text('Não pode haver valores negativos')

    # Agrupamento por dimensões
    gr = st.session_state['df'].groupby(dims)[meds[0]].sum().reset_index()
    with st.expander(label='Mostrar Tabela', expanded=False):
        st.dataframe(
            gr, hide_index=True, use_container_width=True
        )

    # Gráfico de pizza
    st.plotly_chart(
        px.pie(gr, names=dims, values=meds[0], hole=0.5)
    )

    # Agrupamento por dimensões temporais e categóricas
    gr = st.session_state['df'].groupby(
        [time] + [dims])[meds[0]].sum().reset_index()
    
    with st.expander(label='Mostrar Tabela', expanded=False):
        st.dataframe(
            gr, hide_index=True, use_container_width=True
        )

    # Visualização de série temporal
    if len(gr[time].unique()) <= 6:
        if len(gr[dims].unique()) <= 6:
            st.plotly_chart(
                px.bar(
                    data_frame=gr, x=time,
                    y=meds[0], color=dims
                )
            )
        else:
            st.plotly_chart(
                px.area(
                    data_frame=gr,
                    x=time,
                    y=meds[0],
                    color=dims
                )
            )
    else:
        st.plotly_chart(
            px.line(
                data_frame=gr,
                x=time,
                y=meds[0],
                color=dims
            )
        )
