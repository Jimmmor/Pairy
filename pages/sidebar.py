import streamlit as st
from constants.tickers import tickers

def show(tickers_dict):
    """
    Toon de sidebar en retourneer alle trading parameters
    
    Args:
        tickers_dict (dict): Dictionary met coin namen en ticker symbols
        
    Returns:
        dict: Dictionary met alle geselecteerde parameters
    """
    params = {}
    
    with st.sidebar:
        # Coin selectie sectie
        st.header("🔍 Kies een Coin Pair")
        params['name1'] = st.selectbox(
            "Coin 1", 
            list(tickers_dict.keys()), 
            index=0,
            key='sb_coin1'
        )
        remaining = [k for k in tickers_dict.keys() if k != params['name1']]
        params['name2'] = st.selectbox(
            "Coin 2", 
            remaining, 
            index=0,
            key='sb_coin2'
        )
        
        # Data instellingen sectie
        st.markdown("---")
        st.header("📊 Data Instellingen")
        params['period'] = st.selectbox(
            "Periode", 
            ["1mo", "3mo", "6mo", "1y", "2y"], 
            index=2,
            key='sb_period'
        )
        params['interval'] = st.selectbox(
            "Interval", 
            ["1d"] if params['period'] in ["6mo", "1y", "2y"] else ["1d", "1h", "30m"],
            key='sb_interval'
        )
        params['corr_window'] = st.slider(
            "Rolling correlatie window (dagen)", 
            min_value=5, 
            max_value=60, 
            value=20,
            step=1,
            key='sb_corr_window'
        )

        # Trading parameters sectie
        st.markdown("---")
        st.header("⚙️ Trading Parameters")
        params['zscore_entry'] = st.slider(
            "Z-score entry threshold", 
            min_value=1.0, 
            max_value=5.0, 
            value=2.0, 
            step=0.1,
            key='sb_zscore_entry'
        )
        params['zscore_exit'] = st.slider(
            "Z-score exit threshold", 
            min_value=0.0, 
            max_value=2.0, 
            value=0.5, 
            step=0.1,
            key='sb_zscore_exit'
        )

        # Backtesting sectie
        st.markdown("---")
        st.header("🎯 Backtesting Instellingen")
        params['initial_capital'] = st.number_input(
            "Startkapitaal (USD)", 
            min_value=1000, 
            max_value=1000000, 
            value=10000, 
            step=1000,
            key='sb_initial_capital'
        )
        params['transaction_cost'] = st.slider(
            "Transactiekosten (%)", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.1, 
            step=0.01,
            key='sb_transaction_cost'
        )
        params['max_position'] = st.slider(
            "Max positie grootte (% van kapitaal)", 
            min_value=10, 
            max_value=100, 
            value=50, 
            step=10,
            key='sb_max_position'
        )

        # Risk management sectie
        st.markdown("---")
        st.subheader("🛡️ Risk Management")
        params['stop_loss'] = st.slider(
            "Stop Loss (%)", 
            min_value=0.0, 
            max_value=20.0, 
            value=5.0, 
            step=0.5,
            key='sb_stop_loss'
        )
        params['take_profit'] = st.slider(
            "Take Profit (%)", 
            min_value=0.0, 
            max_value=50.0, 
            value=10.0, 
            step=1.0,
            key='sb_take_profit'
        )

        # Info sectie
        st.markdown("---")
        st.header("ℹ️ Info")
        st.info("""
            **Pairs Trading Strategie**:  
            - **Long spread**: Z-score < -entry threshold  
            - **Short spread**: Z-score > entry threshold  
            - **Exit**: |z-score| < exit threshold  
        """)
    
    # Voeg ticker symbols toe aan parameters
    params['coin1'] = tickers_dict[params['name1']]
    params['coin2'] = tickers_dict[params['name2']]
    
    # Sla ook op in session state voor persistentie
    for key, value in params.items():
        st.session_state[key] = value
    
    return params
