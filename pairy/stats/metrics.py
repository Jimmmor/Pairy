# Lineaire regressie voor spread berekening
X = df['price1'].values.reshape(-1, 1)
y = df['price2'].values

model = LinearRegression()
model.fit(X, y)

alpha = model.intercept_
beta = model.coef_[0]
r_squared = model.score(X, y)

# Spread berekenen
df['spread'] = df['price2'] - (alpha + beta * df['price1'])

# Spread statistieken
spread_mean = df['spread'].mean()
spread_std = df['spread'].std()

# Z-score berekenen
df['zscore'] = (df['spread'] - spread_mean) / spread_std

# Rolling correlatie
df['rolling_corr'] = df['price1'].rolling(window=corr_window).corr(df['price2'])

# Pearson correlatie
pearson_corr = df['price1'].corr(df['price2'])

# Trade signalen gebaseerd op z-score thresholds
df['long_entry'] = df['zscore'] < -zscore_entry_threshold
df['short_entry'] = df['zscore'] > zscore_entry_threshold
df['exit'] = df['zscore'].abs() < zscore_exit_threshold

# Huidige positie bepalen (laatste data punt)
if df['long_entry'].iloc[-1]:
    current_position = f"Long Spread (koop {name2}, verkoop {name1})"
elif df['short_entry'].iloc[-1]:
    current_position = f"Short Spread (verkoop {name2}, koop {name1})"
elif df['exit'].iloc[-1]:
    current_position = "Exit positie (geen trade)"
else:
    current_position = "Geen duidelijk signaal"

# Correlatie statistieken tabel
st.subheader("📈 Correlatie Statistieken")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Pearson Correlatie", f"{pearson_corr:.4f}")
    st.metric("Beta (β)", f"{beta:.4f}")
    st.metric("R-squared", f"{r_squared:.4f}")

with col2:
    current_rolling_corr = df['rolling_corr'].iloc[-1]
    avg_rolling_corr = df['rolling_corr'].mean()
    st.metric("Huidige Rolling Correlatie", f"{current_rolling_corr:.4f}")
    st.metric("Gemiddelde Rolling Correlatie", f"{avg_rolling_corr:.4f}")
    st.metric("Alpha (α)", f"{alpha:.6f}")

with col3:
    returns_corr = returns_clean['returns1'].corr(returns_clean['returns2'])
    volatility_ratio = returns_clean['returns2'].std() / returns_clean['returns1'].std()
    st.metric("Returns Correlatie", f"{returns_corr:.4f}")
    st.metric("Volatiliteit Ratio", f"{volatility_ratio:.4f}")
    st.metric("Std Error (β)", f"{np.sqrt(np.mean((df['price2'] - (alpha + beta * df['price1']))**2)):.4f}")
