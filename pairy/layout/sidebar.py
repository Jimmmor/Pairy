import streamlit as st
from layout.sidebar import sidebar_ui
from logic.data_loader import load_and_process_data
from logic.signals import calculate_signals
from stats.metrics import compute_metrics
from visualizations.plots import (
    plot_spread_signal,
    plot_prices,
    plot_zscore,
    plot_rolling_corr,
    plot_returns_scatter,
    plot_correlation_boxplot,
)

# Pagina-instellingen
st.set_page_config(layout="wide")
st.title("📈 Pairs Trading Monitor")

# Sidebar UI: laat gebruiker keuzes maken en return parameters
params = sidebar_ui()

# Data ophalen en verwerken
data1, data2 = load_and_process_data(
    params['name1'], params['name2'], params['periode'], params['interval']
)

if data1.empty or data2.empty:
    st.error("Geen data beschikbaar voor één of beide coins. Probeer een andere combinatie of periode.")
    st.stop()

# Signalen berekenen
df = calculate_signals(data1, data2, params)

# Statistieken berekenen
metrics = compute_metrics(df)

# Resultaten tonen
st.subheader("🚦 Huidige trade signaal")
st.write(f"**Z-score laatste waarde:** {df['zscore'].iloc[-1]:.2f}")
st.write(f"**Signaal:** {metrics['current_position']}")

# Grafieken weergeven
plot_spread_signal(df, params)
plot_prices(df, params)
plot_zscore(df, params)
plot_rolling_corr(df)
plot_returns_scatter(df, params)
plot_correlation_boxplot(df)

# Statistische metrics tonen
st.subheader("📈 Correlatie Statistieken")
st.metric("Pearson Correlatie", f"{metrics['pearson_corr']:.4f}")
st.metric("Beta (β)", f"{metrics['beta']:.4f}")
st.metric("R-squared", f"{metrics['r_squared']:.4f}")

st.subheader("🎯 Correlatie Beoordeling")
st.write(f"**Correlatie beoordeling:** {metrics['corr_assessment']}")
st.write(f"**R-squared beoordeling:** {metrics['r2_assessment']}")
st.write(f"**Stabiliteit beoordeling:** {metrics['stability_assessment']}")

# Export mogelijkheid
if st.button("Exporteer analyse naar CSV"):
    csv = df.to_csv(index=True)
    st.download_button(label="Download CSV", data=csv, file_name="pairs_trading_analysis.csv", mime='text/csv')
