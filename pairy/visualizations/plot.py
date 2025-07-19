# plots.py
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression

def plot_price(df, name1, name2):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['price1'], name=name1, line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=df['price2'], name=name2, line=dict(color='red'), yaxis='y2'))
    fig.update_layout(
        title="Prijsverloop",
        xaxis_title="Datum",
        yaxis_title=f"{name1} Prijs (USD)",
        yaxis2=dict(title=f"{name2} Prijs (USD)", overlaying='y', side='right'),
        template='plotly_dark'
    )
    return fig

def plot_zscore(df, zscore_entry_threshold, zscore_exit_threshold):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['zscore'], name='Z-score', line=dict(color='purple')))
    fig.add_hline(y=zscore_entry_threshold, line=dict(color='red', dash='dash'), annotation_text='Entry Threshold')
    fig.add_hline(y=-zscore_entry_threshold, line=dict(color='green', dash='dash'), annotation_text='Entry Threshold')
    fig.add_hline(y=zscore_exit_threshold, line=dict(color='blue', dash='dot'), annotation_text='Exit Threshold')
    fig.add_hline(y=-zscore_exit_threshold, line=dict(color='blue', dash='dot'), annotation_text='Exit Threshold')
    fig.update_layout(title="Z-score", yaxis_title="Z-score", xaxis_title="Datum", template='plotly_dark')
    return fig

def plot_rolling_corr(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=df['rolling_corr'],
        fill='tozeroy',
        fillcolor='rgba(0, 255, 0, 0.3)',  # Groen transparant
        line=dict(color='orange', width=2),
        name='Rolling Correlatie'
    ))
    fig.update_layout(
        title="Rolling Correlatie met Transparant Oppervlak",
        yaxis_title="Correlatie",
        xaxis_title="Datum",
        yaxis=dict(range=[-1, 1]),
        template='plotly_dark'
    )
    return fig

def plot_returns_scatter(df, name1, name2):
    returns_clean = df[['returns1', 'returns2']].dropna()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=returns_clean['returns1'] * 100,
        y=returns_clean['returns2'] * 100,
        mode='markers',
        marker=dict(color='purple', size=8, opacity=0.6),
        name='Daily Returns',
        showlegend=False
    ))
    X_scatter = returns_clean['returns1'].values.reshape(-1, 1)
    y_scatter = returns_clean['returns2'].values
    model_scatter = LinearRegression()
    model_scatter.fit(X_scatter, y_scatter)
    x_line = np.linspace(returns_clean['returns1'].min(), returns_clean['returns1'].max(), 100)
    y_line = model_scatter.predict(x_line.reshape(-1, 1))
    fig.add_trace(go.Scatter(
        x=x_line * 100,
        y=y_line * 100,
        mode='lines',
        line=dict(color='yellow', width=3),
        name=f'y = {model_scatter.coef_[0]:.3f}x + {model_scatter.intercept_:.3f}',
        showlegend=False
    ))
    fig.add_annotation(
        x=0.05, y=0.95,
        xref='paper', yref='paper',
        text=f'y = {model_scatter.coef_[0]:.3f}x + {model_scatter.intercept_:.6f}',
        showarrow=False,
        font=dict(size=12, color='yellow'),
        bgcolor='rgba(0,0,0,0.5)',
        bordercolor='yellow',
        borderwidth=1
    )
    fig.update_layout(
        title="Returns Correlatie Scatter Plot",
        xaxis_title=f"{name1} Returns (%)",
        yaxis_title=f"{name2} Returns (%)",
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white')
    )
    return fig
def plot_spread_signal(df, params):
    import streamlit as st
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['spread'], name='Spread', line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=df.index, y=df['entry_upper'], name='Upper Threshold', line=dict(color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=df.index, y=df['entry_lower'], name='Lower Threshold', line=dict(color='green', dash='dash')))
    fig.add_trace(go.Scatter(x=df.index, y=df['exit'], name='Exit Threshold', line=dict(color='blue', dash='dot')))
    fig.update_layout(title="Spread & Trade Signal", xaxis_title="Datum", yaxis_title="Spread", template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

def plot_prices(df, params):
    import streamlit as st
    fig = plot_price(df, params['coin1'], params['coin2'])
    st.plotly_chart(fig, use_container_width=True)

def plot_zscore(df, params):
    import streamlit as st
    fig = plot_zscore(df, params['zscore_entry'], params['zscore_exit'])
    st.plotly_chart(fig, use_container_width=True)

def plot_rolling_correlation(df):
    import streamlit as st
    fig = plot_rolling_corr(df)
    st.plotly_chart(fig, use_container_width=True)

def plot_returns_scatter(df, params):
    import streamlit as st
    fig = plot_returns_scatter(df, params['coin1'], params['coin2'])
    st.plotly_chart(fig, use_container_width=True)

def plot_correlation_boxplot(df):
    import streamlit as st
    fig = go.Figure()
    fig.add_trace(go.Box(y=df['rolling_corr'], name='Rolling Correlatie', boxpoints='all', jitter=0.5, whiskerwidth=0.2, marker_color='cyan'))
    fig.update_layout(title="Boxplot van Rolling Correlatie", yaxis_title="Correlatie", template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)
