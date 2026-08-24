-- Sales by country
SELECT
		country,
		COUNT(DISTINCT invoice_no) AS total_orders,
		SUM(quantity) AS total_quantity,
		SUM(quantity * unit_price) AS total_sales
FROM clean.online_retail_clean
WHERE quantity > 0
	AND unit_price > 0
GROUP BY country
ORDER BY total_sales DESC;

-- Sales by date
SELECT
		invoice_date::date AS sales_date,
		COUNT(DISTINCT invoice_no) AS total_orders,
		SUM(quantity) AS total_quantity,
		SUM(quantity * unit_price) AS total_sales
FROM clean.online_retail_clean
WHERE quantity > 0
	AND unit_price > 0
GROUP BY invoice_date::date
ORDER BY sales_date;

-- Sales by product
SELECT
		stock_code,
		description,
		SUM(quantity) AS total_quantity,
		SUM(quantity * unit_price) AS total_sales
FROM clean.online_retail_clean
WHERE quantity > 0
	AND unit_price > 0
GROUP BY stock_code, description
ORDER BY total_sales DESC;

-- Sales by customer
SELECT
		customer_id,
		COUNT(DISTINCT invoice_no) AS total_orders,
		SUM(quantity) AS total_quantity,
		SUM(quantity * unit_price) AS total_sales
FROM clean.online_retail_clean
WHERE quantity > 0
	AND unit_price > 0
	AND customer_id IS NOT NULL
GROUP BY customer_id
ORDER BY total_sales DESC;

-- Monthly sales
SELECT
		DATE_TRUNC('month', invoice_date)::date AS sales_month,
		COUNT(DISTINCT invoice_no) AS total_orders,
		SUM(quantity) AS total_quantity,
		SUM(quantity * unit_price) AS total_sales
FROM clean.online_retail_clean
WHERE quantity > 0
	AND unit_price > 0
GROUP BY DATE_TRUNC('month', invoice_date)::date
ORDER BY sales_month;

-- Key performance indicators
SELECT
		COUNT(DISTINCT invoice_no) AS total_orders,
		COUNT(DISTINCT customer_id) AS total_customers,
		COUNT(DISTINCT stock_code) AS total_products,
		SUM(quantity) AS total_quantity,
		SUM(quantity * unit_price) AS total_sales,
		ROUND(SUM(quantity * unit_price) / NULLIF(COUNT(DISTINCT invoice_no), 0), 2) AS average_order_value
FROM clean.online_retail_clean
WHERE quantity > 0
	AND unit_price > 0;

-- Average order value by country
SELECT
		country,
		COUNT(DISTINCT invoice_no) AS total_orders,
		ROUND(SUM(quantity * unit_price) / NULLIF(COUNT(DISTINCT invoice_no), 0), 2) AS average_order_value,
		SUM(quantity * unit_price) AS total_sales
FROM clean.online_retail_clean
WHERE quantity > 0
	AND unit_price > 0
GROUP BY country
ORDER BY average_order_value DESC;

-- Top ten products by sales
SELECT
		stock_code,
		description,
		SUM(quantity) AS total_quantity,
		SUM(quantity * unit_price) AS total_sales
FROM clean.online_retail_clean
WHERE quantity > 0
	AND unit_price > 0
GROUP BY stock_code, description
ORDER BY total_sales DESC
LIMIT 10;
