SELECT
    stock_code,
    MAX(description) AS description,
    MAX(unit_price) AS unit_price
FROM {{ ref('stg_online_retail') }}
WHERE stock_code IS NOT NULL
GROUP BY stock_code