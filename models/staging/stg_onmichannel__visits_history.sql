with raw_visit_history AS
(
    SELECT
        customer_id,
        channel_id,
        safe_cast(visit_timestamp as timestamp) as visit_timestamp,
        safe_cast(bounce_timestamp as timestamp) as bounce_timestamp,
        safe_cast(created_at as timestamp) as created_at,
        safe_cast(updated_at as timestamp) as updated_at
    FROM {{ source("omnichannel","visitHistory")}}
)
SELECT *
FROM raw_visit_history