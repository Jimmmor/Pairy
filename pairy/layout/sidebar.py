# layout/sidebar.py
import streamlit as st
from constants.tickers import tickers

def configure_sidebar():
    st.sidebar.header("🔍 Kies een Coin Pair")
    name1 = st.sidebar.selectbox("Coin 1", list(tickers.keys()))
    name2 = st.sidebar.selectbox("Coin 2", [k for k in tickers if k != name1])
    
    st.sidebar.markdown("---")
    periode = st.sidebar.selectbox("Periode", ["1mo", "3mo", "6mo", "1y"], index=2)
    interval = st.sidebar.selectbox("Interval", ["1d"] if periode in ["6mo", "1y"] else ["1d", "1h", "30m"])
    corr_window = st.sidebar.slider("Rolling correlatie window (dagen)", 5, 60, 20)

    st.sidebar.markdown("---")
    z_in = st.sidebar.slider("Z-score entry threshold", 1.0, 5.0, 2.0, step=0.1)
    z_out = st.sidebar.slider("Z-score exit threshold", 0.0, 2.0, 0.5, step=0.1)

    return {
        'name1': name1,
        'name2': name2,
        'ticker1': tickers[name1],
        'ticker2': tickers[name2],
        'periode': periode,
        'interval': interval,
        'corr_window': corr_window,
        'z_entry': z_in,
        'z_exit': z_out
    }
