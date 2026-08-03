with raw_customers AS
(
    SELECT
        customer_id,
        name,
        safe_cast(date_birth as date) as date_birth,
        email_address,
        phone_number,
        country,
        safe_cast(CREATED_AT as timestamp) as CREATED_AT,
        safe_cast(UPDATED_AT as timestamp) as UPDATED_AT
    FROM {{ source("omnichannel","customers")}}
)
SELECT
*
FROM raw_customers