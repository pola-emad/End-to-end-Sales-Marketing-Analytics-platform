select 
    dd.year_number,
    dd.quarter_of_year,
    sum(ph.mtr_total_amount_net) as mtr_total_amount_net
from {{ref('dim_date')}} as dd inner join {{ref('fct_purchase_history')}} as ph 
on dd.date_day = ph.sk_order_date
group by 1,2