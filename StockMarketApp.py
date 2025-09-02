import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Streamlit App Title
st.title("Stock Market Tracker")


# Sidebar for User Input
st.sidebar.header("User Input")

# User enters stock ticker
ticker = st.sidebar.text_input("Enter Stock Ticker", "AAPL")

# Select time period
period = st.sidebar.selectbox("Select Time Period", ["1d", "5d", "1mo", "6mo", "1y", "5y", "max"], index=4)


# Fetch Stock Data
stock = yf.Ticker(ticker)
data = stock.history(period=period)

if not data.empty:
    st.subheader(f"{ticker} Stock Price")
    fig = px.line(data, x=data.index, y="Close", title=f"{ticker} Closing Price")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Recent Data")
    st.write(data.tail())
else:
    st.warning("No data found for this ticker. Try another one.")


# Portfolio Tracker
st.subheader("Portfolio Tracker")

portfolio_input = st.text_input(
    "Enter your portfolio (format: TICKER:SHARES, e.g. AAPL:10)", 
    "AAPL:10, MSFT:5"
)

if portfolio_input:
    portfolio = {}
    for item in portfolio_input.split(","):
        try:
            ticker_port, shares = item.strip().split(":")
            portfolio[ticker_port.strip().upper()] = int(shares.strip())
        except:
            st.error(f"Invalid format: {item}. Please use TICKER:SHARES format.")
    
    if portfolio:
        results = []
        total_value = 0
        
        for ticker_port, shares in portfolio.items():
            stock_port = yf.Ticker(ticker_port)
            hist = stock_port.history(period="2d") 
            
            if not hist.empty and len(hist) >= 2:
                price_today = hist["Close"].iloc[-1]
                price_yesterday = hist["Close"].iloc[-2]
                change = price_today - price_yesterday
                pct_change = (change / price_yesterday) * 100

                value = shares * price_today
                total_value += value

                results.append({
                    "Ticker": ticker_port,
                    "Shares": shares,
                    "Price": round(price_today, 2),
                    "Value": round(value, 2),
                    "Change $": round(change, 2),
                    "Change %": f"{pct_change:.2f}%"
                })
        
        if results:
            df_portfolio = pd.DataFrame(results)
            
            # Highlight daily % change in red/green
            def highlight_change(val):
                if isinstance(val, str) and "%" in val:
                    num = float(val.replace("%",""))
                    color = "green" if num > 0 else "red"
                    return f"color: {color}"
                return ""
            
            st.dataframe(df_portfolio.style.applymap(highlight_change, subset=["Change %"]))

            st.metric("Total Portfolio Value", f"${total_value:,.2f}")

            # Portfolio Allocation Pie Chart
            fig = px.pie(df_portfolio, names="Ticker", values="Value", title="Portfolio Allocation")
            st.plotly_chart(fig, use_container_width=True)

