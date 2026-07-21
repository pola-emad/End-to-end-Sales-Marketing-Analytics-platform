WITH base_cte AS (
    SELECT 
        dp.dsc_product_name,
        dc.dsc_channel_name,
        ROUND(SUM(fct.mtr_total_amount_net),2) as sum_total_amount
    from {{ref('fct_purchase_history')}} as fct left join {{ref('dim_channels')}} dc on fct.sk_channel = dc.sk_channel
    left join {{ref('dim_products')}} as dp on fct.sk_product = dp.sk_product
    group by 1,2

),
ranked_cte as 
(
    select *,
    rank() over(partition by  dsc_channel_name order by sum_total_amount desc) as rank
    from base_cte
)
select 
    dsc_product_name,
    dsc_channel_name,
    sum_total_amount
from ranked_cte
where rank <= 3