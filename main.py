import streamlit as st
from pathlib import Path
import sys
from constants.tickers import tickers
from pages.sidebar import show as sidebar_ui
from utils.data_loader import load_data, preprocess_data
from pages.analysis import show as show_analysis
from pages.backtesting import show as show_backtest

# Configuratie
def setup():
    """Initialiseer applicatie-instellingen"""
    # Pad configuratie
    sys.path.append(str(Path(__file__).parent.parent))
    
    # Cache leegmaken
    st.cache_data.clear()
    
    # Pagina config
    st.set_page_config(
        layout="wide",
        page_title="Pairs Trading Monitor",
        page_icon="📈"
    )

def load_and_prepare_data(params):
    """Garandeer dat alle benodigde kolommen aanwezig zijn"""
    try:
        # Data laden
        data1 = load_data(params['coin1'], params['period'], params['interval'])
        data2 = load_data(params['coin2'], params['period'], params['interval'])
        
        if data1.empty or data2.empty:
            st.error("Ontbrekende data voor één of beide assets")
            st.stop()
            
        # Data verwerken (inclusief z-score berekening)
        df = preprocess_data(data1, data2)
        
        # Controleer kritieke kolommen
        required_columns = ['price1', 'price2', 'spread', 'zscore']
        if not all(col in df.columns for col in required_columns):
            missing = [col for col in required_columns if col not in df.columns]
            st.error(f"Ontbrekende kolommen in data: {', '.join(missing)}")
            st.stop()
            
        return df
        
    except Exception as e:
        st.error(f"Data voorbereidingsfout: {str(e)}")
        st.stop()

def main():
    """Hoofdapplicatie"""
    setup()
    st.title("📈 Pairs Trading Monitor")
    
    try:
        # Laad sidebar en parameters
        params = sidebar_ui(tickers)
        
        # Data pipeline
        df = load_and_prepare_data(params)
        
        # Verpak data en parameters voor analyse
        analysis_data = {
            'df': df,
            'params': params
        }
        
        # Toon analyse
        show_analysis(analysis_data)
        
        # Optionele backtest
        if params.get('run_backtest', False):
            with st.spinner("Backtest uitvoeren..."):
                backtest_results = show_backtest(analysis_data)
                if backtest_results:
                    st.success("Backtest voltooid!")
                    
    except Exception as e:
        st.error(f"Er is een onverwachte fout opgetreden: {str(e)}")
        st.stop()
if __name__ == "__main__":
    main()
