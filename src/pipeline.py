import subprocess
import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

try:
    from src.config import DATABASE_URL
    from src.extract import extract
    from src.load import load_clean, load_raw
    from src.transform import transform
except ModuleNotFoundError:
    from config import DATABASE_URL
    from extract import extract
    from load import load_clean, load_raw
    from transform import transform


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DBT_PROJECT_DIR = PROJECT_ROOT / "ecommerce_dbt"
OUTPUT_DIR = PROJECT_ROOT / "output"


def load_view(view_name, engine):
    query = f"SELECT * FROM analytics.{view_name};"
    return pd.read_sql(query, engine)


def main():
    print("Starting e-commerce pipeline...\n")
    OUTPUT_DIR.mkdir(exist_ok=True)
    engine = create_engine(DATABASE_URL)

    raw_data = extract()
    clean_data = transform(raw_data)
    load_raw(raw_data, engine)
    load_clean(clean_data, engine)

    subprocess.run(
        [sys.executable, "-m", "dbt.cli.main", "run", "--project-dir", str(DBT_PROJECT_DIR)],
        cwd=PROJECT_ROOT,
        check=True,
    )
    subprocess.run(
        [sys.executable, "-m", "dbt.cli.main", "test", "--project-dir", str(DBT_PROJECT_DIR)],
        cwd=PROJECT_ROOT,
        check=True,
    )

    # -------------------------
    # KPI SUMMARY
    # -------------------------
    kpi = load_view("kpi_summary", engine)

    print("===== KPI SUMMARY =====")
    print(kpi.to_string(index=False))

    kpi.to_csv(
        OUTPUT_DIR / "kpi_summary.csv",
        index=False
    )

    # -------------------------
    # MONTHLY SALES
    # -------------------------
    monthly_sales = load_view("monthly_sales", engine)

    print("\n===== MONTHLY SALES =====")
    print(monthly_sales.head(10).to_string(index=False))

    monthly_sales.to_csv(
        OUTPUT_DIR / "monthly_sales.csv",
        index=False
    )

    # -------------------------
    # PRODUCT SALES
    # -------------------------
    product_sales = load_view("product_sales", engine)

    print("\n===== TOP PRODUCTS =====")

    top_products = (
        product_sales
        .sort_values("revenue", ascending=False)
        .head(10)
    )

    print(top_products.to_string(index=False))

    product_sales.to_csv(
        OUTPUT_DIR / "product_sales.csv",
        index=False
    )

    # -------------------------
    # COUNTRY SALES
    # -------------------------
    country_sales = load_view("country_sales", engine)

    print("\n===== TOP COUNTRIES =====")

    top_countries = (
        country_sales
        .sort_values("revenue", ascending=False)
        .head(10)
    )

    print(top_countries.to_string(index=False))

    country_sales.to_csv(
        OUTPUT_DIR / "country_sales.csv",
        index=False
    )

    # -------------------------
    # CUSTOMER SALES
    # -------------------------
    customer_sales = load_view("customer_sales", engine)

    print("\n===== TOP CUSTOMERS =====")

    top_customers = (
        customer_sales
        .sort_values("revenue", ascending=False)
        .head(10)
    )

    print(top_customers.to_string(index=False))

    customer_sales.to_csv(
        OUTPUT_DIR / "customer_sales.csv",
        index=False
    )

    print("\nAll analytics files exported successfully!")


if __name__ == "__main__":
    main()