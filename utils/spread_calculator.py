import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import streamlit as st

def calculate_spread(df):
    """Bereken spread en trading signalen"""
    try:
        # Linear regression model
        X = df['price1'].values.reshape(-1, 1)
        y = df['price2'].values
        model = LinearRegression().fit(X, y)
        
        # Bereken spread en z-score
        df['spread'] = df['price2'] - (model.intercept_ + model.coef_[0] * df['price1'])
        df['zscore'] = (df['spread'] - df['spread'].mean()) / df['spread'].std()
        
        return df, {
            'alpha': model.intercept_,
            'beta': model.coef_[0],
            'r_squared': model.score(X, y)
        }
    except Exception as e:
        st.error(f"Spread berekeningsfout: {str(e)}")
        return df, {}
