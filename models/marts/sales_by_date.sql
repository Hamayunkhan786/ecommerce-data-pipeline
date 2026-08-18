SELECT
    DATE(invoice_date) AS sales_date,
    COUNT(DISTINCT invoice_no) AS total_orders,
    SUM(quantity) AS total_quantity,
    SUM(sales_amount) AS total_sales
FROM {{ ref('fact_sales') }}
GROUP BY DATE(invoice_date)
ORDER BY sales_date