import pandas as pd
from sqlalchemy import create_engine, text
from src.config import DATABASE_URL


# Create PostgreSQL connection
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


# Remove duplicates
df = df.drop_duplicates()


# Remove missing descriptions
df = df.dropna(subset=["description"])


# Convert customer_id to nullable integer
df["customer_id"] = df["customer_id"].astype("Int64")


# Create total sales
df["total_sales"] = df["quantity"] * df["unit_price"]


# Remove invalid quantity
df = df[df["quantity"] > 0]


# Remove invalid unit price
df = df[df["unit_price"] > 0]


print("Clean rows:", len(df))


# Create clean schema
with engine.begin() as connection:
    connection.execute(text("CREATE SCHEMA IF NOT EXISTS clean"))


# Load data into PostgreSQL
df.to_sql(
    "online_retail_clean",
    engine,
    schema="clean",
    if_exists="replace",
    index=False
)


print("Data loaded successfully!")
print("Table: clean.online_retail_clean")