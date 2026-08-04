with stg_fct_purchase_history AS
(
    SELECT
        customer_id AS nk_customer_id,
        product_sku AS nk_product_sku,
        channel_id AS nk_channel_id,
        quantity AS mtr_quantity,
        discount AS mtr_discount,
        order_date  AS dt_order_date,
        purchase_sku
    FROM {{ ref("stg_omnichannel__purchase_history")}}
)

SELECT
    {{dbt_utils.generate_surrogate_key(["fct.purchase_sku"])}} 
    AS sk_purchase_history,
    COALESCE(dcust.sk_customer, '-1') AS sk_customer,
    COALESCE(dchan.sk_channel, '-1') AS sk_channel,
    COALESCE(dprod.sk_product, '-1') AS sk_product,
    fct.dt_order_date AS dt_order_date,
    fct.mtr_quantity,
    fct.mtr_discount,
    dprod.mtr_unit_price,
    ROUND(fct.mtr_quantity * dprod.mtr_unit_price,2) AS mtr_total_amount_gross,
    ROUND(fct.mtr_quantity *
    dprod.mtr_unit_price *
    (1 - fct.mtr_discount),2) AS mtr_total_amount_net

FROM stg_fct_purchase_history AS fct
LEFT JOIN {{ ref("dim_customers")}} AS dcust
ON fct.nk_customer_id = dcust.nk_customer_id

LEFT JOIN {{ ref("dim_channels")}} AS dchan
ON fct.nk_channel_id = dchan.nk_channel_id

LEFT JOIN {{ ref("dim_products")}} AS dprod
ON fct.nk_product_sku = dprod.nk_product_sku