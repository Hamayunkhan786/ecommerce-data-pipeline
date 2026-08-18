import pandas as pd
from sqlalchemy import create_engine
from src.config import DATABASE_URL


# Create PostgreSQL connection
engine = create_engine(DATABASE_URL)


# Load the raw data
query = """
SELECT *
FROM raw.online_retail;
"""

df = pd.read_sql(query, engine)


# Convert column names to lowercase
df.columns = df.columns.str.lower()


print("Dataset loaded successfully!")
print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))


print("\nColumn names:")
print(df.columns.tolist())


print("\nData types:")
print(df.dtypes)


print("\nNULL values:")
print(df.isnull().sum())


print("\nDuplicate rows:")
print(df.duplicated().sum())