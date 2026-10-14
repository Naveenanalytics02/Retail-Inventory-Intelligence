import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

DATA_DIR = Path("data")

# -----------------------------------
# LOAD MASTER DATA
# -----------------------------------

products = pd.read_csv(DATA_DIR / "products.csv")
warehouses = pd.read_csv(DATA_DIR / "warehouses.csv")

# -----------------------------------
# SETTINGS
# -----------------------------------

START_DATE = "2024-01-01"
END_DATE = "2025-12-31"

TARGET_TRANSACTIONS = 400_000

dates = pd.date_range(
    START_DATE,
    END_DATE,
    freq="D"
)

# -----------------------------------
# PRODUCT DEMAND PROFILE
# -----------------------------------

# Determines how frequently products appear,
# not huge quantities per transaction.
products["demand_score"] = np.random.gamma(
    shape=2.0,
    scale=1.0,
    size=len(products)
)

# High-demand products
high_demand = np.random.choice(
    products.index,
    size=40,
    replace=False
)

products.loc[
    high_demand,
    "demand_score"
] *= np.random.uniform(
    1.5,
    2.2,
    size=len(high_demand)
)

# Low-demand products
remaining = products.index.difference(high_demand)

low_demand = np.random.choice(
    remaining,
    size=50,
    replace=False
)

products.loc[
    low_demand,
    "demand_score"
] *= np.random.uniform(
    0.4,
    0.7,
    size=len(low_demand)
)

# -----------------------------------
# PRODUCT SELECTION WEIGHTS
# -----------------------------------

product_weights = products["demand_score"].values

product_weights = (
    product_weights /
    product_weights.sum()
)

# -----------------------------------
# WAREHOUSE WEIGHTS
# -----------------------------------

warehouse_weights = np.random.uniform(
    0.7,
    1.3,
    size=len(warehouses)
)

warehouse_weights = (
    warehouse_weights /
    warehouse_weights.sum()
)

# -----------------------------------
# GENERATE TRANSACTIONS
# -----------------------------------

print("Generating sales transactions...")

sale_dates = np.random.choice(
    dates,
    size=TARGET_TRANSACTIONS
)

product_indices = np.random.choice(
    len(products),
    size=TARGET_TRANSACTIONS,
    p=product_weights
)

warehouse_indices = np.random.choice(
    len(warehouses),
    size=TARGET_TRANSACTIONS,
    p=warehouse_weights
)

# -----------------------------------
# CREATE BASE DATAFRAME
# -----------------------------------

sales_df = pd.DataFrame({
    "sale_date": sale_dates,

    "product_id": products.iloc[
        product_indices
    ]["product_id"].values,

    "warehouse_id": warehouses.iloc[
        warehouse_indices
    ]["warehouse_id"].values
})

# -----------------------------------
# DATE FEATURES
# -----------------------------------

sales_df["day_of_week"] = (
    sales_df["sale_date"].dt.dayofweek
)

sales_df["month"] = (
    sales_df["sale_date"].dt.month
)

# -----------------------------------
# WEEKEND EFFECT
# -----------------------------------

weekend_factor = np.where(
    sales_df["day_of_week"] >= 5,
    1.10,
    1.00
)

# -----------------------------------
# SEASONAL EFFECT
# -----------------------------------

seasonal_factor = np.select(
    [
        sales_df["month"].isin([10, 11, 12]),
        sales_df["month"].isin([6, 7, 8])
    ],
    [
        1.20,
        1.08
    ],
    default=1.00
)

# -----------------------------------
# QUANTITY SOLD
# -----------------------------------

# Normal retail order quantity.
# Most records will contain a few units.
random_factor = np.random.uniform(
    0.75,
    1.25,
    size=TARGET_TRANSACTIONS
)

expected_quantity = (
    3.0
    * weekend_factor
    * seasonal_factor
    * random_factor
)

quantity = np.random.poisson(
    expected_quantity
)

# Minimum 1 unit
quantity = np.maximum(quantity, 1)

# Prevent unrealistic very large quantities
quantity = np.minimum(quantity, 10)

sales_df["quantity_sold"] = quantity

# -----------------------------------
# SELLING PRICE
# -----------------------------------

sales_df["selling_price"] = products.iloc[
    product_indices
]["selling_price"].values

# Small realistic price variation
sales_df["selling_price"] *= np.random.uniform(
    0.97,
    1.03,
    size=TARGET_TRANSACTIONS
)

sales_df["selling_price"] = (
    sales_df["selling_price"].round(2)
)

# -----------------------------------
# REVENUE
# -----------------------------------

sales_df["revenue"] = (
    sales_df["quantity_sold"]
    * sales_df["selling_price"]
).round(2)

# -----------------------------------
# KEEP REQUIRED COLUMNS
# -----------------------------------

sales_df = sales_df[
    [
        "sale_date",
        "product_id",
        "warehouse_id",
        "quantity_sold",
        "selling_price",
        "revenue"
    ]
]

# Sort chronologically
sales_df = sales_df.sort_values(
    "sale_date"
).reset_index(drop=True)

# -----------------------------------
# SALE ID
# -----------------------------------

sales_df.insert(
    0,
    "sale_id",
    [
        f"SALE{i:07d}"
        for i in range(
            1,
            len(sales_df) + 1
        )
    ]
)

# -----------------------------------
# SAVE
# -----------------------------------

sales_df.to_csv(
    DATA_DIR / "sales.csv",
    index=False
)

# -----------------------------------
# VALIDATION
# -----------------------------------

print("\n" + "=" * 50)
print("SALES DATA GENERATION COMPLETED")
print("=" * 50)

print(
    f"\nTransactions: "
    f"{len(sales_df):,}"
)

print(
    f"Date range: "
    f"{sales_df['sale_date'].min().date()} "
    f"to "
    f"{sales_df['sale_date'].max().date()}"
)

print(
    f"Unique products: "
    f"{sales_df['product_id'].nunique()}"
)

print(
    f"Unique warehouses: "
    f"{sales_df['warehouse_id'].nunique()}"
)

print(
    f"Total units sold: "
    f"{sales_df['quantity_sold'].sum():,}"
)

print(
    f"Average units/transaction: "
    f"{sales_df['quantity_sold'].mean():.2f}"
)

print(
    f"Total revenue: "
    f"₹{sales_df['revenue'].sum():,.2f}"
)

print(
    f"Average transaction value: "
    f"₹{sales_df['revenue'].mean():,.2f}"
)

print("\nMissing values:")
print(sales_df.isnull().sum())

print(
    "\nDuplicate Sale IDs:",
    sales_df["sale_id"].duplicated().sum()
)

print("\nSample records:")
print(sales_df.head())

print("\nSales data saved to:")
print("data/sales.csv")