import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import yfinance as yf

st.set_page_config(page_title="Market Tracking Dashboard", layout="wide")

st.title("Stock Portfolio Dashboard")

# Gather data from yahoo finance or any other source:
index = "MSFT"
index_ticker = yf.Ticker(index)
data = index_ticker.history(period="max")
data.index = data.index.strftime('%Y-%m-%d')
data = data.drop(columns=['Dividends', 'Stock Splits'])
data.index = pd.to_datetime(data.index)


# Sidebar filters
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date", min_value=data.index.min(), max_value=data.index.max(), value=data.index.min())
end_date = st.sidebar.date_input("End Date", min_value=data.index.min(), max_value=data.index.max(), value=data.index.max())


filtered_data = data[(data.index >= pd.to_datetime(start_date)) & (data.index <= pd.to_datetime(end_date))]

# Main dashboard
st.subheader("Market Price Over Time")
st.line_chart(filtered_data["Close"])

st.subheader("Market Volume Over Time")
st.bar_chart(filtered_data["Volume"])

st.subheader(f"Raw Data for {index}")
st.dataframe(filtered_data)

# Summary statistics
st.sidebar.header("Summary Statistics")
st.sidebar.metric("Latest Price", f"${filtered_data['Close'].iloc[-1]:.2f}")
st.sidebar.metric("Average Volume", f"{filtered_data['Volume'].mean():.0f}")