import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
from src.config import DATABASE_URL


# PostgreSQL connection
engine = create_engine(DATABASE_URL)


# Output folder
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def load_view(view_name):
    query = f"""
    SELECT *
    FROM analytics.{view_name};
    """

    return pd.read_sql(query, engine)


def main():

    print("Starting e-commerce analytics pipeline...\n")

    # -------------------------
    # KPI SUMMARY
    # -------------------------
    kpi = load_view("kpi_summary")

    print("===== KPI SUMMARY =====")
    print(kpi.to_string(index=False))

    kpi.to_csv(
        OUTPUT_DIR / "kpi_summary.csv",
        index=False
    )

    # -------------------------
    # MONTHLY SALES
    # -------------------------
    monthly_sales = load_view("monthly_sales")

    print("\n===== MONTHLY SALES =====")
    print(monthly_sales.head(10).to_string(index=False))

    monthly_sales.to_csv(
        OUTPUT_DIR / "monthly_sales.csv",
        index=False
    )

    # -------------------------
    # PRODUCT SALES
    # -------------------------
    product_sales = load_view("product_sales")

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
    country_sales = load_view("country_sales")

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
    customer_sales = load_view("customer_sales")

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