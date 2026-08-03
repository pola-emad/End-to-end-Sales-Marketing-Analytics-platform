with raw_purchase_history AS
(
    SELECT
        purchase_sku,
        customer_id,
        product_sku,
        channel_id,
        safe_cast( quantity as numeric) as quantity,
        safe_cast( discount as numeric) as discount,
        safe_cast( created_at as date) as order_date
    FROM {{ source("omnichannel","purchaseHistory")}}
)
SELECT
*
FROM raw_purchase_history