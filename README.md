# Retail Inventory Intelligence & Sales Analytics

This project started with a simple question: what can sales and inventory data tell us about how a retail business is performing?

I used Python to generate a retail dataset and Power BI to explore sales trends, product profitability, inventory levels, and warehouse performance. The aim was to connect the numbers to practical questions about product performance and stock management.

## Project at a Glance

- 240 products across 8 categories
- 400,000 sales transactions covering 2024 and 2025
- 3,600 inventory records across 15 warehouses
- 30 suppliers
- 3-page Power BI dashboard

The dataset is synthetic and was created for this project.

## Tools Used

- **Python, Pandas and NumPy** — data generation and validation
- **Power BI** — dashboard development and data visualization
- **DAX** — KPI calculations and analytical measures
- **Git and GitHub** — version control

## Business Questions I Explored

### 1. Which products and categories generate the most revenue?

I compared revenue across product categories and individual products. The dashboard includes revenue by category and a Top 10 Products by Revenue chart, making it easier to see how sales are distributed across the product range.

### 2. Are the products generating the most revenue also profitable?

Revenue alone doesn't show how much a business earns after product costs. I created DAX measures for gross profit and profit margin, then compared profitability across categories and examined monthly gross profit trends.

### 3. Which products may need replenishment?

I compared closing stock with the reorder point for each inventory record. Products at or below their reorder point were counted as requiring attention. I also calculated the percentage of distinct products at risk within each warehouse.

Reaching a reorder point does not necessarily mean a product is already out of stock; it indicates that replenishment may need to be considered.

### 4. How is inventory value distributed across categories and warehouses?

I calculated inventory value using closing stock multiplied by unit cost. I then compared inventory value across product categories and warehouses, including a matrix that breaks down value by warehouse and inventory status.

### 5. Do warehouses with higher inventory value also have higher stock risk?

I used a scatter chart to compare inventory value against stock risk for each warehouse, with units sold providing additional context. Reference lines help separate different combinations of inventory value and stock risk so that warehouses can be compared more easily.

These lines are analytical reference points, not official business risk limits.

### 6. How can the analysis be presented in one report?

I organized the report into three pages so that overall performance, sales analysis, and inventory operations could be examined separately. KPI cards, charts, a matrix, DAX measures, and Power BI bookmarks make the report easier to navigate and compare.

## Power BI Dashboard

### 1. Executive Overview

A summary of overall sales and inventory performance.

- Total revenue
- Total units sold
- Total inventory value
- Total products
- Products requiring reorder
- Monthly revenue and units sold
- Inventory status distribution
- Stock risk by warehouse

### 2. Sales & Product Performance

A closer look at sales contribution and profitability.

- Revenue by category
- Top 10 products by revenue
- Monthly gross profit
- Profit margin by category

### 3. Inventory & Operations

A comparison of inventory levels, stock risk, and warehouse performance.

- Inventory turnover by warehouse
- Inventory value by category
- Warehouse inventory value versus stock risk
- Inventory value by warehouse and inventory status

### Interactive Features

I used DAX measures to calculate the main KPIs and Power BI bookmarks to switch between report views where configured. The scatter chart includes reference lines to help compare warehouse performance, while the matrix provides a more detailed breakdown of inventory value and status.

## Data Preparation with Python

I wrote three scripts to generate the datasets.

| Script | What it does |
|---|---|
| `generate_master_data.py` | Generates product, supplier, and warehouse data |
| `generate_inventory_data.py` | Creates inventory records for product and warehouse combinations |
| `generate_sales_data.py` | Generates sales transactions across the date range |

The scripts include checks for missing values, duplicate identifiers, and inventory calculations. The inventory dataset contains one record for each product–warehouse combination.

## Dataset Details

| Dataset | Records | Description |
|---|---:|---|
| Products | 240 | Product details, categories, and pricing |
| Inventory | 3,600 | Stock records across products and warehouses |
| Sales | 400,000 | Sales transactions from 2024–2025 |
| Suppliers | 30 | Supplier details |
| Warehouses | 15 | Warehouse locations and capacity |

All records were generated for this project. They do not represent transactions or performance data from a real retailer, so the results should be interpreted within the context of the synthetic dataset.

## Project Structure

```text
Retail-Inventory-Intelligence/
├── Data/
│   ├── inventory.csv
│   ├── products.csv
│   ├── sales.csv
│   ├── suppliers.csv
│   └── warehouses.csv
├── Power BI/
│   └── Retail_Analysis.pbix
├── Python/
│   ├── generate_master_data.py
│   ├── generate_inventory_data.py
│   └── generate_sales_data.py
├── .gitignore
└── README.md
```

## Running the Project

The generated CSV files are already included, so you can open the Power BI report without generating the data again.

To regenerate the datasets, install Python and the required libraries:

```bash
pip install pandas numpy
```

Run the scripts from the project root in this order:

```bash
python Python/generate_master_data.py
python Python/generate_inventory_data.py
python Python/generate_sales_data.py
```

Open `Power BI/Retail_Analysis.pbix` in Power BI Desktop to explore the dashboard.

## What I Learned

This project gave me practice in generating related datasets, checking data consistency, creating DAX measures, and designing a report around specific business questions. It also helped me understand the difference between looking at sales figures in isolation and examining sales alongside profitability and inventory conditions.

## Author

**Naveen Sharma**  
B.Tech — Computer Science & Engineering  
Interested in Data Analytics and Business Intelligence
