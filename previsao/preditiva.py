import streamlit as st
import pandas as pd
from prophet import Prophet
from sklearn.ensemble import RandomForestRegressor
import random

# Carregar variáveis de sessão necessárias
df = st.session_state.get('df', pd.DataFrame())
dimensao = st.session_state.get('dimensao', [])
dimensao_tempo = st.session_state.get('dimensao_tempo', [])
medida = st.session_state.get('medida', [])

# Criar uma coluna de mês para a projeção, se ainda não existir
if 'Order Date Month' not in df.columns and 'Data' in df.columns:
    df['Order Date Month'] = pd.to_datetime(df['Data']).dt.to_period('M').astype(str)

tabs = st.tabs(['Projeção de Valores', 'Previsão de Valor'])

# Projeção de Valores usando Prophet
with tabs[0]:
    selected_medida = st.selectbox('Medidas para Predição', medida)
    if st.checkbox('Calcular Previsão'):
        # Agrupamento por mês usando a nova coluna
        projecao = df.groupby('Order Date Month')[[selected_medida]].sum().reset_index()
        projecao.columns = ['ds', 'y']  # Necessário para o Prophet
        projecao['ds'] = pd.to_datetime(projecao['ds'])  # Converter para datetime

        # Criar o modelo e gerar previsão
        model = Prophet().fit(projecao)
        future = model.make_future_dataframe(periods=12, freq='MS')
        forecast = model.predict(future)

        # Exibir o gráfico e os dados previstos
        cols = st.columns(2)
        cols[0].pyplot(model.plot(forecast))
        cols[1].dataframe(
            forecast.tail(12)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']],
            hide_index=True,
            use_container_width=True,
            height=480
        )

# Previsão de Valor usando RandomForestRegressor
with tabs[1]:
    selected_medida = st.selectbox('Selecione a Medida', medida)
    selected_dimensao = st.multiselect('Selecione a dimensão: ', dimensao + dimensao_tempo)
    if len(selected_dimensao) > 0:
        if st.checkbox('Calcular'):
            regressao = df[[selected_medida] + selected_dimensao]
            dummies = pd.get_dummies(df[selected_dimensao])
            rf = RandomForestRegressor(n_estimators=1000, random_state=42)
            rf.fit(dummies, df[selected_medida])

            # Amostra de previsão
            amostra = dummies.sample(n=10, random_state=42)
            previsao = rf.predict(amostra)
            amostra['previsao'] = previsao

            # Exibição dos resultados
            result_tabs = st.tabs(['DataFrame', 'Dummies', 'Amostra'])
            with result_tabs[0]:
                st.dataframe(regressao, use_container_width=True)
            with result_tabs[1]:
                st.dataframe(dummies, use_container_width=True)
            with result_tabs[2]:
                st.dataframe(amostra, use_container_width=True)
