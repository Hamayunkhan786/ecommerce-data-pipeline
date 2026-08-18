import pandas as pd
from sqlalchemy import create_engine
from src.config import DATABASE_URL


# Create PostgreSQL connection
engine = create_engine(DATABASE_URL)


# SQL query
query = """
SELECT *
FROM raw.online_retail;
"""


# Read the complete table into Pandas
df = pd.read_sql(query, engine)


# Show the first 5 rows

# Show number of rows
print("\nRows extracted:", len(df))

# Show column names
print("\nColumns:")
print(df.columns.tolist())
