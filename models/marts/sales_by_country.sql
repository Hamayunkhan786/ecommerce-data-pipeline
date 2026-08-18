SELECT
    country,
    COUNT(DISTINCT invoice_no) AS total_orders,
    SUM(quantity) AS total_quantity,
    SUM(sales_amount) AS total_sales
FROM {{ ref('fact_sales') }}
GROUP BY country
ORDER BY total_sales DESC