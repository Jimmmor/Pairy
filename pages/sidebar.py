import streamlit as st
from constants.tickers import tickers

def show(tickers):
    """Toon de sidebar met alle configuratie-opties"""
    with st.sidebar:
        # Coin selectie
        st.header("🔍 Kies een Coin Pair")
        name1 = st.selectbox("Coin 1", list(tickers.keys()), index=0)
        remaining = [k for k in tickers.keys() if k != name1]
        name2 = st.selectbox("Coin 2", remaining, index=0)
        
        # Sla selecties op in session state
        st.session_state['name1'] = name1
        st.session_state['name2'] = name2
        st.session_state['coin1'] = tickers[name1]
        st.session_state['coin2'] = tickers[name2]
        
        # Data instellingen
        st.markdown("---")
        st.header("📊 Data Instellingen")
        periode = st.selectbox("Periode", ["1mo", "3mo", "6mo", "1y", "2y"], index=2)
        interval_options = ["1d"] if periode in ["6mo", "1y", "2y"] else ["1d", "1h", "30m"]
        interval = st.selectbox("Interval", interval_options, index=0)
        corr_window = st.slider(
            "Rolling correlatie window (dagen)", 
            min_value=5, 
            max_value=60, 
            value=20, 
            step=1
        )
        
        # Sla data instellingen op
        st.session_state['periode'] = periode
        st.session_state['interval'] = interval
        st.session_state['corr_window'] = corr_window
        
        # Trading parameters
        st.markdown("---")
        st.header("⚙️ Trading Parameters")
        zscore_entry_threshold = st.slider(
            "Z-score entry threshold", 
            min_value=1.0, 
            max_value=5.0, 
            value=2.0, 
            step=0.1
        )
        zscore_exit_threshold = st.slider(
            "Z-score exit threshold", 
            min_value=0.0, 
            max_value=2.0, 
            value=0.5, 
            step=0.1
        )
        
        # Sla trading parameters op
        st.session_state['zscore_entry_threshold'] = zscore_entry_threshold
        st.session_state['zscore_exit_threshold'] = zscore_exit_threshold
        
        # Backtesting instellingen
        st.markdown("---")
        st.header("🎯 Backtesting Instellingen")
        initial_capital = st.number_input(
            "Startkapitaal (USD)", 
            min_value=1000, 
            max_value=1000000, 
            value=10000, 
            step=1000
        )
        transaction_cost = st.slider(
            "Transactiekosten (%)", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.1, 
            step=0.01
        )
        max_position_size = st.slider(
            "Max positie grootte (% van kapitaal)", 
            min_value=10, 
            max_value=100, 
            value=50, 
            step=10
        )
        
        # Sla backtest instellingen op
        st.session_state['initial_capital'] = initial_capital
        st.session_state['transaction_cost'] = transaction_cost
        st.session_state['max_position_size'] = max_position_size
        
        # Risk management
        st.markdown("---")
        st.subheader("🛡️ Risk Management")
        stop_loss_pct = st.slider(
            "Stop Loss (%)", 
            min_value=0.0, 
            max_value=20.0, 
            value=5.0, 
            step=0.5
        )
        take_profit_pct = st.slider(
            "Take Profit (%)", 
            min_value=0.0, 
            max_value=50.0, 
            value=10.0, 
            step=1.0
        )
        
        # Sla risk parameters op
        st.session_state['stop_loss_pct'] = stop_loss_pct
        st.session_state['take_profit_pct'] = take_profit_pct
        
        # Info sectie
        st.markdown("---")
        st.header("ℹ️ Info")
        st.info("""
            **Pairs Trading Strategie**:  
            Deze app implementeert een statistische arbitrage strategie op basis van z-scores.  
            - **Long spread**: Wanneer z-score < -entry threshold  
            - **Short spread**: Wanneer z-score > entry threshold  
            - **Exit**: Wanneer |z-score| < exit threshold  
        """)