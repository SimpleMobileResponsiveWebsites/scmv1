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
st.title("Time Series Forecasting Tool")

# Sidebar navigation for different pages
page = st.sidebar.selectbox("Select a Page", ["Forecasting Tool", "Learning About Moving Averages"])

if page == "Forecasting Tool":
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

elif page == "Learning About Moving Averages":
    # Add educational content here
    st.header("Time Series Forecasting with Moving Averages")

    st.write("""
    Time series forecasting with moving averages is a popular method for predicting future sales based on historical data. 
    This technique helps smooth out short-term fluctuations and highlight longer-term trends in sales data.
    """)

    st.subheader("How Moving Averages Work")
    st.write("""
    The moving average method involves calculating the average of a fixed number of data points over a specified time period. 
    This "window" of data points moves forward in time, creating a series of averages that can be used to forecast future values.
    """)

    st.subheader("Simple Moving Average (SMA)")
    st.write("""
    1. Select a window size (e.g., 3 months, 6 months, or 12 months)
    2. Calculate the average of sales data within that window
    3. Move the window forward by one time period
    4. Repeat the process to create a series of averages

    Example: 
    - Average sales from January to March for April's forecast
    - Average sales from February to April for May's forecast
    - Continue this pattern for subsequent months.
    """)

    st.subheader("Weighted Moving Average (WMA)")
    st.write("""
    The weighted moving average assigns different weights to data points within the window, typically giving more importance to recent data:
    - Assign percentages to each period in the window (e.g., 15% for the oldest, 20% for the middle, and 35% for the most recent)
    - Multiply each period's sales by its assigned percentage
    - Sum the weighted values to create the forecast
    """)

    st.subheader("Forecasting Process")
    st.write("""
    1. Analyze historical sales data to identify patterns and trends
    2. Choose an appropriate window size based on the data's characteristics
    3. Calculate moving averages using either SMA or WMA
    4. Use the calculated averages to predict future sales

    The moving average serves as a baseline forecast, which can be adjusted for:
    - Seasonal variations
    - Long-term trends
    - Known future events or market changes
    """)

    st.subheader("Advantages and Limitations")
    st.write("""
    **Advantages**:
    - Smooths out short-term fluctuations
    - Highlights underlying trends
    - Relatively simple to implement and understand

    **Limitations**:
    - May lag behind rapid changes in trends
    - Does not account for seasonality on its own
    - Accuracy decreases for longer forecast horizons
    """)

    st.subheader("Improving Forecast Accuracy")
    st.write("""
    To enhance the accuracy of moving average forecasts:
    - Combine with other forecasting methods (e.g., regression analysis)
    - Adjust for seasonality and trends
    - Regularly update the model with new data
    - Use software tools for more complex calculations and analysis
    """)

    st.write("""
    By understanding and properly applying the moving average method, businesses can create more reliable sales forecasts, helping with inventory management, resource allocation, and strategic planning.
    """)
