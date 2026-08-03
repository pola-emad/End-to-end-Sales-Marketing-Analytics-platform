from datetime import datetime, timedelta
import random
import pandas as pd
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

# Set date boundaries
START_DATE = datetime(2026, 1, 1)
END_DATE = datetime(2026, 7, 31)

def random_timestamp(start, end):
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)

def fmt_ts(ts):
    return ts.strftime("%Y-%m-%d %H:%M:%S")

def fmt_date(d):
    return d.strftime("%Y-%m-%d")

# ---------------------------------------------------------
# 1. CHANNELS (5 Channels)
# ---------------------------------------------------------
channels_data = [
    {"channel_id": "CH_001", "channel_name": "Organic Search"},
    {"channel_id": "CH_002", "channel_name": "Paid Search"},
    {"channel_id": "CH_003", "channel_name": "Email Marketing"},
    {"channel_id": "CH_004", "channel_name": "Direct Web"},
    {"channel_id": "CH_005", "channel_name": "Social Media"},
]
for c in channels_data:
    created = random_timestamp(START_DATE, START_DATE + timedelta(days=5))
    c["CREATED_AT"] = fmt_ts(created)
    c["UPDATED_AT"] = fmt_ts(created)

df_channels = pd.DataFrame(channels_data)

# ---------------------------------------------------------
# 2. PRODUCTS (15 Products)
# ---------------------------------------------------------
products_data = []
categories = ["Electronics", "Apparel", "Home", "Books"]
for i in range(1, 16):
    created = random_timestamp(START_DATE, START_DATE + timedelta(days=10))
    products_data.append({
        "product_sku": f"SKU_{100 + i}",
        "product_name": f"{fake.word().capitalize()} {random.choice(categories)} Item",
        "unit_price": str(round(random.uniform(15.0, 450.0), 2)),
        "CREATED_AT": fmt_ts(created),
        "UPDATED_AT": fmt_ts(created)
    })

df_products = pd.DataFrame(products_data)

# ---------------------------------------------------------
# 3. CUSTOMERS (50 Customers)
# ---------------------------------------------------------
customers_data = []
for i in range(1, 51):
    created = random_timestamp(START_DATE, START_DATE + timedelta(days=30))
    dob = fake.date_of_birth(minimum_age=18, maximum_age=65)
    customers_data.append({
        "customer_id": f"CUST_{1000 + i}",
        "name": fake.name(),
        "date_birth": fmt_date(dob),
        "email_address": fake.company_email(),
        "phone_number": fake.phone_number(),
        "country": fake.country_code(representation="alpha-2"),
        "CREATED_AT": fmt_ts(created),
        "UPDATED_AT": fmt_ts(created)
    })

df_customers = pd.DataFrame(customers_data)

# Extract generated IDs for foreign key constraints
customer_ids = df_customers["customer_id"].tolist()
product_skus = df_products["product_sku"].tolist()
channel_ids = df_channels["channel_id"].tolist()

# ---------------------------------------------------------
# 4. VISIT HISTORY (300 Rows)
# ---------------------------------------------------------
visit_data = []
for i in range(1, 301):
    v_time = random_timestamp(START_DATE, END_DATE)
    # 70% of visits result in a bounce (bounce timestamp is 1 to 30 mins after visit)
    has_bounce = random.random() < 0.7
    b_time = v_time + timedelta(seconds=random.randint(60, 1800)) if has_bounce else None
    
    visit_data.append({
        "visit_sku": f"VIS_{10000 + i}",
        "customer_id": random.choice(customer_ids),
        "channel_id": random.choice(channel_ids),
        "visit_timestamp": fmt_ts(v_time),
        "bounce_timestamp": fmt_ts(b_time) if b_time else "",
        "CREATED_AT": fmt_ts(v_time),
        "UPDATED_AT": fmt_ts(v_time)
    })

df_visits = pd.DataFrame(visit_data)

# ---------------------------------------------------------
# 5. PURCHASE HISTORY (150 Rows)
# ---------------------------------------------------------
purchase_data = []
for i in range(1, 151):
    p_time = random_timestamp(START_DATE, END_DATE)
    purchase_data.append({
        "purchase_sku": f"PUR_{20000 + i}",
        "customer_id": random.choice(customer_ids),
        "product_sku": random.choice(product_skus),
        "channel_id": random.choice(channel_ids),
        "quantity": str(random.randint(1, 5)),
        "discount": str(round(random.choice([0.0, 0.05, 0.10, 0.20]), 2)),
        "order_date": fmt_date(p_time),
        "CREATED_AT": fmt_ts(p_time),
        "UPDATED_AT": fmt_ts(p_time)
    })

df_purchases = pd.DataFrame(purchase_data)

# Export all to CSV files as strings to match BigQuery raw schema
df_channels.astype(str).to_csv("channels.csv", index=False)
df_products.astype(str).to_csv("products.csv", index=False)
df_customers.astype(str).to_csv("customers.csv", index=False)
df_visits.astype(str).to_csv("visitHistory.csv", index=False)
df_purchases.astype(str).to_csv("purchaseHistory.csv", index=False)

print("Generated 5 relationally valid seed files.")