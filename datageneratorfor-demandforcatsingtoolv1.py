import pandas as pd
import numpy as np

# Parameters
start_date = "2020-01-01"
end_date = "2023-12-31"
products = ["Product_A", "Product_B", "Product_C"]
n_products = len(products)

# Generate date range
dates = pd.date_range(start=start_date, end=end_date)

# Create synthetic sales data
data = []
np.random.seed(42)

for product in products:
    sales_trend = np.linspace(50, 500, len(dates))  # Trend line
    seasonal_effect = 50 * np.sin(np.linspace(0, 6 * np.pi, len(dates)))  # Sinusoidal seasonality
    random_noise = np.random.normal(scale=30, size=len(dates))  # Random noise

    sales = np.maximum(0, sales_trend + seasonal_effect + random_noise)  # Sales can't be negative
    for date, sale in zip(dates, sales):
        data.append({"Date": date, "Product": product, "Sales": sale})

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("synthetic_sales_data.csv", index=False)

print("Synthetic dataset created and saved as 'synthetic_sales_data.csv'.")
