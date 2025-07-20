import yfinance as yf
import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression

@st.cache_data(ttl=3600)
def load_data(ticker, period, interval):
    """Laad data van Yahoo Finance met caching"""
    try:
        data = yf.download(ticker, period=period, interval=interval)
        return data[['Close']].rename(columns={'Close': 'price'})
    except Exception as e:
        st.error(f"Fout bij laden {ticker}: {str(e)}")
        return pd.DataFrame()

def preprocess_data(data1, data2):
    """Combineer twee datasets op datum"""
    try:
        df = pd.concat([
            data1.rename(columns={'price': 'price1'}),
            data2.rename(columns={'price': 'price2'})
        ], axis=1).dropna()
        return df
    except Exception as e:
        st.error(f"Fout bij verwerken data: {str(e)}")
        return pd.DataFrame()
