import streamlit as st
import pandas as pd

# Moving Average Forecast Function
def moving_average_forecast(data, window=5, forecast_days=7):
    historical = data['Sales'].rolling(window=window).mean().iloc[-forecast_days:].values
    forecast = historical[-1] if len(historical) > 0 else 0
    return [forecast] * forecast_days

# Streamlit Application
st.title("Simplified Demand Forecasting Tool")

# Upload CSV File
uploaded_file = st.file_uploader("Upload your sales data CSV file", type="csv")

if uploaded_file:
    # Load and preprocess data
    data = pd.read_csv(uploaded_file)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    # Filter Product
    selected_product = st.selectbox('Select a Product', data['Product'].unique())
    product_data = data[data['Product'] == selected_product]

    # Forecast Future Sales
    forecast_days = st.slider('Forecast Days', min_value=1, max_value=30, value=7)
    forecast = moving_average_forecast(product_data, window=5, forecast_days=forecast_days)

    # Display Historical Data and Forecast Together
    st.line_chart({
        'Historical Sales': product_data['Sales'],
        'Forecasted Sales': pd.Series(forecast, index=pd.date_range(product_data.index[-1], periods=forecast_days, freq='D'))
    })
