# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import streamlit as st

# Main Tool Class
class DemandForecastingTool:
    def __init__(self):
        self.model = LinearRegression()
        self.data = None  # Initialize data attribute
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def load_data(self, file_path):
        """
        Load the historical sales data from a CSV file.
        The CSV file should have columns: 'Date', 'Product', 'Sales'
        """
        try:
            # Load data from the CSV file
            st.write("Loading data from the file...")
            self.data = pd.read_csv(file_path)
            
            # Check if the necessary columns exist
            if not {'Date', 'Product', 'Sales'}.issubset(self.data.columns):
                st.error("CSV file must contain 'Date', 'Product', and 'Sales' columns.")
                return

            # Convert 'Date' to datetime and handle errors gracefully
            self.data['Date'] = pd.to_datetime(self.data['Date'], errors='coerce')

            # Drop rows with missing or invalid values in 'Date' or 'Sales'
            self.data.dropna(subset=['Date', 'Sales'], inplace=True)
            self.data.sort_values(by='Date', inplace=True)
            
            st.write("✅ Data loaded successfully.")
            st.write(self.data.head())  # Show the first few rows for confirmation
        except Exception as e:
            st.error(f"Error loading data: {e}")

    def preprocess_data(self, product_name):
        """
        Filter data for a specific product and prepare features for modeling.
        """
        if self.data is None:
            st.error("Data not loaded. Please upload a file.")
            return
        
        try:
            st.write(f"Preprocessing data for {product_name}...")
            product_data = self.data[self.data['Product'] == product_name]
            if product_data.empty:
                st.error(f"No data found for product: {product_name}")
                return

            # Convert dates to days since the first date
            product_data['Days'] = (product_data['Date'] - product_data['Date'].min()).dt.days

            # Prepare features (X) and target (y)
            X = product_data[['Days']]
            y = product_data['Sales']

            # Split the data into training and test sets
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            st.write(f"✅ Data preprocessed for product: {product_name}")
        except Exception as e:
            st.error(f"Error in preprocessing: {e}")

    def train_model(self):
        """
        Train the linear regression model using the preprocessed data.
        """
        if self.X_train is not None and self.y_train is not None:
            try:
                st.write("Training the model...")
                self.model.fit(self.X_train, self.y_train)
                st.write("✅ Model training completed.")
            except Exception as e:
                st.error(f"Error during model training: {e}")
        else:
            st.error("Data not preprocessed. Please preprocess data before training the model.")

    def evaluate_model(self):
        """
        Evaluate the model's performance on test data.
        """
        if self.X_test is not None and self.y_test is not None:
            try:
                y_pred = self.model.predict(self.X_test)
                mae = mean_absolute_error(self.y_test, y_pred)
                mse = mean_squared_error(self.y_test, y_pred)
                rmse = np.sqrt(mse)

                st.write("📊 Model Evaluation:")
                st.write(f"Mean Absolute Error (MAE): {mae:.2f}")
                st.write(f"Mean Squared Error (MSE): {mse:.2f}")
                st.write(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
            except Exception as e:
                st.error(f"Error during evaluation: {e}")
        else:
            st.error("Model not trained. Please train the model before evaluation.")

    def forecast(self, days_ahead):
        """
        Predict sales for a given number of days ahead.
        """
        if self.X_train is not None:
            try:
                max_days = self.X_train['Days'].max()
                future_days = np.array([max_days + i for i in range(1, days_ahead + 1)]).reshape(-1, 1)
                predictions = self.model.predict(future_days)

                forecast_df = pd.DataFrame({
                    'Days Ahead': range(1, days_ahead + 1),
                    'Predicted Sales': predictions
                })

                st.write("🔮 Forecast completed:")
                st.dataframe(forecast_df)
                return forecast_df
            except Exception as e:
                st.error(f"Error during forecasting: {e}")
        else:
            st.error("Model not trained. Please train the model before forecasting.")

    def plot_forecast(self, product_name, forecast_df):
        """
        Plot historical sales data and forecasted sales.
        """
        if self.data is not None and not forecast_df.empty:
            try:
                # Get product-specific data
                product_data = self.data[self.data['Product'] == product_name]
                
                # Plot the historical sales data
                plt.figure(figsize=(10, 6))
                plt.plot(product_data['Date'], product_data['Sales'], label='Historical Sales', color='blue')

                # Generate forecast dates
                forecast_dates = pd.date_range(start=product_data['Date'].max(), periods=len(forecast_df) + 1, freq='D')[1:]
                
                # Plot the forecasted sales
                plt.plot(forecast_dates, forecast_df['Predicted Sales'], label='Forecasted Sales', color='red', linestyle='--')

                # Add labels, title, and grid
                plt.xlabel('Date')
                plt.ylabel('Sales')
                plt.title(f'Sales Forecast for {product_name}')
                plt.legend()
                plt.grid(True)
                plt.xticks(rotation=45)
                plt.tight_layout()

                st.pyplot(plt)  # Display the plot in Streamlit
            except Exception as e:
                st.error(f"Error during plotting: {e}")
        else:
            st.error("No valid data or forecast to plot.")

# Main streamlit interface to interact with
def main():
    st.title('Sales Forecasting Tool')

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload a CSV file", type=['csv'])
    
    tool = DemandForecastingTool()

    if uploaded_file:
        tool.load_data(uploaded_file)
        
        product_name = st.selectbox("Select a product", tool.data['Product'].unique())
        
        if product_name:
            tool.preprocess_data(product_name)
        
        if st.button("Train Model"):
            tool.train_model()
        
        if st.button("Evaluate Model"):
            tool.evaluate_model()
        
        days_ahead = st.number_input("Days Ahead for Forecast", min_value=1, max_value=30, value=7)
        if st.button("Forecast"):
            forecast_df = tool.forecast(days_ahead)
            if forecast_df is not None:
                tool.plot_forecast(product_name, forecast_df)

if __name__ == "__main__":
    main()
