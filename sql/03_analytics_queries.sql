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
