SELECT
    customer_id,
    MAX(country) AS country
FROM {{ ref('stg_online_retail') }}
WHERE customer_id IS NOT NULL
GROUP BY customer_id
