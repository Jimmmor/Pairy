import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def linear_regression_spread(price1: pd.Series, price2: pd.Series):
    """
    Bereken alpha, beta en R² van lineaire regressie price2 ~ price1.
    """
    X = price1.values.reshape(-1, 1)
    y = price2.values
    model = LinearRegression()
    model.fit(X, y)
    alpha = model.intercept_
    beta = model.coef_[0]
    r_squared = model.score(X, y)
    return alpha, beta, r_squared

def calculate_spread(price1: pd.Series, price2: pd.Series, alpha: float, beta: float):
    """
    Bereken de spread op basis van regressie parameters.
    """
    spread = price2 - (alpha + beta * price1)
    return spread

def calculate_zscore(spread: pd.Series):
    """
    Bereken z-score van de spread.
    """
    mean = spread.mean()
    std = spread.std()
    zscore = (spread - mean) / std
    return zscore, mean, std

def rolling_correlation(price1: pd.Series, price2: pd.Series, window: int):
    """
    Bereken rolling correlatie over window dagen.
    """
    return price1.rolling(window=window).corr(price2)

def generate_trade_signals(zscore: pd.Series, entry_threshold: float, exit_threshold: float):
    """
    Genereer long, short en exit signalen op basis van z-score thresholds.
    """
    long_entry = zscore < -entry_threshold
    short_entry = zscore > entry_threshold
    exit = zscore.abs() < exit_threshold
    return long_entry, short_entry, exit

def compute_metrics(price1: pd.Series, price2: pd.Series, entry_threshold=2.0, exit_threshold=0.5, window=20):
    """
    Voert alle berekeningen uit en geeft een dict met de resultaten.
    """
    alpha, beta, r2 = linear_regression_spread(price1, price2)
    spread = calculate_spread(price1, price2, alpha, beta)
    zscore, mean, std = calculate_zscore(spread)
    corr = rolling_correlation(price1, price2, window)
    long_entry, short_entry, exit = generate_trade_signals(zscore, entry_threshold, exit_threshold)
    return {
        "alpha": alpha,
        "beta": beta,
        "r_squared": r2,
        "spread": spread,
        "zscore": zscore,
        "mean_spread": mean,
        "std_spread": std,
        "rolling_corr": corr,
        "long_entry": long_entry,
        "short_entry": short_entry,
        "exit": exit,
    }
