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

portfolio_input = st.text_input("Enter your portfolio (format: TICKER:SHARES, e.g. AAPL:10", "AAPL:10")

if portfolio_input:
    portfolio = {}
    for item in portfolio_input.split(","):
        try:
            ticker, shares = item.strip().split(":")
            portfolio[ticker.strip().upper()] = int(shares.strip())
        except:
            st.error(f"Invalid format: {item}. Please use TICKER:SHARES format.")
    
    if portfolio:
        results = []
        total_value = 0
        
        for ticker, shares in portfolio.items():
            stock = yf.Ticker(ticker)
            price = stock.history(period="1d")["Close"].iloc[-1] if not stock.history(period="1d").empty else None
            if price:
                value = shares * price
                total_value += value
                results.append({"Ticker": ticker, "Shares": shares, "Price": round(price, 2), "Value": round(value, 2)})
        
        if results:
            df_portfolio = pd.DataFrame(results)
            st.dataframe(df_portfolio)

            st.metric("Total Portfolio Value", f"${total_value:,.2f}")

            # Portfolio Allocation Pie Chart
            fig = px.pie(df_portfolio, names="Ticker", values="Value", title="Portfolio Allocation")
            st.plotly_chart(fig, use_container_width=True)
