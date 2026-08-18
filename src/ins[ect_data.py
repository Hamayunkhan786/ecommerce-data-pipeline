import pandas as pd
from sqlalchemy import create_engine
from src.config import DATABASE_URL


# Connect to PostgreSQL
engine = create_engine(DATABASE_URL)


# Load the raw data
query = """
SELECT *
FROM raw.online_retail;
"""

df = pd.read_sql(query, engine)


# Basic information
print("Dataset loaded successfully!")
print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))


# Column names
print("\nColumn names:")
print(df.columns.tolist())


# Data types
print("\nData types:")
print(df.dtypes)


# NULL values
print("\nNULL values:")
print(df.isnull().sum())


# Duplicate rows
print("\nDuplicate rows:")
print(df.duplicated().sum())