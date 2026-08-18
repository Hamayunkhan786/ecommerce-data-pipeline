SELECT
    invoice_no,
    stock_code,
    description,
    quantity,
    invoice_date,
    unit_price,
    customer_id,
    country,
    quantity * unit_price AS sales_amount
FROM {{ ref('int_sales') }}
WHERE quantity > 0
  AND unit_price > 0