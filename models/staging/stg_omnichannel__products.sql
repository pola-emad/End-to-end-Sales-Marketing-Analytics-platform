with raw_products AS
(
    SELECT
        product_sku,
        product_name,
        safe_cast(unit_price as numeric) as unit_price,
        safe_cast(CREATED_AT as timestamp) as CREATED_AT,
        safe_cast(UPDATED_AT as timestamp) as UPDATED_AT
    FROM {{ source("omnichannel","products")}}
)
SELECT
*
FROM raw_products