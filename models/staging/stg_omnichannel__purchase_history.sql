with raw_purchase_history AS
(
    SELECT
        customer_id,
        product_sku,
        channel_id,
        safe_cast( quantity as numeric) as quantity,
        safe_cast( discount as numeric) as discount,
        safe_cast( CREATED_AT as timestamp) as order_date
    FROM {{ source("omnichannel","purchaseHistory")}}
)
SELECT
*
FROM raw_purchase_history