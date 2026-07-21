with stg_dim_products AS
(
    SELECT
        product_sku AS nk_product_sku,
        product_name AS dsc_product_name,
        cast(unit_price as int64) AS mtr_unit_price,
        created_at AS dt_created_at,
        updated_at AS dt_updated_at
    FROM {{ ref("stg_omnichannel__products")}}
)
SELECT
{{ dbt_utils.generate_surrogate_key( ["nk_product_sku"] )}} AS sk_product,
*
FROM stg_dim_products