import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import yfinance as yf
#import investpy as inv
import seaborn as sns
import fundamentus as fd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from datetime import date


# Página Home_______________________________________________________________________________
def home():    
    col1, col2,col3 = st.columns([1,3,1])
    with col1:   
        st.markdown('---') 
        st.image('grafico_logo.png')

    with col2:
        st.markdown('---')
        st.title('App Financeiro')


    st.header("Taxas de Câmbio")

    # Código HTML do iframe de Taxas de Câmbio do Investing.com
    iframe_code = """
    <iframe frameborder="0" scrolling="auto" height="400" width="1000" allowtransparency="true" 
        marginwidth="0" marginheight="0" 
        src="https://sslfxrates.investing.com/index_exchange.php?params&inner-border-color=%23d1d1d1&border-color=%23000000&bg1=%23F6F6F6&bg2=%23ffffff&inner-text-color=%23000000&currency-name-color=%23000000&header-text-color=%23FFFFFF&header-bg=%23979797&force_lang=12" 
        align="center"></iframe><br />
    <div style="width:540px">
        <a href="http://br.investing.com" target="_blank">
            <img src="https://wmt-invdn-com.investing.com/forexpros_pt_logo.png" alt="Investing.com" title="Investing.com" style="float:left" />
        </a>
        <span style="float:right">
            <span style="font-size: 11px;color: #333333;text-decoration: none;">
                Taxas de Câmbio fornecidas por 
                <a href="https://br.investing.com/" rel="nofollow" target="_blank" 
                style="font-size: 11px;color: #06529D; font-weight: bold;" class="underline_link">
                Investing.com Brasil
                </a>.
            </span>
        </span>
    </div>
    """

    # Renderizando o HTML no Streamlit
    components.html(iframe_code, height=250)





# Página Calendario_______________________________________________________________________
def calendario():    
    st.title("Calendário Econômico")

    # Novo código HTML do iframe do Investing.com
    iframe_code = """
    <iframe src="https://sslecal2.investing.com?columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&importance=2,3&features=datepicker,timezone,timeselector,filters&countries=17,32,37,5,22,39,35,4,12&calType=day&timeZone=12&lang=12" 
        width="700" height="600" frameborder="0" allowtransparency="true" 
        marginwidth="0" marginheight="0"></iframe>
    <div class="poweredBy" style="font-family: Arial, Helvetica, sans-serif;">
        <span style="font-size: 11px;color: #333333;text-decoration: none;">
            Calendário Econômico fornecido por 
            <a href="https://br.investing.com/" rel="nofollow" target="_blank" 
            style="font-size: 11px;color: #06529D; font-weight: bold;" class="underline_link">
            Investing.com Brasil
            </a>.
        </span>
    </div>
    """

    # Renderizando o HTML no Streamlit
    components.html(iframe_code, height=750)





# Página Panorama___________________________________________________________________________
def panorama():
    st.title('Panorama do Mercado')
    st.markdown(date.today().strftime('%d/%m/%Y'))

    st.subheader('Mercados pelo Mundo')

# Criando DataFrame vazio
   # df_info = pd.DataFrame(columns=['Ativo', 'Ticker', 'Ult. Valor', '%'])

