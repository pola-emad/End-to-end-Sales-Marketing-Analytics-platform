select
    ch.sk_channel,
    ch.dsc_channel_name,
    avg(vh.mtr_length_of_stay_minutes) as avg_mtr_length_of_stay_minutes
from {{ref('dim_channels')}} as ch inner join {{ref('fct_visits_history')}} as vh
on ch.sk_channel = vh.sk_channel
group by 1,2