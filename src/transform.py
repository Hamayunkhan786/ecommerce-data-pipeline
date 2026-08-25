import pandas as pd


def transform(data):
    required_columns = [
        "invoice_no",
        "stock_code",
        "description",
        "quantity",
        "invoice_date",
        "unit_price",
        "customer_id",
        "country",
    ]
    missing_columns = set(required_columns) - set(data.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    clean_data = data[required_columns].copy()
    clean_data = clean_data.drop_duplicates()
    clean_data = clean_data.dropna(subset=["description"])
    clean_data["customer_id"] = clean_data["customer_id"].astype("Int64")
    clean_data["total_sales"] = clean_data["quantity"] * clean_data["unit_price"]
    clean_data = clean_data[clean_data["quantity"] > 0]
    clean_data = clean_data[clean_data["unit_price"] > 0]
    clean_data["invoice_date"] = pd.to_datetime(clean_data["invoice_date"])

    print(f"Rows after cleaning: {len(clean_data)}")
    return clean_data