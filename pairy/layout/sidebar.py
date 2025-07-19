import streamlit as st
from constants.tickers import tickers

def sidebar_ui():
    st.sidebar.header("🔍 Kies een Coin Pair")
    name1 = st.sidebar.selectbox("Coin 1", list(tickers.keys()), index=0)
    remaining = [k for k in tickers.keys() if k != name1]
    name2 = st.sidebar.selectbox("Coin 2", remaining, index=0)
    
    st.sidebar.markdown("---")
    periode = st.sidebar.selectbox("Periode", ["1mo", "3mo", "6mo", "1y"], index=2)
    interval_options = ["1d"] if periode in ["6mo", "1y"] else ["1d", "1h", "30m"]
    interval = st.sidebar.selectbox("Interval", interval_options, index=0)
    corr_window = st.sidebar.slider("Rolling correlatie window (dagen)", min_value=5, max_value=60, value=20, step=1)
    
    st.sidebar.markdown("---")
    zscore_entry_threshold = st.sidebar.slider("Z-score entry threshold", min_value=1.0, max_value=5.0, value=2.0, step=0.1)
    zscore_exit_threshold = st.sidebar.slider("Z-score exit threshold", min_value=0.0, max_value=2.0, value=0.5, step=0.1)
    
    return {
        "name1": name1,
        "name2": name2,
        "periode": periode,
        "interval": interval,
        "corr_window": corr_window,
        "zscore_entry_threshold": zscore_entry_threshold,
        "zscore_exit_threshold": zscore_exit_threshold
    }
