with raw_products AS
(
    SELECT
        product_sku,
        product_name,
        unit_price,
        CREATED_AT,
        UPDATED_AT
    FROM {{ source("omnichannel","products")}}
)
SELECT
*
FROM raw_products