# Dicionário de ativos e tickers
    dict_tickers = {
                'Bovespa':'^BVSP', 
                'S&P500':'^GSPC',
                'NASDAQ':'^IXIC', 
                'DAX':'^GDAXI', 
                'FTSE 100':'^FTSE',
                'Cruid Oil': 'CL=F',
                'Gold':'GC=F',
                'BITCOIN':'BTC-USD',
                'ETHEREUM':'ETH-USD'
                }

    df_info = pd.DataFrame({'Ativo': dict_tickers.keys(),'Ticker': dict_tickers.values()})
    
    df_info['Ult. Valor'] = ''
    df_info['%'] = ''
    count =0

    with st.spinner('Baixando cotação...'):
        for ticker in dict_tickers.values():
            cotacoes = yf.download(ticker, period='5d')['Close']
            variacao = (float(cotacoes.iloc[-1]/cotacoes.iloc[-2])-1)*100
            df_info['Ult. Valor'][count] = round(float(cotacoes.iloc[-1]), 2)
            df_info['%'][count] =round(variacao,2)
            count += 1

  #  st.write(df_info)
   
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('Indices')
        st.metric(label=df_info['Ativo'][0], value=df_info['Ult. Valor'][0], delta=str(df_info['%'][0])+ '%')
        st.metric(label=df_info['Ativo'][1], value=df_info['Ult. Valor'][1], delta=str(df_info['%'][1])+ '%')
        st.metric(label=df_info['Ativo'][2], value=df_info['Ult. Valor'][2], delta=str(df_info['%'][2])+ '%')
        st.metric(label=df_info['Ativo'][3], value=df_info['Ult. Valor'][3], delta=str(df_info['%'][3])+ '%')
        st.metric(label=df_info['Ativo'][4], value=df_info['Ult. Valor'][4], delta=str(df_info['%'][4])+ '%')
    
    with col2:
        st.subheader('Commodities')        
        st.metric(label=df_info['Ativo'][5], value=df_info['Ult. Valor'][5], delta=str(df_info['%'][5])+ '%')
        st.metric(label=df_info['Ativo'][6], value=df_info['Ult. Valor'][6], delta=str(df_info['%'][6])+ '%')
    
    with col3:
        st.subheader('Criptos')        
        st.metric(label=df_info['Ativo'][7], value=df_info['Ult. Valor'][7], delta=str(df_info['%'][7])+ '%')
        st.metric(label=df_info['Ativo'][8], value=df_info['Ult. Valor'][8], delta=str(df_info['%'][8])+ '%')
    
    '''    st.markdown('---')
        st.subheader('Comportamento durante o dia')

        lista_indices = ['IBOV', 'S&P500', 'NASDAQ']
        indice = st.selectbox('Selecione o indice', lista_indices)

        if indice == 'IBOV':
            indice_diario = yf.download('^BVSP', period='1d',interval='5m')
        if indice == 'S&P500':
            indice_diario = yf.download('^GSPC', period='1d',interval='5m')
        if indice == 'NASDAQ':
            indice_diario = yf.download('^IXIC', period='1d',interval='5m')
        
        fig = go.Figure(data=[go.Candlestick(x = indice_diario.index,
                                            open = indice_diario['Open'],
                                            high = indice_diario['High'],
                                            low = indice_diario['Low'],
                                            close = indice_diario['Close'])])
        
        fig.update_layout(title=indice, xaxis_rangeslider_visible=False)

        

        st.plotly_chart(fig)'''





# Página Mapa Mensal________________________________________________________________________
def mapa_mensal():
    st.title('Mapa Mensal')

   

    with st.expander('Escolha',expanded=True):
        opcao = st.radio('Selecione',['Índices','Ações'])

    if opcao == 'Índices':
        with st.form(key='form.indice'):
            ticker = st.selectbox('Indice',['Bovespa','Financials','Basic Materials']) 
            analisar = st.form_submit_button('Analisar')
    else:  
        with st.form(key='form_acoes'):
            ticker = st.selectbox('Ações',['PETR4','VALE3','ITUB4']) 
            analisar = st.form_submit_button('Analisar')

    if analisar:
        data_inicial = '01/12/1999'
        data_final = '31/12/2022'

        if opcao == "Índices":
            retornos = inv.get_index_historical_data(ticker, country='brazil',from_date=data_inicial, to_date=data_final,
                                                    interval='Monthly')['Close'].pct_change()
            
        else:
            retornos = inv.get_stock_historical_data(ticker, country='brazil',from_date=data_inicial, to_date=data_final,
                                                    interval='Monthly')['Close'].pct_change()
        
        st.write(retornos)
            




