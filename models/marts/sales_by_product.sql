SELECT
    stock_code,
    description,
    SUM(quantity) AS total_quantity,
    SUM(sales_amount) AS total_sales
FROM {{ ref('fact_sales') }}
GROUP BY
    stock_code,
    description
ORDER BY total_sales DESC