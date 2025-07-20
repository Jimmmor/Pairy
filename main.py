import streamlit as st
from constants.tickers import tickers
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.sidebar import show as sidebar_ui
from pages.analysis import show
from pages.backtesting import show as show_backtest
from logic.data_loader import load_data
from logic.signals import calculate_signals
from stats.metrics import compute_metrics
from visualizations.plots import (
    plot_spread_signal,
    plot_prices,
    plot_zscore,
    plot_rolling_correlation,
    plot_returns_scatter,
    plot_correlation_boxplot,
)

# Zorg dat Python de modules kan vinden
sys.path.append(str(Path(__file__).parent))

# Clear cache bij opstarten
import streamlit as st
st.cache_data.clear()
# Pagina-instellingen
st.set_page_config(layout="wide")
st.title("📈 Pairs Trading Monitor")

# Sidebar UI: laat gebruiker keuzes maken en return parameters
params = sidebar_ui(tickers)

# Data ophalen
data1 = load_data(params['coin1'], params['periode'], params['interval'])
data2 = load_data(params['coin2'], params['periode'], params['interval'])

if data1.empty or data2.empty:
    st.error("Geen data beschikbaar voor één of beide coins. Probeer een andere combinatie of periode.")
    st.stop()

# Data voorbereiden en signalen berekenen
df = calculate_signals(data1, data2, params)

# Metrics berekenen
metrics = compute_metrics(df)

# Resultaten tonen in Streamlit
st.subheader("🚦 Huidige trade signaal")
st.write(f"**Z-score laatste waarde:** {df['zscore'].iloc[-1]:.2f}")
st.write(f"**Signaal:** {metrics['current_position']}")

# Grafieken
plot_spread_signal(df, params)
plot_prices(df, params)
plot_zscore(df, params)
plot_rolling_correlation(df)
plot_returns_scatter(df, params)
plot_correlation_boxplot(df)

# Metrics tabel tonen
st.subheader("📈 Correlatie Statistieken")
st.metric("Pearson Correlatie", f"{metrics['pearson_corr']:.4f}")
st.metric("Beta (β)", f"{metrics['beta']:.4f}")
st.metric("R-squared", f"{metrics['r_squared']:.4f}")
# (etc, voeg meer metrics toe zoals in je oorspronkelijke script)

# Correlatie beoordeling
st.subheader("🎯 Correlatie Beoordeling")
st.write(f"**Correlatie beoordeling:** {metrics['corr_assessment']}")
st.write(f"**R-squared beoordeling:** {metrics['r2_assessment']}")
st.write(f"**Stabiliteit beoordeling:** {metrics['stability_assessment']}")

# Export optie
if st.button("Exporteer analyse naar CSV"):
    csv = df.to_csv(index=True)
    st.download_button(label="Download CSV", data=csv, file_name="pairs_trading_analysis.csv", mime='text/csv')
