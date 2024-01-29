# BIBLIOTECAS IMPORTADAS:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import datetime
from datetime import timedelta
import streamlit as st


# FUNÇÃO CRIAR LINHAS:
def linha():
    print('-' * 37)


# SIGLA E NOME DO ATIVO ANALISADO:
sigla_ativo = "MNQ=F"
nome_ativo = "NASDAQ 100 FUTUROS"

data_hoje = datetime.date.today()
data_hoje.isoformat()


# DEMARCAÇÃO NO GRÁFICO DO DIA ATUAL:
adicao_data_marcacao = timedelta(1)
inicio_negociacao_atual = data_hoje - adicao_data_marcacao
inicio_marcacao = data_hoje
final_marcacao = data_hoje + adicao_data_marcacao


# DADOS HISTÓRICOS PERÍODO DE VENCIMENTO:
data_inicial_vencimento = '2022-12-16'
data_final_vencimento = '2024-03-15'

dados_historico_vencimento = yf.download(sigla_ativo, data_inicial_vencimento, data_final_vencimento, interval='1d')
dados_historico_vencimento['Volatilidade'] = dados_historico_vencimento['High'] - dados_historico_vencimento['Low']


# FILTRO DE TODO O PERÍODO DE VENCIMENTO:
periodo_vencimento_filtrado = dados_historico_vencimento['Volatilidade'][0:-1]


# QUANTIDADE DE PREGÃO NO PERÍODO:
quantidade_pregao = dados_historico_vencimento['Close'].count()


# CÁLCULO DO DESVIO PADRÃO DE TODO ESSE VENCIMENTO:
desvio_padrao = np.std(periodo_vencimento_filtrado)
meio_desvio_padrao = desvio_padrao / 2


# DADOS HISTÓRICOS PERÍODO INTRADAY:
adicao_data_intraday = timedelta(1)
subtracao_data_intraday = timedelta(1)
data_inicial_intraday = data_hoje - adicao_data_intraday
data_final_intraday = data_hoje + subtracao_data_intraday

dados_historico_intraday = yf.download(sigla_ativo, data_inicial_intraday, data_final_intraday, interval='5m')

maxima = dados_historico_intraday['High']

minima = dados_historico_intraday['Low']

ultimo_preco = dados_historico_intraday['Close'][-1]

ultima_maxima = dados_historico_intraday['High'][-1]
ultima_minima = dados_historico_intraday['Low'][-1]


# RANGE DO DIA:
dados_historico_vencimento['range'] = dados_historico_vencimento['High'] - dados_historico_vencimento['Low']
range_do_dia = dados_historico_vencimento['range'][-1]


# DATA DO PREGÃO ATUAL:
pregao_atual = dados_historico_vencimento.index[-1]


# PREÇO DO ÚLTIMO FECHAMENTO E ÚLTIMA ABERTURA:
# PREENCHER OS VALORES ABAIXO:
preco_ultimo_fechamento = dados_historico_vencimento['Close'][-2]
ultima_abertura = dados_historico_vencimento['Open'][-1]


# CÁLCULO PARA ANÁLISE DESVIO PADRÃO:*
mais_2dp = (preco_ultimo_fechamento + (desvio_padrao * 2))
mais_1dp_e_meio = (preco_ultimo_fechamento + (meio_desvio_padrao * 3))
mais_1dp = (preco_ultimo_fechamento + (desvio_padrao))
mais_meio_desvio_padrao = (preco_ultimo_fechamento + meio_desvio_padrao)

menos_meio_desvio_padrao = (preco_ultimo_fechamento - meio_desvio_padrao)
menos_1dp = (preco_ultimo_fechamento - (desvio_padrao))
menos_1dp_e_meio = (preco_ultimo_fechamento - (meio_desvio_padrao * 3))
menos_2dp = (preco_ultimo_fechamento - (desvio_padrao * 2))


with st.sidebar:
    inserir = int(st.number_input("Digite a Quantidade de Meios Desvios Padrões para gerar: "))



def gerar_dp(meio_desvio_padrao):
    input_dp = int(inserir)
    lista_dps = []

    # Gerando desvios padrões positivos e negativos
    for i in range(-input_dp, input_dp + 1):
        if i != 0:  # Ignorando o zero
            total_meio_dp = i * meio_desvio_padrao
            lista_dps.append((i * 0.5, total_meio_dp))

    return lista_dps

# Substitua '10' pelo valor real do seu meio desvio padrão
meio_desvio_padrao = meio_desvio_padrao
df_dp = pd.DataFrame(gerar_dp(meio_desvio_padrao), columns=['DESVIOS PADRÕES', 'VALOR POR DP'])

# Adicionando um índice ao DataFrame
df_dp.index = pd.RangeIndex(start=1, stop=len(df_dp) + 1, step=1)


# DADOS DO CONTRATO:
linha()
print(f'Desvio Padrão: {desvio_padrao:.2f} Pontos.')
print(f'Meio Desvio Padrão: {meio_desvio_padrao:.2f} Pontos.')
print(f'Range de Hoje: ......... {range_do_dia:.2f}.')
print(f'Total de pregões analisados: {quantidade_pregao}.')
print(f'Data inicial do contrato: {data_inicial_vencimento}.')
print(f'Data final do contrato: {data_final_vencimento}.')
print(f'Cálculo para Daytrade no dia:\n {data_hoje}.')
print(f'Gráfico visualizado entre os dias:\n {data_inicial_intraday} ao {data_final_intraday}.')
linha()


