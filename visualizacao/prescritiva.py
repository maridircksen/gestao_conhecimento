import streamlit as st
import pandas as pd
from prophet import Prophet
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
from streamlit_extras.metric_cards import style_metric_cards

# Configura o estilo das métricas exibidas
style_metric_cards(
    border_left_color="#9AD8E1",
    background_color="#fff",
    border_size_px=1,
    border_color="#CCC",
    border_radius_px=5,
    box_shadow=True
)

# Carrega o DataFrame da sessão
df = st.session_state.get('df', pd.DataFrame())

# Exibe as colunas disponíveis no DataFrame para auxiliar na escolha
st.write("Colunas disponíveis no DataFrame:", df.columns)

# Define uma coluna de categoria existente
if 'Grupo' in df.columns:  # Substitua 'Grupo' com a coluna categórica existente
    categoria_coluna = 'Grupo'
else:
    st.error("Nenhuma coluna de categoria ('Grupo' ou alternativa) encontrada no DataFrame.")
    st.stop()

# Converte a coluna 'Data' para datetime se existir
if 'Data' in df.columns:
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
else:
    st.error("A coluna 'Data' não está disponível no DataFrame.")
    st.stop()

# Calcula projeções e otimizações ao pressionar o botão
if st.button('Calcular'):
    # Agrupamento de dados por 'Data' e a coluna de categoria definida
    grupo = df.groupby(['Data', categoria_coluna])[st.session_state['medida']].sum().reset_index()
    projecao = pd.DataFrame()

    # Barra de status durante a execução da projeção
    with st.status('Executando Projeção', expanded=True) as status:
        for sub in grupo[categoria_coluna].unique():
            st.write(f"Processando categoria: {sub}")
            grupo_sub = grupo[grupo[categoria_coluna] == sub]
            
            # Projeção para cada medida
            for medida in st.session_state['medida']:
                grupo_medida = grupo_sub[['Data', medida]].dropna()  # Remove NaNs
                
                # Verifica se há dados suficientes para realizar a projeção
                if len(grupo_medida) < 2:
                    st.write(f"Dados insuficientes para a medida '{medida}' na categoria '{sub}'. Projeção ignorada.")
                    continue  # Pula para a próxima medida ou categoria

                grupo_medida.columns = ['ds', 'y']
                future = Prophet().fit(grupo_medida).make_future_dataframe(periods=1, freq='MS')
                forecast = Prophet().fit(grupo_medida).predict(future)
                
                # Extrai o último valor previsto
                forecast = forecast.tail(1)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
                forecast[categoria_coluna] = sub
                forecast['medida'] = medida
                projecao = pd.concat([projecao, forecast])
        
        # Atualiza o status para "Completo"
        status.update(label="Projeção Completa!", state="complete", expanded=False)

    # Formata a projeção em uma tabela pivotada
    projecao_pivot = projecao.pivot_table(index=categoria_coluna, columns='medida', values='yhat', aggfunc='sum').reset_index()
    st.subheader('Valores Projetados')
    st.dataframe(projecao_pivot, use_container_width=True, hide_index=True, height=650)

    # Verifica se as colunas necessárias para métricas estão presentes
    for col in ['Gols Time da Casa', 'Gols Time Visitante', 'Total de Gols', 'Presença']:
        if col not in projecao_pivot.columns:
            st.error(f"A coluna '{col}' é necessária para o cálculo de métricas, mas não está no DataFrame.")
            st.stop()

    # Calcula valores totais e exibe as métricas
    valor_total = projecao_pivot['Gols Time da Casa'].sum() + projecao_pivot['Gols Time Visitante'].sum()
    unidades = projecao_pivot['Total de Gols'].sum() * 0.7
    cols = st.columns(5)
    cols[0].metric('Valor Projetado para Compras', round(valor_total, 2))
    cols[1].metric('Valor Projetado para Unidades', round(unidades, 0))

    # Configuração do modelo de otimização em Pyomo
    indice = list(projecao_pivot.index.values)
    lucro = projecao_pivot['Gols Time Visitante'].values
    quantidade = projecao_pivot['Total de Gols'].values
    valor = projecao_pivot['Gols Time da Casa'].values
    model = pyo.ConcreteModel()
    model.x = pyo.Var(indice, within=pyo.Binary)
    x = model.x

    # Restrições de valor e quantidade
    model.valores_constraint = pyo.Constraint(expr=sum([x[p] * valor[p] for p in indice]) <= valor_total)
    model.quantidade_constraint = pyo.Constraint(expr=sum([x[p] * quantidade[p] for p in indice]) <= unidades)

    # Função objetivo para maximizar lucro
    model.objective = pyo.Objective(expr=sum([x[p] * lucro[p] for p in indice]), sense=pyo.maximize)

    # Solver GLPK
    opt = SolverFactory('glpk', executable='C:/Users/maria/OneDrive/Área de Trabalho/FACULDADE/gestao_conhecimento/visualizacao/w64/glpsol.exe')
    results = opt.solve(model)
    solution = [int(pyo.value(model.x[p])) for p in indice]

    # Atualiza o DataFrame com a solução
    projecao_pivot['Comprar'] = solution
    cols[2].metric('Valor Otimizado Compras', round(projecao_pivot[projecao_pivot['Comprar'] == 1]['Gols Time da Casa'].sum(), 2))
    cols[3].metric('Quantidade Otimizada Compras', round(projecao_pivot[projecao_pivot['Comprar'] == 1]['Total de Gols'].sum(), 0))
    cols[4].metric('Lucro Otimizado Compras', round(projecao_pivot[projecao_pivot['Comprar'] == 1]['Gols Time Visitante'].sum(), 2))

    # Exibe a tabela final com valores otimizados
    st.subheader('Valores Otimizados')
    st.dataframe(projecao_pivot, use_container_width=True, hide_index=True, height=650)
