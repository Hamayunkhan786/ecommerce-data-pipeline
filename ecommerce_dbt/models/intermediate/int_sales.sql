WITH source_data AS (

    SELECT
        invoice_no,
        stock_code,
        description,
        quantity,
        invoice_date,
        unit_price,
        customer_id,
        country
    FROM {{ ref('stg_online_retail') }}

),

cleaned AS (

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
    FROM source_data
    WHERE quantity > 0
      AND unit_price > 0

)

SELECT *
FROM cleaned