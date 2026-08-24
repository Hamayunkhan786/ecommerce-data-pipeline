SELECT DISTINCT

    invoice_date::date AS date_key,

    EXTRACT(YEAR FROM invoice_date)::integer AS year,

    EXTRACT(QUARTER FROM invoice_date)::integer AS quarter,

    EXTRACT(MONTH FROM invoice_date)::integer AS month,

    TO_CHAR(invoice_date, 'FMMonth') AS month_name,

    EXTRACT(DAY FROM invoice_date)::integer AS day,

    TO_CHAR(invoice_date, 'FMDay') AS day_name

FROM {{ ref('stg_online_retail') }}

WHERE invoice_date IS NOT NULL