import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def moving_average_forecast(data, window=5, forecast_days=7):
    forecast = data['Sales'].rolling(window=window).mean().shift(1).iloc[-forecast_days:].values
    return forecast

# Streamlit Interface
st.title("Basic Time Series Forecasting with Moving Average")

# Data Upload
uploaded_file = st.file_uploader("Upload CSV", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    # Preprocess Data
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    # User Input
    product_filter = st.selectbox('Select Product', data['Product'].unique())
    filtered_data = data[data['Product'] == product_filter]

    # Forecast
    forecast_days = st.slider('Number of Days to Forecast', 1, 30, 7)
    forecast = moving_average_forecast(filtered_data, window=5, forecast_days=forecast_days)

    # Visualization
    st.line_chart(filtered_data['Sales'])
    st.line_chart(forecast)