# RELATÓRIO PREÇOS COM DESVIO PADRÃO:
linha()
print('|    RELATÓRIO DE DESVIO PADRÃO:    |')
linha()
print(f'| + 2 DP: ................ {mais_2dp:.2f} |')
linha()
print(f'| + 1 e Meio DP: ......... {mais_1dp_e_meio:.2f} |')
linha()
print(f'| + 1 DP: ................ {mais_1dp:.2f} |')
linha()
print(f'| + Meio DP: ............. {mais_meio_desvio_padrao:.2f} |')
linha()
print(f'| Preço Último Fechamento: {preco_ultimo_fechamento:.2f} |')
linha()
print(f'| Última Abertura: ....... {ultima_abertura:.2f} |')
linha()
print(f'| - Meio DP: ............. {menos_meio_desvio_padrao:.2f} |')
linha()
print(f'| - 1 DP: ................ {menos_1dp:.2f} |')
linha()
print(f'| - 1 e Meio DP: ......... {menos_1dp_e_meio:.2f} |')
linha()
print(f'| - 2 DP: ................ {menos_2dp:.2f} |')
linha()


# ... [restante do código anterior] ...

# PLOTAR GRÁFICO INTRADAY DO ATIVO ANALISADO COM MATPLOTLIB:
grafico = plt.figure(figsize=(19.2, 8.2), facecolor='#111111')
ax = plt.axes()
ax.set_facecolor('#111111')
dados_historico_intraday['Adj Close'].plot(label=f'Nasdaq Fech. 5min ..... {ultimo_preco:.2f}', lw=2, color= '#33ffff')
maxima.plot(label=f'Nasdaq Máx. 5min ..... {ultima_maxima:.2f}', ls='--', lw=2, color= 'orange')
minima.plot(label=f'Nasdaq Mín. 5min ...... {ultima_minima:.2f}', ls='--', lw=2, color= '#7fff00')

# Ordenando os desvios padrões e adicionando ao gráfico
df_dp_ordenado = df_dp.sort_values(by='VALOR POR DP', ascending=False)
for index, row in df_dp_ordenado.iterrows():
    color = 'red' if row['VALOR POR DP'] > 0 else 'green'
    plt.axhline(preco_ultimo_fechamento + row['VALOR POR DP'], color=color, ls='--', lw=2, label=f'DP {row["DESVIOS PADRÕES"]}: {preco_ultimo_fechamento + row["VALOR POR DP"]:.2f}')

# Linhas de último fechamento e última abertura
plt.axhline(preco_ultimo_fechamento, color='blue', ls='--', lw=2, label=f'Último Fechamento: .... {preco_ultimo_fechamento:.2f}')
plt.axhline(ultima_abertura, color='white', ls='--', lw=2, label=f'Última Abertura: ......... {ultima_abertura:.2f}')

# Mantendo as marcações verticais
plt.axvline(inicio_marcacao, color='#ffd700', label=f'Inicio dia atual ......... {inicio_marcacao}')
plt.axvline(final_marcacao, color='#ffd700', label=f'Fim dia atual ............ {final_marcacao}')

plt.title(f"GRÁFICO INTRADIÁRIO DO {nome_ativo} ({sigla_ativo}), {pregao_atual}", color='#7fff00', fontsize=18)
plt.ylabel('Preço do Ativo', color='r', fontsize=12)
plt.xlabel('Data Histórico', color='r', fontsize=12)

# Configurando a legenda
plt.legend(facecolor='w', frameon=True, framealpha=0.8, loc='upper left')
plt.grid(color='white')
plt.show()

# Gráfico interativo do Nasdaq com Plotly:
fig = go.Figure(data=[go.Candlestick(x=dados_historico_intraday.index,
                open=dados_historico_intraday['Open'],
                high=dados_historico_intraday['High'],
                low=dados_historico_intraday['Low'],
                close=dados_historico_intraday['Close'])])

# Adicionando linhas de desvio padrão do DataFrame df_dp
for index, row in df_dp.iterrows():
    color = 'green' if row['VALOR POR DP'] < 0 else 'red'
    fig.add_hline(preco_ultimo_fechamento + row['VALOR POR DP'], line=dict(color=color, width=2, dash='dash'), name=f'DP {row["DESVIOS PADRÕES"]}: {preco_ultimo_fechamento + row["VALOR POR DP"]:.2f}')

fig.add_hline(preco_ultimo_fechamento, line=dict(color='blue', width=2, dash='dash'), name=f'Último Fechamento: {preco_ultimo_fechamento:.2f}')
fig.add_hline(ultima_abertura, line=dict(color='white', width=2, dash='dash'), name=f'Última Abertura: {ultima_abertura:.2f}')
fig.add_vline(inicio_marcacao, name=('Início dia atual'), line=dict(color='yellow'))
fig.add_vline(final_marcacao, name=('Término dia atual'), line=dict(color='yellow'))
fig.update_layout(title=f"GRÁFICO INTRADIÁRIO DO {nome_ativo} ({sigla_ativo}), {pregao_atual}", xaxis_title='Data Histórico', yaxis_title='Preço Ativo', template = 'plotly_dark', title_x=0.5)
fig.update_layout(xaxis_rangeslider_visible=False)
fig.update_layout(height=720, width=1080)


with st.container():
    st.header('Gráfico Estático:')
    st.pyplot(grafico)

with st.container():
    st.header('Gráfico Interativo:')
    st.plotly_chart(fig)
    
