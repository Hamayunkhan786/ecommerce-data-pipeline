WITH product_data AS (
    SELECT
        UPPER(TRIM(stock_code)) AS stock_code,
        description,
        unit_price,
        invoice_date,
        ROW_NUMBER() OVER (
            PARTITION BY UPPER(TRIM(stock_code))
            ORDER BY invoice_date DESC
        ) AS rn
    FROM {{ ref('stg_online_retail') }}
    WHERE stock_code IS NOT NULL
      AND TRIM(stock_code) <> ''
)

SELECT
    stock_code,
    description,
    unit_price
FROM product_data
WHERE rn = 1