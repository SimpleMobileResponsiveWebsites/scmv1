import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import streamlit as st

class DemandForecastingTool:
    def __init__(self):
        self.model = LinearRegression()

    def load_data(self, file_path):
        """
        Load the historical sales data from a CSV file.
        The CSV file should have columns: 'Date', 'Product', 'Sales'
        """
        self.data = pd.read_csv(file_path)
        
        # Check if the necessary columns are in the data
        if 'Date' not in self.data.columns or 'Product' not in self.data.columns or 'Sales' not in self.data.columns:
            st.write("Missing required columns in the CSV file.")
            return
        
        # Convert Date column to datetime and sort
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data.sort_values(by='Date', inplace=True)
        st.write("Data loaded successfully.")

    def preprocess_data(self, product_name):
        """
        Filter data for a specific product and prepare features for modeling.
        """
        product_data = self.data[self.data['Product'] == product_name]
        
        # Check if there is data for the selected product
        if product_data.empty:
            st.write(f"No data available for the product: {product_name}.")
            return

        # Create the 'Days' feature (difference in days from the first date)
        product_data['Days'] = (product_data['Date'] - product_data['Date'].min()).dt.days

        # Define features (X) and target variable (y)
        X = product_data[['Days']]
        y = product_data['Sales']

        # Ensure there is enough data for training
        if X.empty or y.empty:
            st.write(f"Not enough data for the selected product: {product_name}.")
            return

        # Split the data into training and testing sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        st.write(f"Data preprocessed for product: {product_name}")

    def train_model(self):
        """
        Train the linear regression model using the preprocessed data.
        """
        # Ensure data has been preprocessed before training
        if not hasattr(self, 'X_train') or not hasattr(self, 'y_train'):
            st.write("Please preprocess the data first.")
            return

        # Ensure training data is not empty
        if self.X_train.empty or self.y_train.empty:
            st.write("Training data is empty. Please preprocess the data first.")
            return

        # Fit the model
        self.model.fit(self.X_train, self.y_train)
        st.write("Model training completed.")

    def evaluate_model(self):
        """
        Evaluate the model's performance on test data.
        """
        # Ensure model is trained before evaluation
        if not hasattr(self, 'model') or not hasattr(self, 'X_test') or not hasattr(self, 'y_test'):
            st.write("Please train the model first.")
            return

        # Make predictions
        y_pred = self.model.predict(self.X_test)

        # Calculate evaluation metrics
        mae = mean_absolute_error(self.y_test, y_pred)
        mse = mean_squared_error(self.y_test, y_pred)
        rmse = np.sqrt(mse)

        st.write("Model Evaluation:")
        st.write(f"Mean Absolute Error (MAE): {mae:.2f}")
        st.write(f"Mean Squared Error (MSE): {mse:.2f}")
        st.write(f"Root Mean Squared Error (RMSE): {rmse:.2f}")

    def forecast(self, days_ahead):
        """
        Predict sales for a given number of days ahead.
        """
        # Ensure model is trained before forecasting
        if not hasattr(self, 'model') or not hasattr(self, 'X_train'):
            st.write("Please train the model first.")
            return

        # Get the maximum day from the training data
        max_days = self.X_train['Days'].max()
        future_days = np.array([max_days + i for i in range(1, days_ahead + 1)]).reshape(-1, 1)

        # Make predictions for the future days
        predictions = self.model.predict(future_days)

        # Create a DataFrame for the forecasted sales
        forecast_df = pd.DataFrame({
            'Days Ahead': range(1, days_ahead + 1),
            'Predicted Sales': predictions
        })

        st.write("Forecast completed:")
        st.dataframe(forecast_df)
        return forecast_df

    def plot_forecast(self, product_name, forecast_df):
        """
        Plot historical sales data and forecasted sales.
        """
        # Ensure forecast is available before plotting
        if forecast_df is None or forecast_df.empty:
            st.write("No forecast data available to plot.")
            return
        
        product_data = self.data[self.data['Product'] == product_name]
        plt.figure(figsize=(10, 6))

        # Plot historical sales
        plt.plot(product_data['Date'], product_data['Sales'], label="Historical Sales", marker='o')

        # Generate future dates for plotting
        future_dates = [product_data['Date'].max() + pd.Timedelta(days=x) for x in forecast_df['Days Ahead']]
        plt.plot(future_dates, forecast_df['Predicted Sales'], label="Forecasted Sales", linestyle='--', color='red')

        plt.title(f"Sales Forecast for {product_name}")
        plt.xlabel("Date")
        plt.ylabel("Sales")
        plt.legend()
        plt.grid()
        st.pyplot(plt)

# Streamlit app
st.title("Demand Forecasting Tool")

uploaded_file = st.file_uploader("Upload CSV file with sales data", type="csv")
if uploaded_file is not None:
    tool = DemandForecastingTool()
    tool.load_data(uploaded_file)

    if hasattr(tool, 'data') and tool.data is not None:
        products = tool.data['Product'].unique()
        product_name = st.selectbox("Select Product for Forecasting", products)

        if st.button("Preprocess Data"):
            tool.preprocess_data(product_name)

        if st.button("Train Model"):
            tool.train_model()

        if st.button("Evaluate Model"):
            tool.evaluate_model()

        days_ahead = st.number_input("Enter number of days to forecast", min_value=1, step=1)
        if st.button("Forecast"):
            forecast = tool.forecast(days_ahead)
            st.write(forecast)

        if st.button("Plot Forecast"):
            tool.plot_forecast(product_name, forecast)
