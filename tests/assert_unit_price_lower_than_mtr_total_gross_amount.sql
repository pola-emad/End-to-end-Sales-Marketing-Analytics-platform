select
    sk_customer,
    sk_channel,
    sk_product,
    sum(mtr_total_amount_gross) AS mtr_total_amount_gross,
    sum(mtr_unit_price) AS mtr_unit_price
from {{ ref('fct_purchase_history') }}
group by 1, 2, 3
having mtr_unit_price > mtr_total_amount_gross