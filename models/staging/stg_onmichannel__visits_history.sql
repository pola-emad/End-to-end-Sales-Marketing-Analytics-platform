with raw_visit_history AS
(
    SELECT
        customer_id,
        channel_id,
        visit_timestamp,
        bounce_timestamp,
        created_at,
        updated_at
    FROM {{ source("omnichannel","visitHistory")}}
)
SELECT *
FROM raw_visit_history