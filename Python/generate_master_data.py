import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


# ==========================================
# 1. SUPPLIERS
# ==========================================

supplier_locations = [
    "Delhi", "Mumbai", "Kolkata", "Bengaluru",
    "Chennai", "Hyderabad", "Pune", "Ahmedabad",
    "Jaipur", "Lucknow", "Surat", "Indore"
]

suppliers = []

for i in range(1, 31):

    # Less reliable suppliers
    if i <= 5:
        lead_time = np.random.randint(10, 18)
        rating = round(np.random.uniform(2.8, 3.6), 1)

    # Average suppliers
    elif i <= 20:
        lead_time = np.random.randint(5, 12)
        rating = round(np.random.uniform(3.5, 4.4), 1)

    # High-performing suppliers
    else:
        lead_time = np.random.randint(3, 8)
        rating = round(np.random.uniform(4.2, 5.0), 1)

    suppliers.append({
        "supplier_id": f"S{i:03d}",
        "supplier_name": f"Supplier {i:02d}",
        "location": np.random.choice(supplier_locations),
        "standard_lead_time_days": lead_time,
        "supplier_rating": rating
    })

suppliers_df = pd.DataFrame(suppliers)


# ==========================================
# 2. WAREHOUSES
# ==========================================

# IMPORTANT:
# Sales and inventory datasets use 15 warehouses.
# Therefore master data must also contain 15 warehouses.

warehouse_locations = [
    ("WH001", "North Distribution Center", "Delhi", "North"),
    ("WH002", "South Distribution Center", "Bengaluru", "South"),
    ("WH003", "East Distribution Center", "Kolkata", "East"),
    ("WH004", "West Distribution Center", "Mumbai", "West"),
    ("WH005", "Central Distribution Center", "Nagpur", "Central"),
    ("WH006", "Pune Distribution Center", "Pune", "West"),
    ("WH007", "Hyderabad Distribution Center", "Hyderabad", "South"),
    ("WH008", "Jaipur Distribution Center", "Jaipur", "North"),
    ("WH009", "Ahmedabad Distribution Center", "Ahmedabad", "West"),
    ("WH010", "Lucknow Distribution Center", "Lucknow", "North"),
    ("WH011", "Chennai Distribution Center", "Chennai", "South"),
    ("WH012", "Indore Distribution Center", "Indore", "Central"),
    ("WH013", "Surat Distribution Center", "Surat", "West"),
    ("WH014", "Patna Distribution Center", "Patna", "East"),
    ("WH015", "Bhopal Distribution Center", "Bhopal", "Central")
]

warehouses = []

for warehouse_id, name, city, region in warehouse_locations:

    warehouses.append({
        "warehouse_id": warehouse_id,
        "warehouse_name": name,
        "city": city,
        "region": region,
        "warehouse_capacity": np.random.randint(8000, 25000)
    })

warehouses_df = pd.DataFrame(warehouses)


# ==========================================
# 3. PRODUCTS
# ==========================================

product_catalog = {

    "Electronics": [
        "Wireless Mouse", "Keyboard", "Bluetooth Speaker",
        "Power Bank", "USB Cable", "Headphones",
        "Webcam", "Smart Watch", "Memory Card",
        "Laptop Stand"
    ],

    "Home Appliances": [
        "Electric Kettle", "Mixer Grinder", "Toaster",
        "Table Fan", "Iron", "Air Purifier",
        "Room Heater", "Hand Blender", "Coffee Maker",
        "Vacuum Cleaner"
    ],

    "Personal Care": [
        "Electric Trimmer", "Hair Dryer", "Face Wash",
        "Shampoo", "Body Lotion", "Face Cream",
        "Electric Toothbrush", "Hair Serum",
        "Sunscreen", "Hand Wash"
    ],

    "Grocery": [
        "Coffee", "Tea", "Biscuits", "Breakfast Cereal",
        "Cooking Oil", "Rice", "Pasta", "Spices",
        "Instant Noodles", "Dry Fruits"
    ],

    "Stationery": [
        "Notebook", "Pen Set", "Marker Set",
        "Stapler", "Calculator", "File Folder",
        "Drawing Book", "Highlighter Set",
        "Pencil Box", "Printer Paper"
    ],

    "Sports": [
        "Yoga Mat", "Football", "Cricket Bat",
        "Skipping Rope", "Dumbbells", "Tennis Racket",
        "Badminton Racket", "Sports Bottle",
        "Resistance Band", "Gym Gloves"
    ],

    "Clothing": [
        "T-Shirt", "Jeans", "Hoodie",
        "Sports Shoes", "Jacket", "Track Pants",
        "Casual Shirt", "Socks", "Cap",
        "Sweatshirt"
    ],

    "Home & Kitchen": [
        "Water Bottle", "Storage Box", "Frying Pan",
        "Dinner Set", "Kitchen Container", "Lunch Box",
        "Cutlery Set", "Mug Set", "Chopping Board",
        "Food Storage Jar"
    ]
}