# Página Mapa Mensal________________________________________________________________________
def mapa_mensal():
    st.title('Mapa Mensal')

   

    with st.expander('Escolha', expanded=True):
        opcao = st.radio('Selecione', ['Índices', 'Ações'])

    if opcao == 'Índices':
        indices = {'Bovespa': '^BVSP', 'Financials': '^IXIC', 'Basic Materials': '^GSPC'}
        with st.form(key='form_indice'):
            escolha = st.selectbox('Índice', list(indices.keys()))
            analisar = st.form_submit_button('Analisar')
            ticker = indices[escolha]
    else:
        acoes = {'PETR4': 'PETR4.SA', 'VALE3': 'VALE3.SA', 'ITUB4': 'ITUB4.SA'}
        with st.form(key='form_acoes'):
            escolha = st.selectbox('Ações', list(acoes.keys()))
            analisar = st.form_submit_button('Analisar')
            ticker = acoes[escolha]

    if analisar:
    #    data_inicial = st.date_input("Data Inicial", pd.to_datetime('1999-12-01'))
    #    data_final = st.date_input("Data Final", pd.to_datetime('2022-12-31'))

        data_inicial = ('1999-12-01')
        data_final = ('2030-12-31')

        # Baixa os dados do Yahoo Finance
        dados = yf.download(ticker, start=data_inicial, end=data_final, interval="1mo")

        if not dados.empty:
            retornos = dados['Close'].pct_change().dropna()
            #st.dataframe(retornos)
            # Adiciona colunas de ano e mês para organização
            retornos = retornos.reset_index()
            retornos['Year'] = retornos['Date'].dt.year
            retornos['Month'] = retornos['Date'].dt.month

        # Criar a tabela pivot sem média, apenas reorganizando os dados
            tabela_retornos = retornos.pivot(index='Year', columns='Month', values=ticker)
            tabela_retornos.columns = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                                            'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

            #st.write(tabela_retornos_pivot)
            
    # Criando Heatmap
    # Heatmap
            fig, ax = plt.subplots(figsize=(12, 9))
            cmap = sns.color_palette('RdYlGn', 15)
            sns.heatmap(tabela_retornos, cmap=cmap, annot=True, fmt='.2%', center=0, vmax=0.025, vmin=-0.025, cbar=False,
                        linewidths=0.5, xticklabels=True, yticklabels=True, ax=ax)
            ax.set_title(f'Heatmap Retorno Mensal - {escolha}', fontsize=18)
            ax.set_yticklabels(ax.get_yticklabels(), rotation=0, verticalalignment='center', fontsize='12')
            ax.set_xticklabels(ax.get_xticklabels(), fontsize='12')
          #  ax.xaxis.tick_top()  # x axis em cima
            plt.ylabel('')
            st.pyplot(fig)
       
        else:
            st.error("Erro ao buscar os dados. Verifique o ticker ou tente novamente mais tarde.")
    
    #Estatisticas
        stats = pd.DataFrame(tabela_retornos.mean(), columns=['Média'])
        stats['Mediana'] = tabela_retornos.median()
        stats['Maior'] = tabela_retornos.max()
        stats['Menor'] = tabela_retornos.min()
        stats['Positivos'] = tabela_retornos.gt(0).sum()/tabela_retornos.count() # .gt(greater than) = Contagem de números maior que zero
        stats['Negativos'] = tabela_retornos.le(0).sum()/tabela_retornos.count() # .le(less than) = Contagem de nomeros menor que zero

    #Stats_A
        stats_a = stats[['Média','Mediana','Maior','Menor']]
        stats_a = stats_a.transpose()

        fig, ax = plt.subplots(figsize=(12, 2))
        sns.heatmap(stats_a, cmap=cmap, annot=True, fmt='.2%', center=0, vmax=0.025, vmin=-0.025, cbar=False,
                        linewidths=0.5, xticklabels=True, yticklabels=True, ax=ax)
        st.pyplot(fig)
        
    #Stats_B
        stats_b = stats[['Positivos','Negativos']]
        stats_b = stats_b.transpose()

        fig, ax = plt.subplots(figsize=(12, 1))
        sns.heatmap(stats_b, annot=True, fmt='.2%', center=0, vmax=0.025, vmin=-0.025, cbar=False,
                        linewidths=0.5, xticklabels=True, yticklabels=True, ax=ax)      
        st.pyplot(fig)




