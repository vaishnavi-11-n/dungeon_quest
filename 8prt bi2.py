import pandas as pd
import matplotlib.pyplot as plt

products = pd.read_csv("sales_data.csv")
monthly = pd.read_csv("monthly_sales.csv")

plt.figure(figsize=(8, 8))
plt.pie(
    products["Sales"],
    labels=products["Product"],
    autopct="%1.5f%%",
    startangle=90
)
plt.title("Sales distribution by product")
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(
    monthly["Month"],
    monthly["Sales"],
    marker="o",
    linewidth=2,
    color="red"
    )

plt.title("Sales Trend Line")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.grid(True, linestyle="==", alpha=0.6)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
plt.bar(
    monthly["month"],
    monthly["sales"]
    
)

plt.title("Sales Column Chart")
plt.xlabel("month")
plt.ylabel("sales")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()
