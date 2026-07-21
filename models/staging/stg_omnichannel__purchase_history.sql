with raw_purchase_history AS
(
    SELECT
        customer_id,
        product_sku,
        channel_id,
        cast( quantity as int64) as quantity,
        cast( discount as int64) as discount,
        cast( order_date as date) as order_date
    FROM {{ source("omnichannel","purchaseHistory")}}
)
SELECT
*
FROM raw_purchase_history