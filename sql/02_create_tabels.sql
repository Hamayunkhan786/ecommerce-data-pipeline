CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS clean;

CREATE TABLE IF NOT EXISTS raw.online_retail (
	invoice_no TEXT,
	stock_code TEXT,
	description TEXT,
	quantity INTEGER,
	invoice_date TIMESTAMP,
	unit_price NUMERIC(12, 4),
	customer_id INTEGER,
	country TEXT
);

CREATE TABLE IF NOT EXISTS clean.online_retail_clean (
	invoice_no TEXT,
	stock_code TEXT,
	description TEXT,
	quantity INTEGER,
	invoice_date TIMESTAMP,
	unit_price NUMERIC(12, 4),
	customer_id INTEGER,
	country TEXT,
	total_sales NUMERIC(14, 4)
);