# ==========================================
# 4. PRICE RANGES
# ==========================================

price_ranges = {

    "Electronics": (500, 12000),

    "Home Appliances": (800, 15000),

    "Personal Care": (100, 4000),

    "Grocery": (50, 2000),

    "Stationery": (30, 1500),

    "Sports": (200, 8000),

    "Clothing": (300, 6000),

    "Home & Kitchen": (100, 5000)
}


# ==========================================
# 5. GENERATE PRODUCTS
# ==========================================

products = []

product_id = 1

for category, product_names in product_catalog.items():

    for base_name in product_names:

        # Three variants for every product
        for variant in range(1, 4):

            min_price, max_price = price_ranges[category]

            unit_cost = round(
                np.random.uniform(
                    min_price,
                    max_price
                ),
                2
            )

            # Selling price is higher than unit cost
            markup = np.random.uniform(1.20, 1.70)

            selling_price = round(
                unit_cost * markup,
                2
            )

            supplier_id = np.random.choice(
                suppliers_df["supplier_id"]
            )

            products.append({

                "product_id":
                    f"P{product_id:04d}",

                "product_name":
                    f"{base_name} {variant}",

                "category":
                    category,

                "unit_cost":
                    unit_cost,

                "selling_price":
                    selling_price,

                "supplier_id":
                    supplier_id
            })

            product_id += 1


products_df = pd.DataFrame(products)


# ==========================================
# 6. SAVE CSV FILES
# ==========================================

suppliers_df.to_csv(
    DATA_DIR / "suppliers.csv",
    index=False
)

warehouses_df.to_csv(
    DATA_DIR / "warehouses.csv",
    index=False
)

products_df.to_csv(
    DATA_DIR / "products.csv",
    index=False
)


# ==========================================
# 7. VALIDATION
# ==========================================

print("\n" + "=" * 55)
print("MASTER DATA GENERATION COMPLETED")
print("=" * 55)


# ------------------------------------------
# Record counts
# ------------------------------------------

print("\n--- Record Counts ---")

print(f"Suppliers  : {len(suppliers_df)}")
print(f"Warehouses : {len(warehouses_df)}")
print(f"Products   : {len(products_df)}")


# ------------------------------------------
# Missing values
# ------------------------------------------

print("\n--- Missing Values ---")

print("\nSuppliers:")
print(suppliers_df.isnull().sum())

print("\nWarehouses:")
print(warehouses_df.isnull().sum())

print("\nProducts:")
print(products_df.isnull().sum())


# ------------------------------------------
# Duplicate IDs
# ------------------------------------------

print("\n--- Duplicate IDs ---")

supplier_duplicates = (
    suppliers_df["supplier_id"].duplicated().sum()
)

warehouse_duplicates = (
    warehouses_df["warehouse_id"].duplicated().sum()
)

product_duplicates = (
    products_df["product_id"].duplicated().sum()
)

print("Suppliers  :", supplier_duplicates)
print("Warehouses :", warehouse_duplicates)
print("Products   :", product_duplicates)


# ------------------------------------------
# Product categories
# ------------------------------------------

print("\n--- Product Categories ---")

print(
    products_df["category"]
    .value_counts()
    .sort_index()
)


# ------------------------------------------
# Warehouse regions
# ------------------------------------------

print("\n--- Warehouse Regions ---")

print(
    warehouses_df["region"]
    .value_counts()
    .sort_index()
)


# ------------------------------------------
# Supplier rating summary
# ------------------------------------------

print("\n--- Supplier Rating Summary ---")

print(
    suppliers_df["supplier_rating"]
    .describe()
)


# ------------------------------------------
# Sample products
# ------------------------------------------

print("\n--- Sample Products ---")

print(
    products_df.head()
)


# ------------------------------------------
# Sample suppliers
# ------------------------------------------

print("\n--- Sample Suppliers ---")

print(
    suppliers_df.head()
)


# ------------------------------------------
# Sample warehouses
# ------------------------------------------

print("\n--- Sample Warehouses ---")

print(
    warehouses_df.head()
)


# ==========================================
# 8. FINAL VALIDATION
# ==========================================

print("\n--- Final Validation ---")

if (
    len(suppliers_df) == 30
    and len(warehouses_df) == 15
    and len(products_df) == 240
    and supplier_duplicates == 0
    and warehouse_duplicates == 0
    and product_duplicates == 0
    and suppliers_df.isnull().sum().sum() == 0
    and warehouses_df.isnull().sum().sum() == 0
    and products_df.isnull().sum().sum() == 0
):
    print("MASTER DATA VALIDATION PASSED")
else:
    print("MASTER DATA VALIDATION FAILED")


print("\nCSV files saved inside the 'data' folder.")

print("\nFiles created:")
print("data/suppliers.csv")
print("data/warehouses.csv")
print("data/products.csv")