import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Page config: Wide layout like NoF1.ai
st.set_page_config(page_title="GROK Arena", layout="wide")

# Custom CSS to mirror NoF1.ai: Dark gradient, spaced prices, clean fonts
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
    color: #ffffff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.stMetric > label {
    color: #a0a0a0;
    font-size: 14px;
}
.stMetric > div > h3 {
    color: #00d4ff;
    font-size: 24px;
    font-weight: bold;
}
h1, h2, h3 {
    color: #ffffff;
    text-align: center;
}
.price-header {
    font-size: 18px;
    letter-spacing: 0.5em;
    color: #ffffff;
}
.metric-container {
    background: rgba(255, 255, 255, 0.05);
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}
</style>
""", unsafe_allow_html=True)

# Header mirroring NoF1.ai: Tagline + spaced prices
st.markdown("<h2 style='text-align: center; color: #00d4ff;'>AI trading in real markets</h2>", unsafe_allow_html=True)
st.markdown("---")

# Live crypto prices (keep as float—no string formatting yet)
tickers = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "DOGE-USD", "XRP-USD"]
prices = {}
fallback_prices = {"BTC-USD": 67234.50, "ETH-USD": 2620.75, "SOL-USD": 152.30, "BNB-USD": 585.40, "DOGE-USD": 0.11, "XRP-USD": 0.53}
for ticker in tickers:
    try:
        data = yf.download(ticker, period="1d", interval="1h", progress=False, auto_adjust=False)
        if not data.empty:
            latest = float(data['Close'].iloc[-1])  # Force float—no Series error
            prices[ticker] = latest
        else:
            prices[ticker] = fallback_prices[ticker]
    except:
        prices[ticker] = fallback_prices[ticker]

# Spaced price row (format here—btc_price is float, so :>10,.2f works)
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    btc_price = prices["BTC-USD"]  # Float
    st.markdown(f'<div class="price-header">BTC ${float(btc_price):>10,.2f}</div>', unsafe_allow_html=True)
with col2:
    eth_price = prices["ETH-USD"]  # Float
    st.markdown(f'<div class="price-header">ETH ${float(eth_price):>10,.2f}</div>', unsafe_allow_html=True)
with col3:
    sol_price = prices["SOL-USD"]  # Float
    st.markdown(f'<div class="price-header">SOL ${float(sol_price):>10,.2f}</div>', unsafe_allow_html=True)
with col4:
    bnb_price = prices["BNB-USD"]  # Float
    st.markdown(f'<div class="price-header">BNB ${float(bnb_price):>10,.2f}</div>', unsafe_allow_html=True)
with col5:
    doge_price = prices["DOGE-USD"]  # Float
    st.markdown(f'<div class="price-header">DOGE ${float(doge_price):>10,.2f}</div>', unsafe_allow_html=True)
with col6:
    xrp_price = prices["XRP-USD"]  # Float
    st.markdown(f'<div class="price-header">XRP ${float(xrp_price):>10,.2f}</div>', unsafe_allow_html=True)

st.markdown("---")

# Sidebar: Benchmark (mirror NoF1.ai explanatory panel)
with st.sidebar:
    st.header("The Benchmark")
    st.markdown("""
    **A Better Benchmark for AI Investing**  
    Each model starts with $10,000 of simulated capital on Hyperliquid-style markets.  
    - **Objective**: Maximize risk-adjusted returns (Sharpe ratio).  
    - **Transparency**: All trades, prompts, outputs public.  
    - **Duration**: 2 weeks; Season 2 next.  
    **Contestants**: Grok 4, GPT-5, Claude 3.5, Gemini 2.5 Pro, DeepSeek V3.1, Llama 3.1.  
    """)

# Tabs (subtle, like NoF1.ai navigation)
tab1, tab2, tab3 = st.tabs(["LIVE", "LEADERBOARD", "MODELS"])

with tab1:
    st.header("TOTAL ACCOUNT VALUE")  # Mirror NoF1.ai heading
    st.button("DETAILED VIEW")  # Mirror button
    st.markdown("----------------------------------------------------------------------------------------------------")  # Mirror dashes separator

    # Simulated data (gradual rises)
    dates = pd.date_range(start="2025-10-21 17:00", end="2025-10-29 07:58", periods=9)
    gpt_values = np.linspace(10000, 87477, 9)
    claude_values = np.linspace(10000, 84739, 9)
    gemini_values = np.linspace(10000, 64619, 9)
    grok_values = np.linspace(10000, 119964, 9)
    deepseek_values = np.linspace(10000, 115876, 9)
    llama_values = np.linspace(10000, 110458, 9)

    # Plotly chart (mirror NoF1.ai loading vibe if needed, but full lines)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=gpt_values, mode='lines', name='GPT-5', line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=dates, y=claude_values, mode='lines', name='Claude 3.5', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=dates, y=gemini_values, mode='lines', name='Gemini 2.5', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=dates, y=grok_values, mode='lines', name='Grok 4', line=dict(color='blue', width=4)))
    fig.add_trace(go.Scatter(x=dates, y=deepseek_values, mode='lines', name='DeepSeek V3.1', line=dict(color='purple')))
    fig.add_trace(go.Scatter(x=dates, y=llama_values, mode='lines', name='Llama 3.1', line=dict(color='gray')))

    fig.update_layout(
        title="Model Portfolio Performance Over Time",
        xaxis_title="Date & Time",
        yaxis_title="Account Value ($)",
        yaxis_range=[0, 120000],
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, config={'displayModeBar': False}, use_container_width=True)

    # Grok Trading Sim (button only)
    st.subheader("Grok 4 Live Trading Sim")
    if 'grok_capital' not in st.session_state:
        st.session_state.grok_capital = 10000
        st.session_state.trades = []
        st.session_state.last_btc = prices["BTC-USD"]  # Float now

    if st.button("Simulate Trade Update"):
        current_btc = prices["BTC-USD"]  # Float
        price_change = ((current_btc - st.session_state.last_btc) / st.session_state.last_btc) * 100

        if price_change < -2:
            trade_amount = st.session_state.grok_capital * 0.1
            st.session_state.grok_capital -= trade_amount
            btc_bought = trade_amount / current_btc
            st.session_state.trades.append({"Time": datetime.now().strftime("%H:%M"), "Action": "BUY", "Asset": "BTC", "Amount": btc_bought, "Price": current_btc, "P&L": 0})
            st.success(f"🟢 Grok bought {btc_bought:.4f} BTC at ${current_btc:,.2f} (dip: {price_change:.1f}%)")
        elif price_change > 3:
            if st.session_state.trades:
                st.warning(f"🟡 Grok sold partial at ${current_btc:,.2f} (gain: {price_change:.1f}%)")
                st.session_state.grok_capital += 2000
                if st.session_state.trades:
                    st.session_state.trades[-1]["P&L"] = 150

        st.session_state.last_btc = current_btc
        st.rerun()

    st.metric("Grok 4 Capital", f"${st.session_state.grok_capital:,.2f}")

    if st.session_state.trades:
        trades_df = pd.DataFrame(st.session_state.trades)
        st.dataframe(trades_df, use_container_width=True)

with tab2:
    st.header("LEADING MODELS")  # Mirror NoF1.ai
    st.markdown("----------------------------------------------------------------------------------------------------")  # Mirror dashes
    data = {
        'Rank': [1, 2, 3, 4, 5, 6],
        'Model': ['Grok 4', 'DeepSeek V3.1', 'Llama 3.1', 'GPT-5', 'Claude 3.5', 'Gemini 2.5'],
        'Final Value': ['$119,964', '$115,876', '$110,458', '$87,477', '$84,739', '$64,619'],
        'Sharpe Ratio': [1.45, 1.32, 1.28, 1.12, 1.05, 0.92],
        'Completed Trades': [128, 115, 107, 92, 88, 76]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

with tab3:
    st.header("Models")
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.expander("Grok 4 (xAI)"):
            st.write("**Bio**: Grok 4 excels in bold, data-driven crypto strategies.")
            st.subheader("Sample Prompt")
            st.code("Analyze BTC 1h: Buy if RSI <30 and >MA50. Sell if RSI >70.")
            st.subheader("Trades Log")
            trades_data = {
                'Time': ['Oct 22 14:00', 'Oct 23 09:30', 'Oct 25 16:45'],
                'Action': ['BUY', 'SELL', 'BUY'],
                'Asset': ['BTC', 'SOL', 'ETH'],
                'Amount': [0.01, 2.5, 0.5],
                'P&L': ['+$150', '-$45', '+$320']
            }
            trades_df = pd.DataFrame(trades_data)
            st.dataframe(trades_df, use_container_width=True)
    with col2:
        with st.expander("GPT-5 (OpenAI)"):
            st.write("**Bio**: Conservative, diversified portfolios for steady gains.")
            st.subheader("Sample Prompt")
            st.code("Scan ETH/SOL: Allocate 50% to top if volume > avg.")
            st.subheader("Trades Log")
            st.info("Placeholder—Grok's got more action!")
    with col3:
        with st.expander("Claude 3.5 (Anthropic)"):
            st.write("**Bio**: Ethical, low-volatility trades.")
            st.subheader("Sample Prompt")
            st.code("Risk check: Avoid if volatility >5%.")
            st.subheader("Trades Log")
            st.info("Placeholder.")