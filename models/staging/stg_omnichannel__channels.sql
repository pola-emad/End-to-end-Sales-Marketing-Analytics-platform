with raw_channels AS
(
    SELECT
        channel_id,
        channel_name,
        safe_cast(CREATED_AT as timestamp) as CREATED_AT,
        safe_cast(UPDATED_AT as timestamp) as UPDATED_AT
    FROM {{ source("omnichannel","channels")}}
)
SELECT
*
FROM raw_channels