# E-Commerce Data Pipeline

This project builds a PostgreSQL-backed e-commerce analytics pipeline using Python, dbt, and a retail dataset. It extracts raw online retail data, cleans it, loads it into PostgreSQL, and models sales, customer, product, and date dimensions in dbt.

## Overview

The workflow is designed to:

- Load raw transaction data from the Excel source file in `data/`
- Clean and validate the retail dataset in Python
- Load transformed data into PostgreSQL schemas such as `raw` and `clean`
- Build reusable dbt models for analytics
- Run data quality tests and produce business metrics

## Project structure

- `data/` - source data files, including the Excel workbook
- `src/` - Python data pipeline scripts
- `sql/` - SQL scripts for database creation and analytical queries
- `models/` - SQL-based analytics models outside dbt
- `output/` - generated CSV summary outputs
- `ecommerce_dbt/` - dbt project with staging, intermediate, marts, seeds, snapshots, macros, and tests
- `tests/` - Python unit tests for the pipeline
- `logs/` - dbt execution logs

## Main components

### Python pipeline

Files in `src/` handle loading and transformation:

- `src/config.py` - environment configuration and database URL
- `src/extract.py` - reads raw data
- `src/load.py` - loads cleaned data into PostgreSQL
- `src/transform.py` - applies cleaning and validation rules
- `src/pipeline.py` - orchestrates the end-to-end flow
- `src/test_connection.py` - verifies database connectivity

### dbt project

The dbt project in `ecommerce_dbt/` contains:

- `models/staging/` - staging layer from raw PostgreSQL data
- `models/intermediate/` - intermediate sales logic
- `models/marts/` - final sales fact model and downstream reporting tables
- `models/analytics/` - dimensions such as date, customer, and product
- `macros/` - reusable SQL macros
- `seeds/` - lookup data such as country-to-region mappings
- `snapshots/` - historical tracking for raw retail data

## Setup

1. Create and activate a virtual environment.
2. Install the requirements:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure your PostgreSQL credentials in a `.env` file, for example:

   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=ecommerce_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```

4. Make sure PostgreSQL is running and the database exists.

## Running the pipeline

From the project root:

```bash
python src/pipeline.py
```

This runs the cleaning and loading flow for the online retail dataset.

## dbt commands

Activate the project virtual environment, then run:

```bash
cd ecommerce_dbt
dbt debug
dbt run
dbt test
```

You can also run specific dbt selections:

```bash
dbt run --select dim_date
dbt test --select fact_sales
```

## Testing

Python tests can be run with:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

The project includes 17 Python unit tests and 16 dbt data tests, covering data validation, clean data quality, and analytics integrity.

## Outputs

The project generates summary analysis files under `output/`, including:

- `country_sales.csv`
- `customer_sales.csv`
- `monthly_sales.csv`
- `product_sales.csv`
- `kpi_summary.csv`

## Database design

The SQL scripts in `sql/` create the main PostgreSQL structures, including:

- database creation
- schema creation
- raw table definitions
- clean table definitions
- analytics queries

## Notes

- The project uses PostgreSQL as the warehouse layer.
- The dbt models transform raw transactional data into analytics-ready tables.
- The repo includes both Python pipeline validation and dbt data quality checks.

## License

This project is intended for learning and analytics work and is not a production deployment package.
