import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

def show(df_backtest, trades):
    """Toon de backtesting resultaten sectie"""
    st.header("🔙 Backtesting Resultaten")
    
    if len(trades) > 0:
        show_backtest_results(df_backtest, trades)
        show_trade_history(trades)
        show_export_options(df_backtest, trades)
    else:
        st.warning("Geen trades uitgevoerd in de backtesting periode. Probeer andere parameters.")

def show_backtest_results(df_backtest, trades):
    """Toon de backtest resultaten en prestatie metrics"""
    st.subheader("📊 Prestatie Metrics")
    
    # Bereken key metrics
    trades_df = pd.DataFrame(trades)
    initial_capital = st.session_state.initial_capital
    final_value = df_backtest['portfolio_value'].iloc[-1]
    total_return = ((final_value - initial_capital) / initial_capital) * 100
    
    # Trade metrics
    winning_trades = trades_df[trades_df['P&L'] > 0]
    losing_trades = trades_df[trades_df['P&L'] < 0]
    
    win_rate = (len(winning_trades) / len(trades_df)) * 100 if len(trades_df) > 0 else 0
    avg_win = winning_trades['P&L'].mean() if len(winning_trades) > 0 else 0
    avg_loss = losing_trades['P&L'].mean() if len(losing_trades) > 0 else 0
    profit_factor = abs(winning_trades['P&L'].sum() / losing_trades['P&L'].sum()) if len(losing_trades) > 0 else float('inf')
    
    # Risk metrics
    returns = df_backtest['portfolio_value'].pct_change().dropna()
    volatility = returns.std() * np.sqrt(252)  # Annualized volatility
    sharpe_ratio = (total_return / 100) / volatility if volatility > 0 else 0
    max_drawdown = ((df_backtest['portfolio_value'].cummax() - df_backtest['portfolio_value']) / 
                   df_backtest['portfolio_value'].cummax()).max() * 100
    
    # Buy and hold benchmark
    buy_hold_value = initial_capital * (df_backtest['price1'].iloc[-1] / df_backtest['price1'].iloc[0])
    buy_hold_return = ((buy_hold_value - initial_capital) / initial_capital) * 100
    
    # Toon metrics in kolommen
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Totaal Rendement", f"{total_return:.2f}%", 
                 f"{total_return - buy_hold_return:.2f}% vs buy & hold")
        st.metric("Eindwaarde", f"${final_value:,.0f}")
        st.metric("Aantal Trades", len(trades_df))
    
    with col2:
        st.metric("Win Rate", f"{win_rate:.1f}%")
        st.metric("Gemiddelde Win", f"${avg_win:,.0f}")
        st.metric("Gemiddelde Loss", f"${avg_loss:,.0f}")
    
    with col3:
        st.metric("Profit Factor", f"{profit_factor:.2f}")
        st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
        st.metric("Max Drawdown", f"{max_drawdown:.2f}%")
    
    with col4:
        st.metric("Buy & Hold Rendement", f"{buy_hold_return:.2f}%")
        st.metric("Volatiliteit", f"{volatility:.2f}")
        st.metric("Gem. Holding Periode", f"{trades_df['Days Held'].mean():.1f} dagen")
    
    # Portfolio value grafiek
    fig = go.Figure()
    
    # Portfolio lijn
    fig.add_trace(go.Scatter(
        x=df_backtest.index,
        y=df_backtest['portfolio_value'],
        mode='lines',
        name='Portfolio Value',
        line=dict(color='#00CC96', width=2)
    ))
    
    # Buy and hold benchmark
    fig.add_hline(
        y=buy_hold_value, 
        line_dash="dash", 
        line_color="#636EFA",
        annotation_text=f"Buy & Hold {st.session_state.name1}: ${buy_hold_value:,.0f}",
        annotation_position="bottom right"
    )
    
    # Voeg trade markers toe
    for trade in trades:
        # Entry marker
        fig.add_trace(go.Scatter(
            x=[trade['Entry Date']],
            y=[df_backtest.loc[trade['Entry Date'], 'portfolio_value']],
            mode='markers',
            marker=dict(
                color='green' if trade['Position'] == 'Long Spread' else 'red',
                size=10,
                symbol='triangle-up' if trade['Position'] == 'Long Spread' else 'triangle-down'
            ),
            name=f"Entry {trade['Position']}",
            showlegend=False
        ))
        
        # Exit marker
        fig.add_trace(go.Scatter(
            x=[trade['Exit Date']],
            y=[df_backtest.loc[trade['Exit Date'], 'portfolio_value']],
            mode='markers',
            marker=dict(
                color='blue',
                size=8,
                symbol='x'
            ),
            name="Exit",
            showlegend=False
        ))
    
    fig.update_layout(
        title="Portfolio Ontwikkeling met Trades",
        xaxis_title="Datum",
        yaxis_title="Waarde (USD)",
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_trade_history(trades):
    """Toon de gedetailleerde trade history"""
    st.subheader("📋 Trade Geschiedenis")
    
    trades_df = pd.DataFrame(trades)
    
    # Maak een mooiere weergave voor de tabel
    display_df = trades_df.copy()
    display_df['Entry Date'] = display_df['Entry Date'].dt.strftime('%Y-%m-%d')
    display_df['Exit Date'] = display_df['Exit Date'].dt.strftime('%Y-%m-%d')
    display_df['P&L'] = display_df['P&L'].apply(lambda x: f"${x:,.0f}")
    display_df['P&L %'] = display_df['P&L %'].apply(lambda x: f"{x:.2f}%")
    display_df['Position Size'] = display_df['Position Size'].apply(lambda x: f"${x:,.0f}")
    
    # Toon de tabel
    st.dataframe(
        display_df[[
            'Entry Date', 'Exit Date', 'Position', 
            'P&L', 'P&L %', 'Position Size',
            'Exit Reason', 'Days Held'
        ]],
        use_container_width=True,
        height=400
    )
    
    # Toon distributie grafieken
    st.subheader("📊 Trade Analyse")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pnl = px.histogram(
            trades_df, 
            x='P&L %', 
            nbins=20,
            title="P&L Distributie (%)",
            color_discrete_sequence=['#00CC96']
        )
        st.plotly_chart(fig_pnl, use_container_width=True)
    
    with col2:
        fig_days = px.histogram(
            trades_df, 
            x='Days Held', 
            nbins=15,
            title="Holding Periode (Dagen)",
            color_discrete_sequence=['#636EFA']
        )
        st.plotly_chart(fig_days, use_container_width=True)

def show_export_options(df_backtest, trades):
    """Toon opties om backtest data te exporteren"""
    st.markdown("---")
    st.subheader("💾 Exporteer Resultaten")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Exporteer Portfolio Data"):
            csv = df_backtest.to_csv(index=True)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"portfolio_results_{st.session_state.name1}_{st.session_state.name2}.csv",
                mime='text/csv'
            )
    
    with col2:
        if st.button("Exporteer Trade Geschiedenis"):
            trades_df = pd.DataFrame(trades)
            csv = trades_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"trade_history_{st.session_state.name1}_{st.session_state.name2}.csv",
                mime='text/csv'
            )

