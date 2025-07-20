import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def show(df):
    """Toon de huidige analyse sectie"""
    st.header("📊 Huidige Analyse")
    
    # Huidige signaal
    show_current_signal(df)
    
    # Toon grafieken
    show_spread_chart(df)
    show_price_and_zscore_charts(df)
    show_correlation_stats(df)
    
    # Export functionaliteit
    show_export_options(df)

def show_current_signal(df):
    """Toon het huidige trading signaal"""
    st.subheader("🚦 Huidige Trade Signaal")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Laatste Z-score", f"{df['zscore'].iloc[-1]:.2f}")
        
    with col2:
        current_position = get_current_position(df)
        st.metric("Huidig Signaal", current_position)
        
    st.write(f"**Verklaring:** {get_signal_explanation(current_position)}")

def get_current_position(df):
    """Bepaal het huidige trading signaal"""
    if df['long_entry'].iloc[-1]:
        return f"Long Spread (koop {st.session_state.name2}, verkoop {st.session_state.name1})"
    elif df['short_entry'].iloc[-1]:
        return f"Short Spread (verkoop {st.session_state.name2}, koop {st.session_state.name1})"
    elif df['exit'].iloc[-1]:
        return "Exit positie (geen trade)"
    return "Geen duidelijk signaal"

def get_signal_explanation(position):
    """Geef een uitleg bij het huidige signaal"""
    if "Long Spread" in position:
        return "De spread is significant laag en wordt verwacht te stijgen naar het gemiddelde."
    elif "Short Spread" in position:
        return "De spread is significant hoog en wordt verwacht te dalen naar het gemiddelde."
    elif "Exit" in position:
        return "De spread is terug bij het gemiddelde, tijd om posities te sluiten."
    return "De spread is binnen normale bereik, wacht op een signaal."