# Página Fundamentos________________________________________________________________________
def fundamentos():
    st.title('Dados Fundamentalistas')

    lista_tickers = fd.list_papel_all()
    #st.write(lista_tickers)

    comparar = st.checkbox('Comparar 2 ativos')
    col1, col2 = st.columns(2)

    with col1:
        with st.expander('Ativo 1', expanded=True):
            papel1 = st.selectbox('Selecione o Papel', lista_tickers)
            info_papel1 = fd.get_detalhes_papel(papel1)
            st.write('**Empresa:**', info_papel1['Empresa'][0])
            st.write('**Setor:**', info_papel1['Setor'][0])
            st.write('**Subsetor:**', info_papel1['Subsetor'][0])
            st.write('**Valor de Mercado:**',f"R$ {float(info_papel1['Valor_de_mercado'][0]):,.2f}")
            st.write('**Patrimônio Líquido:**', f"R$ {float(info_papel1['Patrim_Liq'][0]):,.2f}")
            st.write('**Receita Liq. 12m:**', f"R$ {float(info_papel1['Receita_Liquida_12m'][0]):,.2f}")
            st.write('**Dívida Bruta:**', f"R$ {float(info_papel1['Div_Bruta'][0]):,.2f}")
            st.write('**Dívida Líquida:**', f"R$ {float(info_papel1['Div_Liquida'][0]):,.2f}")
            st.write('**P/L:**', f"{float(info_papel1['PL'][0]) / 100:,.2f}")
            st.write('**Dividend Yield:**', f"{info_papel1['Div_Yield'][0]}")

    if comparar:
        with col2:
            with st.expander('Ativo 2', expanded=True):
                papel2 = st.selectbox('Selecione o 2º Papel', lista_tickers)
                info_papel2 = fd.get_detalhes_papel(papel2)
                st.write('**Empresa:**', info_papel2['Empresa'][0])
                st.write('**Setor:**', info_papel2['Setor'][0])
                st.write('**Subsetor:**', info_papel2['Subsetor'][0])
                st.write('**Valor de Mercado:**',f"R$ {float(info_papel2['Valor_de_mercado'][0]):,.2f}")
                st.write('**Patrimônio Líquido:**', f"R$ {float(info_papel2['Patrim_Liq'][0]):,.2f}")
                st.write('**Receita Liq. 12m:**', f"R$ {float(info_papel2['Receita_Liquida_12m'][0]):,.2f}")
                st.write('**Dívida Bruta:**', f"R$ {float(info_papel2['Div_Bruta'][0]):,.2f}")
                st.write('**Dívida Líquida:**', f"R$ {float(info_papel2['Div_Liquida'][0]):,.2f}")

                st.write('**P/L:**', f"{float(info_papel2['PL'][0]) / 100:,.2f}")

                st.write('**Dividend Yield:**', f"{info_papel2['Div_Yield'][0]}")

#___________________________________________________________________________________________
def main():

    st.sidebar.image('grafico_logo.png',width=150)

    st.sidebar.title('App Financeiro')
    #st.markdown('---')

    lista_menu = ['Home','Calendário Econômico', 'Panorama do Mercado','Rentabilidade Mensais','Fundamentos']
    
    escolha = st.sidebar.radio('Escolha a opção', lista_menu)
    if escolha == 'Home':
        home()
    if escolha == 'Calendário Econômico':
        calendario()
    if escolha == 'Panorama do Mercado':
        panorama()
    if escolha == 'Rentabilidade Mensais':
        mapa_mensal()
    if escolha == 'Fundamentos':
        fundamentos()        

main() 
