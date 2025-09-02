import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px


# Streamlit App Title
st.title("📈 Stock Market Tracker")


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
