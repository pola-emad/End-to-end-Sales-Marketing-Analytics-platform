with base as 
(
    select
        dcust.dsc_name,
        dcust.dsc_email_address,
        ROUND(SUM(fct.mtr_total_amount_net),2) as sum_total_amount
    from {{ref('fct_purchase_history')}} as fct left join {{ref('dim_date')}} as dd on fct.dt_order_date = dd.date_day
    left join {{ref('dim_channels')}} dc on dc.sk_channel = fct.sk_channel
    left join {{ref('dim_customers')}} dcust on dcust.sk_customer = fct.sk_customer

    where dd.year_number = 2023 and dc.dsc_channel_name = 'mobile phone'
    group by 1,2
    order by sum_total_amount desc
        limit 3
)
select * from base