def show_spread_chart(df):
    """Toon de spread chart met trading niveaus"""
    st.subheader("📈 Spread Analyse")
    
    # Bereken niveaus
    entry_long_level = -st.session_state.zscore_entry_threshold * st.session_state.spread_std + st.session_state.spread_mean
    entry_short_level = st.session_state.zscore_entry_threshold * st.session_state.spread_std + st.session_state.spread_mean
    exit_level_pos = st.session_state.zscore_exit_threshold * st.session_state.spread_std + st.session_state.spread_mean
    exit_level_neg = -st.session_state.zscore_exit_threshold * st.session_state.spread_std + st.session_state.spread_mean
    
    # Maak figuur
    fig = go.Figure()
    
    # Voeg spread toe
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['spread'],
        mode='lines',
        name='Spread',
        line=dict(color='#636EFA')
    ))
    
    # Voeg mean toe
    fig.add_hline(
        y=st.session_state.spread_mean,
        line=dict(color='black', dash='dash'),
        annotation_text='Gemiddelde',
        annotation_position='bottom right'
    )
    
    # Voeg trading niveaus toe
    fig.add_hline(
        y=entry_long_level,
        line=dict(color='green', dash='dash'),
        annotation_text='Long Entry',
        annotation_position='bottom left'
    )
    
    fig.add_hline(
        y=entry_short_level,
        line=dict(color='red', dash='dash'),
        annotation_text='Short Entry',
        annotation_position='top left'
    )
    
    fig.add_hline(
        y=exit_level_pos,
        line=dict(color='blue', dash='dot'),
        annotation_text='Exit',
        annotation_position='top right'
    )
    
    fig.add_hline(
        y=exit_level_neg,
        line=dict(color='blue', dash='dot'),
        annotation_text='Exit',
        annotation_position='bottom right'
    )
    
    # Layout aanpassingen
    fig.update_layout(
        title="Spread met Trading Niveaus",
        yaxis_title="Spread Waarde",
        xaxis_title="Datum",
        hovermode='x unified',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_price_and_zscore_charts(df):
    """Toon de prijs en z-score grafieken naast elkaar"""
    st.subheader("📉 Prijs- en Z-score Analyse")
    col1, col2 = st.columns(2)
    
    with col1:
        # Prijsgrafiek
        fig_prices = go.Figure()
        
        fig_prices.add_trace(go.Scatter(
            x=df.index,
            y=df['price1'],
            name=st.session_state.name1,
            line=dict(color='#00CC96')
        ))
        
        fig_prices.add_trace(go.Scatter(
            x=df.index,
            y=df['price2'],
            name=st.session_state.name2,
            line=dict(color='#EF553B'),
            yaxis='y2'
        ))
        
        fig_prices.update_layout(
            title="Genormaliseerde Prijzen",
            xaxis_title="Datum",
            yaxis_title=f"{st.session_state.name1} Prijs (USD)",
            yaxis2=dict(
                title=f"{st.session_state.name2} Prijs (USD)",
                overlaying='y',
                side='right'
            ),
            height=400
        )
        
        st.plotly_chart(fig_prices, use_container_width=True)
    
    with col2:
        # Z-score grafiek
        fig_zscore = go.Figure()
        
        fig_zscore.add_trace(go.Scatter(
            x=df.index,
            y=df['zscore'],
            name='Z-score',
            line=dict(color='#AB63FA')
        ))
        
        # Voeg trading niveaus toe
        fig_zscore.add_hline(
            y=st.session_state.zscore_entry_threshold,
            line=dict(color='red', dash='dash'),
            annotation_text='Short Entry',
            annotation_position='top right'
        )
        
        fig_zscore.add_hline(
            y=-st.session_state.zscore_entry_threshold,
            line=dict(color='green', dash='dash'),
            annotation_text='Long Entry',
            annotation_position='bottom right'
        )
        
        fig_zscore.add_hline(
            y=st.session_state.zscore_exit_threshold,
            line=dict(color='blue', dash='dot'),
            annotation_text='Exit',
            annotation_position='top right'
        )
        
        fig_zscore.add_hline(
            y=-st.session_state.zscore_exit_threshold,
            line=dict(color='blue', dash='dot'),
            annotation_text='Exit',
            annotation_position='bottom right'
        )
        
        fig_zscore.update_layout(
            title="Z-score Evolutie",
            yaxis_title="Z-score",
            xaxis_title="Datum",
            height=400
        )
        
        st.plotly_chart(fig_zscore, use_container_width=True)

def show_correlation_stats(df):
    """Toon correlatie statistieken"""
    st.subheader("📊 Correlatie Statistieken")
    
    # Bereken extra stats
    volatility_ratio = df['returns2'].std() / df['returns1'].std()
    current_rolling_corr = df['rolling_corr'].iloc[-1]
    
    # Toon metrics in kolommen
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Pearson Correlatie", f"{st.session_state.pearson_corr:.4f}")
        st.metric("Beta (β)", f"{st.session_state.beta:.4f}")
        st.metric("R-squared", f"{st.session_state.r_squared:.4f}")
    
    with col2:
        st.metric("Huidige Rolling Correlatie", f"{current_rolling_corr:.4f}")
        st.metric("Gem. Rolling Correlatie", f"{df['rolling_corr'].mean():.4f}")
        st.metric("Alpha (α)", f"{st.session_state.alpha:.6f}")
    
    with col3:
        st.metric("Returns Correlatie", f"{st.session_state.returns_corr:.4f}")
        st.metric("Volatiliteit Ratio", f"{volatility_ratio:.4f}")
        st.metric("Spread Volatiliteit", f"{st.session_state.spread_std:.4f}")

def show_export_options(df):
    """Toon export opties voor de data"""
    st.markdown("---")
    st.subheader("💾 Exporteer Analyse")
    
    if st.button("Genereer CSV Export"):
        # Maak een copy van de dataframe voor export
        export_df = df.copy()
        
        # Voeg belangrijke statistieken toe als metadata
        metadata = {
            'pair': f"{st.session_state.name1}_{st.session_state.name2}",
            'period': st.session_state.periode,
            'interval': st.session_state.interval,
            'alpha': st.session_state.alpha,
            'beta': st.session_state.beta,
            'r_squared': st.session_state.r_squared
        }
        
        # Converteer naar CSV
        csv = export_df.to_csv(index=True)
        
        # Download knop
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"pairs_analysis_{metadata['pair']}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv'
        )