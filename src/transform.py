import pandas as pd
from sqlalchemy import create_engine
from src.config import DATABASE_URL


# Connect to PostgreSQL
engine = create_engine(DATABASE_URL)


# Load raw data
query = """
SELECT *
FROM raw.online_retail;
"""

df = pd.read_sql(query, engine)


# Standardize column names
df.columns = [
    "invoice_no",
    "stock_code",
    "description",
    "quantity",
    "invoice_date",
    "unit_price",
    "customer_id",
    "country"
]


print("Original rows:", len(df))


# Remove exact duplicate rows
df = df.drop_duplicates()

print("Rows after removing duplicates:", len(df))


# Remove rows with missing description
df = df.dropna(subset=["description"])

print("Rows after removing missing descriptions:", len(df))


# Convert customer_id to nullable integer
df["customer_id"] = df["customer_id"].astype("Int64")


# Create total sales column
df["total_sales"] = df["quantity"] * df["unit_price"]


# Remove rows with invalid quantity
df = df[df["quantity"] > 0]


# Remove rows with invalid unit price
df = df[df["unit_price"] > 0]


print("Rows after cleaning:", len(df))


# Display final information
print("\nFinal columns:")
print(df.columns.tolist())


print("\nFinal NULL values:")
print(df.isnull().sum())


# Load cleaned data into PostgreSQL
df.to_sql(
    "online_retail_clean",
    engine,
    schema="clean",
    if_exists="append",
    index=False
)


print("\nCleaned data loaded successfully into clean.online_retail_clean")