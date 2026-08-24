SELECT
    invoice_no,
    stock_code,
    quantity,
    unit_price,
    sales_amount
FROM {{ ref('fact_sales') }}
WHERE sales_amount <> quantity * unit_price
   OR sales_amount IS NULL
