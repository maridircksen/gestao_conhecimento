# Avaliação - Mariana-Dircksen

Esta avaliação tem por objetivo realizar Análise dos Filmes Exibidos entre 2009 a 2019 utilizando uma base de dados disponibilizada em https://www.kaggle.com/datasets/pedrothiago/anlise-dos-filmes-exibidos-2009-a-2019 


**Sobre a Base de Dados** 
A base escolhida tem informações dos filmes exibidos entre 209 e 2019, tal arquivo que se localiza em Data > database_filmes


**Classificação das colunas conforme modelo multidimensional (4W1H)**

Quem (Quem): Refere-se aos sujeitos ou entidades envolvidas no processo.
Colunas: Empresa distribuidora, Origem da empresa distribuidora

O quê (O quê): Refere-se ao objeto ou ao conteúdo do processo.
Colunas: Título da obra, Gênero, Nacionalidade da obra, Países

Onde (Onde): Refere-se à localização ou ao contexto geográfico.
Colunas: Países

Quando (When): Refere-se ao tempo ou ao momento em que o evento ocorre.
Colunas: Ano de exibição

Como (Como): Refere-se ao método ou à quantidade que quantifica ou qualifica o evento.
Colunas: Publico no ano de exibição, Renda no ano de exibição

**Implementação de Cubo de Dados**
Foi implementado um cubo de dados conforme a base escolhida. Onde poderá escolher as categorias que quer ver nas linhas e colunas, um valor numérico para analisar (como vendas ou renda) e como quer agregar esses valores (somar, contar, etc.). Caso sejam escolhidas diferentes linhas e colunas, o código cria uma tabela dinâmica, que organiza os dados para mostrar o valor escolhido de acordo com as categorias que você selecionou. Além disso, ele também mostra uma tabela simples, somando os valores da categoria de linha que você escolheu.

**Visualização**
O usuário pode escolher medidas (como valores numéricos) e dimensões (categorias como país ou gênero) para analisar. Dependendo de quantas medidas o usuário escolhe, diferentes tipos de gráficos são exibidos: Histograma (com 1 medida): mostra a distribuição dessa medida., Gráfico de dispersão (com 2 medidas): mostra a relação entre duas medidas. Gráfico de bolhas (com 3 medidas): visualiza a relação entre três medidas, usando o tamanho das bolhas para a terceira medida. Também há gráficos de pizza e barras/linhas para mostrar como as dimensões escolhidas afetam as medidas ao longo do tempo.

**Rotinas com base na análise de dados**
Aqui estão duas rotinas para cada tipo de análise de dados para ser implemento a base de dados de filmes:

 *1. Análise Descritiva*

Rotina 1: Estatísticas Básicas por Gênero e País
Objetivo: Obter estatísticas básicas sobre o público e a renda, segmentadas por gênero e país.
Passos:
  1. Selecionar Colunas: Usar "Gênero" e "Países" para segmentar e "Público no ano de exibição" e "Renda no ano de exibição" como medidas.
  2. Calcular Estatísticas Descritivas: Agrupar os dados por gênero e país e calcular estatísticas como média e desvio padrão.


Rotina 2: Distribuição de Renda e Público
Objetivo: Analisar a distribuição de renda e público ao longo dos anos.
Passos:
  1. Selecionar Colunas: Usar "Ano de exibição" e "Renda no ano de exibição" ou "Público no ano de exibição".
  2. Criar Gráficos de Distribuição: Gerar histogramas para visualizar a distribuição de renda e público por ano.


 *2. Análise Diagnóstica*

Rotina 1: Análise de Tendências ao Longo dos Anos
Objetivo: Identificar como a renda e o público mudaram ao longo dos anos e relacionar essas mudanças com diferentes gêneros e países.
Passos:
  1. Selecionar Colunas: Usar "Ano de exibição", "Gênero" e "Público no ano de exibição" ou "Renda no ano de exibição".
  2. Criar Gráficos de Linha: Plotar gráficos de linha para mostrar as tendências de renda e público ao longo dos anos.


Rotina 2: Análise de Desvios por País e Gênero
Objetivo: Examinar como os desvios na renda e no público variam entre diferentes países e gêneros.
Passos:
  1. Selecionar Colunas: Usar "Países", "Gênero", "Renda no ano de exibição" e "Público no ano de exibição".
  2. Calcular e Visualizar Desvios: Calcular desvios padrão e criar gráficos para mostrar a variação de renda e público entre diferentes países e gêneros.


 *3. Análise Preditiva*

Rotina 1: Previsão de Renda Futura
Objetivo: Prever a renda futura com base em dados históricos.
Passos:
  1. Preparar Dados: Usar dados históricos de renda e ano de exibição.
  2. Aplicar Modelo de Regressão: Usar um modelo de regressão para prever a renda futura.


Rotina 2: Previsão de Público Futuro
Objetivo: Estimar o público futuro com base em dados passados.
Passos:
  1. Preparar Dados: Usar dados históricos de público e ano de exibição.
  2. Aplicar Modelo de Regressão: Usar um modelo de regressão para prever o público futuro.


 *4. Análise Prescritiva*

Rotina 1: Otimização de Marketing para Aumentar a Renda
Objetivo: Recomendar estratégias para aumentar a renda com base em análises passadas.
Passos:
  1. Analisar Dados Passados: Usar dados sobre renda e fatores que afetam a renda (como gênero e país).
  2. Modelar Estratégias de Marketing: Aplicar modelos de otimização para recomendar estratégias para maximizar a renda.


Rotina 2: Recomendar Filmes com Base em Preferências de Público
Objetivo: Sugerir filmes para promover com base nas preferências do público.
Passos:
  1. Analisar Preferências do Público: Usar dados sobre público e gêneros.
  2. Criar Recomendações: Identificar filmes que têm altos níveis de público em categorias populares.
