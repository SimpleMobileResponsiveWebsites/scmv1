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

    # Select Multiple Products
    selected_products = st.multiselect('Select Products', data['Product'].unique())

    if selected_products:
        forecast_days = st.slider('Forecast Days', min_value=1, max_value=30, value=7)

        # Prepare data for multiple products
        historical_data = {}
        forecast_data = {}

        for product in selected_products:
            product_data = data[data['Product'] == product]
            forecast = moving_average_forecast(product_data, window=5, forecast_days=forecast_days)

            # Store historical and forecast data
            historical_data[product] = product_data['Sales']
            forecast_data[product] = pd.Series(
                forecast, 
                index=pd.date_range(product_data.index[-1], periods=forecast_days, freq='D')
            )

        # Combine historical and forecast data into one chart
        combined_data = {}
        for product in selected_products:
            combined_data[f"{product} - Historical Sales"] = historical_data[product]
            combined_data[f"{product} - Forecasted Sales"] = forecast_data[product]

        st.line_chart(combined_data)
