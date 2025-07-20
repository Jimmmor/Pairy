import streamlit as st
from pathlib import Path
import os
import sys
from constants.tickers import tickers

# Voeg project root toe aan Python path
sys.path.append(str(Path(__file__).parent.parent))

# Clear cache bij opstarten
st.cache_data.clear()

# Importeer vanuit de juiste locaties
from pages.sidebar import show as sidebar_ui
from utils.data_loader import load_data, preprocess_data
from pages.analysis import show as show_analysis
from pages.backtesting import show as show_backtest

# Pagina-instellingen
st.set_page_config(layout="wide")
st.title("📈 Pairs Trading Monitor")

def main():
    # Sidebar UI
    sidebar_params = sidebar_ui(tickers)
    
    # Data ophalen
    data1 = load_data(sidebar_params['coin1'], sidebar_params['periode'], sidebar_params['interval'])
    data2 = load_data(sidebar_params['coin2'], sidebar_params['periode'], sidebar_params['interval'])
    
    if data1.empty or data2.empty:
        st.error("Geen data beschikbaar voor één of beide coins. Probeer een andere combinatie of periode.")
        st.stop()
    
    # Data verwerken
    df = preprocess_data(data1, data2)
    
    # Toon analyse
    show_analysis(df, sidebar_params)
    
    # Voer backtest uit en toon resultaten
    if 'run_backtest' in sidebar_params and sidebar_params['run_backtest']:
        df_backtest, trades = show_backtest(df, sidebar_params)
        if trades:
            show_backtest(df_backtest, trades)

if __name__ == "__main__":
    main()
