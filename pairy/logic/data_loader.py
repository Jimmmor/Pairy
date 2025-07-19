# logic/data_loader.py
import yfinance as yf
import pandas as pd
import streamlit as st

@st.cache_data
def fetch_data(ticker, period, interval):
    df = yf.download(ticker, period=period, interval=interval)
    return df['Close'] if 'Close' in df else df.iloc[:, 0]

def load_and_process_data(params):
    d1 = fetch_data(params['ticker1'], params['periode'], params['interval'])
    d2 = fetch_data(params['ticker2'], params['periode'], params['interval'])
    
    df = pd.DataFrame({'price1': d1, 'price2': d2}).dropna()
    df = df.align(df, join='inner')[0]
    
    return df, {'start': df.index.min(), 'end': df.index.max()}
