{% macro calculate_sales_amount(quantity_column, price_column) %}
    ({{ quantity_column }} * {{ price_column }})
{% endmacro %}