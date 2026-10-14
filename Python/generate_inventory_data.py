import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)



# LOAD MASTER DATA


products = pd.read_csv(DATA_DIR / "products.csv")
warehouses = pd.read_csv(DATA_DIR / "warehouses.csv")



# INVENTORY GENERATION


inventory_records = []

inventory_id = 1


for _, product in products.iterrows():

    product_id = product["product_id"]
    unit_cost = product["unit_cost"]

    for _, warehouse in warehouses.iterrows():

        warehouse_id = warehouse["warehouse_id"]

        # --------------------------------------
        # Opening stock
        # --------------------------------------

        opening_stock = np.random.randint(100, 5000)

        # --------------------------------------
        # Stock received
        # --------------------------------------

        stock_received = np.random.randint(0, 3000)

        # --------------------------------------
        # Maximum available stock
        # --------------------------------------

        available_stock = opening_stock + stock_received

        # --------------------------------------
        # Units sold
        #
        # Keep units_sold <= available stock
        # so closing stock can never become negative.
        # --------------------------------------

        units_sold = np.random.randint(
            0,
            max(1, int(available_stock * 0.90))
        )

        # --------------------------------------
        # Closing stock
        # --------------------------------------

        closing_stock = (
            opening_stock
            + stock_received
            - units_sold
        )

        # --------------------------------------
        # Safety stock
        # --------------------------------------

        safety_stock = np.random.randint(100, 1000)

        # --------------------------------------
        # Reorder point
        # --------------------------------------

        reorder_point = np.random.randint(
            200,
            1500
        )

        # --------------------------------------
        # Stockout days
        # --------------------------------------

        if closing_stock == 0:
            stockout_days = np.random.randint(1, 15)
        else:
            stockout_days = 0

        # --------------------------------------
        # Inventory value
        # --------------------------------------

        inventory_value = round(
            closing_stock * unit_cost,
            2
        )

        # --------------------------------------
        # Days of inventory
        #
        # Based on current stock and units sold.
        # --------------------------------------

        if units_sold > 0:

            days_of_inventory = round(
                closing_stock / units_sold * 30,
                2
            )

        else:

            days_of_inventory = 999.0

        # --------------------------------------
        # Inventory status
        # --------------------------------------

        if closing_stock == 0:

            inventory_status = "Stockout"

        elif closing_stock <= reorder_point:

            inventory_status = "Reorder Required"

        elif closing_stock > safety_stock * 2:

            inventory_status = "Overstocked"

        else:

            inventory_status = "Healthy"

        # --------------------------------------
        # Store record
        # --------------------------------------

        inventory_records.append({

            "inventory_id": f"INV{inventory_id:06d}",

            "product_id": product_id,

            "warehouse_id": warehouse_id,

            "opening_stock": opening_stock,

            "stock_received": stock_received,

            "units_sold": units_sold,

            "closing_stock": closing_stock,

            "safety_stock": safety_stock,

            "reorder_point": reorder_point,

            "stockout_days": stockout_days,

            "inventory_value": inventory_value,

            "days_of_inventory": days_of_inventory,

            "inventory_status": inventory_status

        })

        inventory_id += 1



# CREATE DATAFRAME


inventory_df = pd.DataFrame(inventory_records)



# SAVE DATA


inventory_df.to_csv(
    DATA_DIR / "inventory.csv",
    index=False
)


# VALIDATION


print("\n" + "=" * 60)
print("INVENTORY DATA GENERATION COMPLETED")
print("=" * 60)


print(
    f"\nInventory records: "
    f"{len(inventory_df):,}"
)

print(
    f"Unique products: "
    f"{inventory_df['product_id'].nunique():,}"
)

print(
    f"Unique warehouses: "
    f"{inventory_df['warehouse_id'].nunique():,}"
)

print(
    f"Total closing stock: "
    f"{inventory_df['closing_stock'].sum():,}"
)

print(
    f"Total inventory value: "
    f"₹{inventory_df['inventory_value'].sum():,.2f}"
)


# INVENTORY STATUS


print("\nInventory status:")

print(
    inventory_df["inventory_status"].value_counts()
)



# STATUS PERCENTAGES


print("\nInventory status percentages:")

print(
    inventory_df["inventory_status"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)


# MISSING VALUES


print("\nMissing values:")

print(
    inventory_df.isnull().sum()
)


# DUPLICATE IDS


print("\nDuplicate Inventory IDs:")

print(
    inventory_df["inventory_id"].duplicated().sum()
)



# CLOSING STOCK VALIDATION


calculated_closing_stock = (
    inventory_df["opening_stock"]
    + inventory_df["stock_received"]
    - inventory_df["units_sold"]
)

closing_stock_errors = (
    inventory_df["closing_stock"]
    != calculated_closing_stock
).sum()

print("\nClosing stock calculation errors:")

print(closing_stock_errors)


# INVENTORY VALUE VALIDATION


inventory_check = inventory_df.merge(
    products[["product_id", "unit_cost"]],
    on="product_id",
    how="left"
)

calculated_inventory_value = (
    inventory_check["closing_stock"]
    * inventory_check["unit_cost"]
)

inventory_value_errors = (
    (
        inventory_check["inventory_value"]
        - calculated_inventory_value
    ).abs() > 0.01
).sum()

print("\nInventory value calculation errors:")

print(inventory_value_errors)



# SAMPLE RECORDS

print("\nSample records:")

print(
    inventory_df.head(10)
)


# FINAL VALIDATION


print("\n" + "=" * 60)
print("FINAL VALIDATION")
print("=" * 60)


if (
    inventory_df.isnull().sum().sum() == 0
    and inventory_df["inventory_id"].duplicated().sum() == 0
    and closing_stock_errors == 0
    and inventory_value_errors == 0
):

    print("INVENTORY DATA VALIDATION PASSED")

else:

    print("INVENTORY DATA VALIDATION FAILED")


print("\nInventory data saved to:")

print("data/inventory.csv")