import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# Load CSV Files
# ==========================================

# Product-wise sales
products = pd.read_csv("sales_data.csv")

# Monthly sales data
monthly = pd.read_csv("monthly_sales.csv")

# ==========================================
# Pie Chart - Product Distribution
# ==========================================

plt.figure(figsize=(8, 8))
plt.pie(
    products["Sales"],
    labels=products["Product"],
    autopct='%1.1f%%',
    startangle=90
)
plt.title("Sales Distribution by Product")
plt.tight_layout()
plt.show()