def run_backtest(df, entry_threshold, exit_threshold, initial_capital, 
                transaction_cost, max_position_size, stop_loss_pct, take_profit_pct):
    """Voer de backtest uit volgens de pairs trading strategie"""
    # Bereken spread en z-score
    X = df['price1'].values.reshape(-1, 1)
    y = df['price2'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    alpha = model.intercept_
    beta = model.coef_[0]
    
    df['spread'] = df['price2'] - (alpha + beta * df['price1'])
    spread_mean = df['spread'].mean()
    spread_std = df['spread'].std()
    df['zscore'] = (df['spread'] - spread_mean) / spread_std
    
    # Initialiseer backtesting variabelen
    cash = initial_capital
    position = 0  # 0 = geen positie, 1 = long spread, -1 = short spread
    coin1_shares = 0
    coin2_shares = 0
    entry_price1 = 0
    entry_price2 = 0
    entry_date = None
    position_value = 0
    
    # Tracking variabelen
    trades = []
    portfolio_values = []
    positions = []
    
    # Bereken maximum positie grootte
    max_position_value = (max_position_size / 100) * initial_capital
    
    for i in range(len(df)):
        current_zscore = df['zscore'].iloc[i]
        current_price1 = df['price1'].iloc[i]
        current_price2 = df['price2'].iloc[i]
        current_date = df.index[i]
        
        # Bereken huidige portfolio waarde
        position_market_value = coin1_shares * current_price1 + coin2_shares * current_price2
        portfolio_value = cash + position_market_value
        
        # Check voor nieuwe posities
        if position == 0 and i > 0:
            if current_zscore < -entry_threshold:  # Long spread signaal
                position = 1
                position_value = min(max_position_value, portfolio_value * 0.95)
                
                half_position = position_value / 2
                coin2_shares = half_position / current_price2  # Long coin2
                coin1_shares = -half_position / current_price1  # Short coin1
                
                entry_price1 = current_price1
                entry_price2 = current_price2
                entry_date = current_date
                
                # Transactiekosten
                transaction_costs = position_value * (transaction_cost / 100)
                cash -= transaction_costs
                
            elif current_zscore > entry_threshold:  # Short spread signaal
                position = -1
                position_value = min(max_position_value, portfolio_value * 0.95)
                
                half_position = position_value / 2
                coin1_shares = half_position / current_price1  # Long coin1
                coin2_shares = -half_position / current_price2  # Short coin2
                
                entry_price1 = current_price1
                entry_price2 = current_price2
                entry_date = current_date
                
                # Transactiekosten
                transaction_costs = position_value * (transaction_cost / 100)
                cash -= transaction_costs
        
        # Check voor exit condities
        elif position != 0:
            exit_trade = False
            exit_reason = ""
            
            # Normal exit op z-score
            if abs(current_zscore) < exit_threshold:
                exit_trade = True
                exit_reason = "Z-score exit"
            
            # P&L berekening voor risk management
            current_position_value = abs(coin1_shares * current_price1) + abs(coin2_shares * current_price2)
            pnl_dollar = (coin1_shares * (current_price1 - entry_price1) + 
                         coin2_shares * (current_price2 - entry_price2))
            pnl_pct = (pnl_dollar / position_value) * 100
            
            # Stop loss en take profit checks
            if pnl_pct < -stop_loss_pct:
                exit_trade = True
                exit_reason = "Stop loss"
            elif pnl_pct > take_profit_pct:
                exit_trade = True
                exit_reason = "Take profit"
            
            # Execute exit
            if exit_trade:
                final_pnl = pnl_dollar
                exit_transaction_costs = current_position_value * (transaction_cost / 100)
                final_pnl -= exit_transaction_costs
                cash += (coin1_shares * current_price1 + coin2_shares * current_price2 + final_pnl)
                
                # Log trade
                trades.append({
                    'Entry Date': entry_date,
                    'Exit Date': current_date,
                    'Position': 'Long Spread' if position == 1 else 'Short Spread',
                    'Entry Z-score': df['zscore'].loc[entry_date],
                    'Exit Z-score': current_zscore,
                    'Entry Price 1': entry_price1,
                    'Entry Price 2': entry_price2,
                    'Exit Price 1': current_price1,
                    'Exit Price 2': current_price2,
                    'Coin1 Shares': coin1_shares,
                    'Coin2 Shares': coin2_shares,
                    'Position Size': position_value,
                    'P&L': final_pnl,
                    'P&L %': (final_pnl / position_value) * 100,
                    'Exit Reason': exit_reason,
                    'Days Held': (current_date - entry_date).days
                })
                
                # Reset position
                position = 0
                coin1_shares = 0
                coin2_shares = 0
                entry_price1 = 0
                entry_price2 = 0
                entry_date = None
                position_value = 0
        
        # Track portfolio value en posities
        portfolio_values.append(portfolio_value)
        positions.append(position)
    
    # Creëer results DataFrame
    df_result = df.copy()
    df_result['portfolio_value'] = portfolio_values
    df_result['position'] = positions
    
    return df_result, trades