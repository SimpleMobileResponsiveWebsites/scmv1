import streamlit as st
import pandas as pd

# Moving Average Forecast Function
def moving_average_forecast(data, window=5, forecast_days=7):
    historical = data['Sales'].rolling(window=window).mean().iloc[-forecast_days:].values
    forecast = historical[-1] if len(historical) > 0 else 0
    return [forecast] * forecast_days

# Basic Time Series Forecasting Function
def basic_time_series_forecast(data, forecast_days=7):
    # Use the mean of the last observed data points as the forecast
    last_values = data['Sales'].iloc[-forecast_days:]
    if len(last_values) > 0:
        forecast = last_values.mean()
    else:
        forecast = 0
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

    # Select Multiple Products
    selected_products = st.multiselect('Select Products', data['Product'].unique())

    if selected_products:
        forecast_days = st.slider('Forecast Days', min_value=1, max_value=30, value=7)

        # Prepare data for multiple products
        historical_data = {}
        ma_forecast_data = {}
        ts_forecast_data = {}

        for product in selected_products:
            product_data = data[data['Product'] == product]

            # Moving Average Forecast
            ma_forecast = moving_average_forecast(product_data, window=5, forecast_days=forecast_days)

            # Basic Time Series Forecast
            ts_forecast = basic_time_series_forecast(product_data, forecast_days=forecast_days)

            # Store historical and forecast data
            historical_data[product] = product_data['Sales']
            ma_forecast_data[product] = pd.Series(
                ma_forecast, 
                index=pd.date_range(product_data.index[-1], periods=forecast_days, freq='D')
            )
            ts_forecast_data[product] = pd.Series(
                ts_forecast,
                index=pd.date_range(product_data.index[-1], periods=forecast_days, freq='D')
            )

        # Combine and display data dynamically
        display_historical = st.checkbox("Display Historical Data", value=True)
        display_ma_forecast = st.checkbox("Display MA Forecast", value=True)
        display_ts_forecast = st.checkbox("Display TS Forecast", value=True)

        combined_data = {}
        for product in selected_products:
            if display_historical:
                combined_data[f"{product} - Historical Sales"] = historical_data[product]
            if display_ma_forecast:
                combined_data[f"{product} - MA Forecasted Sales"] = ma_forecast_data[product]
            if display_ts_forecast:
                combined_data[f"{product} - TS Forecasted Sales"] = ts_forecast_data[product]

        st.line_chart(combined_data)
