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
    """Combineer data en bereken statistieken"""
    try:
        # Combineer data
        df = pd.concat([
            data1['Close'].rename('price1'),
            data2['Close'].rename('price2')
        ], axis=1).dropna()
        
        if df.empty:
            st.error("Geen overlappende data tussen de assets")
            return pd.DataFrame()
        
        # Bereken spread en z-scores
        X = df['price1'].values.reshape(-1, 1)
        y = df['price2'].values
        
        model = LinearRegression().fit(X, y)
        df['spread'] = df['price2'] - (model.intercept_ + model.coef_[0] * df['price1'])
        df['zscore'] = (df['spread'] - df['spread'].mean()) / df['spread'].std()
        
        return df
        
    except Exception as e:
        st.error(f"Data verwerkingsfout: {str(e)}")
        return pd.DataFrame()
