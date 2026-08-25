from io import StringIO

import pandas as pd
from sqlalchemy import create_engine, text

try:
    from src.config import DATABASE_URL
except ModuleNotFoundError:
    from config import DATABASE_URL


def _copy_dataframe(data, table_name, schema, engine, columns, table_definition):
    csv_data = StringIO()
    data.to_csv(csv_data, index=False, header=False, na_rep="\\N")
    csv_data.seek(0)

    connection = engine.raw_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
        cursor.execute(f"DROP TABLE IF EXISTS {schema}.{table_name}")
        cursor.execute(
            f"CREATE TABLE {schema}.{table_name} ({table_definition})"
        )
        cursor.copy_expert(
            f"COPY {schema}.{table_name} ({', '.join(columns)}) "
            "FROM STDIN WITH (FORMAT CSV, NULL '\\N')",
            csv_data,
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
    print(f"Loaded {len(data)} rows into {schema}.{table_name}")


def load_raw(data, engine=None):
    database_engine = engine or create_engine(DATABASE_URL)
    staging_table = "online_retail_load"
    columns = [
        "invoice_no", "stock_code", "description", "quantity",
        "invoice_date", "unit_price", "customer_id", "country",
    ]
    table_definition = (
        "invoice_no TEXT, stock_code TEXT, description TEXT, quantity INTEGER, "
        "invoice_date TIMESTAMP, unit_price NUMERIC(12, 4), "
        "customer_id INTEGER, country TEXT"
    )
    _copy_dataframe(
        data, staging_table, "raw", database_engine, columns, table_definition
    )
    with database_engine.begin() as connection:
        connection.execute(
            text(
                "CREATE TABLE IF NOT EXISTS raw.online_retail "
                "(LIKE raw.online_retail_load INCLUDING ALL)"
            )
        )
        connection.execute(text("DELETE FROM raw.online_retail"))
        connection.execute(
            text(
                "INSERT INTO raw.online_retail "
                "SELECT invoice_no, stock_code, description, quantity, "
                "invoice_date, unit_price, customer_id, country "
                "FROM raw.online_retail_load"
            )
        )
        connection.execute(text("DROP TABLE raw.online_retail_load"))
    print("Raw data loaded into raw.online_retail")


def load_clean(data, engine=None):
    database_engine = engine or create_engine(DATABASE_URL)
    staging_table = "online_retail_clean_load"
    columns = [
        "invoice_no", "stock_code", "description", "quantity",
        "invoice_date", "unit_price", "customer_id", "country", "total_sales",
    ]
    table_definition = (
        "invoice_no TEXT, stock_code TEXT, description TEXT, quantity INTEGER, "
        "invoice_date TIMESTAMP, unit_price NUMERIC(12, 4), "
        "customer_id INTEGER, country TEXT, total_sales NUMERIC(14, 4)"
    )
    _copy_dataframe(
        data, staging_table, "clean", database_engine, columns, table_definition
    )
    with database_engine.begin() as connection:
        connection.execute(
            text(
                "CREATE TABLE IF NOT EXISTS clean.online_retail_clean "
                "(LIKE clean.online_retail_clean_load INCLUDING ALL)"
            )
        )
        connection.execute(text("DELETE FROM clean.online_retail_clean"))
        connection.execute(
            text(
                "INSERT INTO clean.online_retail_clean "
                "SELECT * FROM clean.online_retail_clean_load"
            )
        )
        connection.execute(text("DROP TABLE clean.online_retail_clean_load"))
    print("Cleaned data loaded into clean.online_retail_clean")