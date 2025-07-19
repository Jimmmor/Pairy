# logic/signals.py
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def calculate_signals(df, params):
    X = df['price1'].values.reshape(-1, 1)
    y = df['price2'].values
    model = LinearRegression().fit(X, y)

    df['spread'] = y - model.predict(X)
    spread_mean = df['spread'].mean()
    spread_std = df['spread'].std()
    df['zscore'] = (df['spread'] - spread_mean) / spread_std
    df['rolling_corr'] = df['price1'].rolling(window=params['corr_window']).corr(df['price2'])

    df['long_entry'] = df['zscore'] < -params['z_entry']
    df['short_entry'] = df['zscore'] > params['z_entry']
    df['exit'] = df['zscore'].abs() < params['z_exit']

    last = df.iloc[-1]
    signal = (
        f"Long Spread (koop {params['name2']}, verkoop {params['name1']})"
        if last['long_entry'] else
        f"Short Spread (verkoop {params['name2']}, koop {params['name1']})"
        if last['short_entry'] else
        "Exit positie (geen trade)" if last['exit'] else
        "Geen duidelijk signaal"
    )

    return df, {'signal': signal, 'zscore': last['zscore']}
