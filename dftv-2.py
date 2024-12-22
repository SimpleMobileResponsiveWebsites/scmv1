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
st.title("Time Series Forecasting with Moving Average")

# Upload CSV File for Historical Data
uploaded_historical_file = st.file_uploader("Upload your historical sales data CSV file", type="csv")

# Upload CSV File for Forecasted Data (Optional)
uploaded_forecast_file = st.file_uploader("Upload your forecasted sales data CSV file (Optional)", type="csv")

if uploaded_historical_file:
    # Load and preprocess historical data
    historical_data = pd.read_csv(uploaded_historical_file)
    historical_data['Date'] = pd.to_datetime(historical_data['Date'])
    historical_data.set_index('Date', inplace=True)

    # Select Multiple Products
    selected_products = st.multiselect('Select Products', historical_data['Product'].unique())

    if selected_products:
        forecast_days = st.slider('Forecast Days', min_value=1, max_value=30, value=7)

        # Allow users to select forecast method
        forecast_method = st.radio("Select Forecasting Method", ("Moving Average", "Time Series"))

        # Prepare data for multiple products
        combined_data = {}

        for product in selected_products:
            product_data = historical_data[historical_data['Product'] == product]

            # Generate forecasts based on selected method
            if forecast_method == "Moving Average":
                forecast = moving_average_forecast(product_data, window=5, forecast_days=forecast_days)
            else:
                forecast = basic_time_series_forecast(product_data, forecast_days=forecast_days)

            # Store historical and forecast data
            combined_data[f"{product} - Historical Sales"] = product_data['Sales']
            combined_data[f"{product} - Forecasted Sales"] = pd.Series(
                forecast,
                index=pd.date_range(product_data.index[-1], periods=forecast_days, freq='D')
            )

        # Display the combined data
        st.line_chart(combined_data)

        # If a forecasted file is uploaded, combine user-provided forecasts
        if uploaded_forecast_file:
            forecast_data = pd.read_csv(uploaded_forecast_file)
            forecast_data['Date'] = pd.to_datetime(forecast_data['Date'])
            forecast_data.set_index('Date', inplace=True)

            for product in selected_products:
                product_forecast_data = forecast_data[forecast_data['Product'] == product]
                combined_data[f"{product} - User Forecasted Sales"] = product_forecast_data['Sales']

            st.line_chart(combined_data)
