from requests.api import options
import streamlit as st
import pandas as pd 
import yfinance as yf 
import datetime
import numpy as np 
from pandas_datareader import data as pdr
import cufflinks as cf
from pathlib import Path 

def main():
    # App title
    st.markdown('''
    # Cryptos & Stocks  📈
   
    ''')
    st.write('------')

    # App sidebar
    st.sidebar.subheader('Parameters')
    start_date= st.sidebar.date_input('Start date', datetime.date(2020,1,1))
    end_date= st.sidebar.date_input('End date', datetime.date.today())

    # Retrieving tickers data
    ticker_str= 'BTC-USD', 'ETH-USD', 'DOGE-USD', 'AAPL', 'SPYG', 'SPYD'
    yf_df = yf.download(ticker_str, group_by='Ticker', start= start_date, end= end_date)
    yf_df = yf_df.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index(level=1)

    # select the ticker to display
    ticker_selected= st.selectbox('Select a ticker', options= ticker_str)
    s_data= yf_df[yf_df['Ticker']==ticker_selected]
    st.write(s_data.describe())

    # text for key take away
    bbs= Path('BollingerBands.md').read_text()


    # Bollinger bands
    st.info('Bollinger Bands®')
    st.write('Key Take Away')
    st.markdown(bbs, unsafe_allow_html= True)

    qf= cf.QuantFig(s_data, title= 'Bollinger bands', legend= 'top', name= 'GS')
    qf.add_bollinger_bands()
    fig= qf.iplot(asFigure= True)
    st.plotly_chart(fig)


if __name__ =='__main__':
    main()
    