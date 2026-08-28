# Retail Sales and Marketing Analytics Platform

## Overview

This project is a synthetic retail analytics platform built with dbt. It demonstrates how raw omnichannel customer, product, visit, and purchase data can be transformed into a tested dimensional model and a reusable semantic layer for sales and marketing analysis.

The project is designed as a portfolio demonstration of analytics engineering practices and the type of contribution a data professional can make to a retail data team.

## Business Problem

Retail businesses collect sales and digital engagement data across multiple channels, but raw operational data is difficult to use consistently for decision-making. Without a shared analytical model, teams may spend time reconciling definitions, joining source tables manually, and producing inconsistent answers to questions such as:

- Which channels generate visits, conversions, and revenue?
- Which products perform best in each channel?
- How much time do visitors spend on the website, and how often do they bounce?
- How do discounts affect gross revenue and net revenue?
- Which customers are active or repeat purchasers?
- How does sales performance change over time?

This platform addresses that problem by organizing source data into trusted, analysis-ready models with shared dimensions, fact tables, documented metrics, and automated data quality tests.

## Business Impact

Because the data is synthetic, this project does not claim measured commercial results. Its demonstrated business value is the analytical foundation it provides for retail teams:

- **Consistent reporting:** Shared dimensions and fact tables provide common definitions for customers, products, channels, visits, orders, revenue, discounts, and engagement.
- **Channel performance analysis:** Marketing and commercial teams can compare visits, bounce rate, conversion rate, average visit duration, and revenue across channels.
- **Sales performance analysis:** Stakeholders can examine revenue, units sold, average order value, discounted orders, and product performance by time period and channel.
- **Customer insight:** Analysts can identify active customers, repeat customers, and high-value customers within a channel and time period.
- **Reusable decision support:** The semantic metrics make recurring analysis easier to reproduce and reduce dependence on one-off SQL queries.
- **Data trust:** Uniqueness, null, relationship, and financial-value tests help identify invalid or inconsistent data before it is used for reporting.

## Project Structure

```text
.
├── analyses/                         # Example business analyses
│   ├── average_stay_length_per_channel.sql
│   ├── top_3_custoemers_in_2023_on_mobile_app.sql
│   ├── top_3_selling_products_per_channel.sql
│   └── total_amount_sold_by_quarter.sql
├── ETL Scripts/
│   ├── ETL.py                         # MySQL-to-BigQuery ingestion example
│   └── Generate_mock_date.py          # Synthetic data generation
├── macros/
│   └── generate_schema_name.sql       # Custom dbt schema naming
├── models/
│   ├── staging/                       # Source cleanup and type conversion
│   └── marts/                         # Dimensions, facts, and semantic metrics
├── seeds/                             # Synthetic retail source data
│   ├── channels.csv
│   ├── customers.csv
│   ├── products.csv
│   ├── purchaseHistory.csv
│   └── visitHistory.csv
├── snapshots/                         # dbt snapshot directory
├── tests/                             # Singular business-rule tests
├── dbt_project.yml                    # dbt project configuration
├── packages.yml                       # dbt package dependencies
└── README.md
```

Generated dbt artifacts are stored in `target/` and are not part of the analytical model itself.

## Data Model

### Source and staging layer

The source definitions represent an `omnichannel` source with five raw tables:

- `channels`
- `customers`
- `products`
- `visitHistory`
- `purchaseHistory`

Staging models standardize names, cast fields to analytical data types, and prepare the raw records for downstream joins.

### Mart layer

The mart layer contains the following models:

| Model | Purpose |
| --- | --- |
| `dim_customers` | Customer attributes, including anonymous users represented in the customer dimension |
| `dim_products` | Product names, prices, and record timestamps |
| `dim_channels` | Sales and engagement channel attributes |
| `dim_date` | Calendar and time analysis |
| `fct_purchase_history` | Purchase-level quantities, discounts, gross amounts, and net amounts |
| `fct_visits_history` | Visit timestamps, bounce timestamps, and visit duration |

Staging models are configured as views and mart models as tables in `dbt_project.yml`.

## Metrics and Example Analyses

The semantic layer defines reusable metrics including:

- Orders, units sold, unique products sold, and active customers
- Total revenue and gross revenue
- Discount value, discounted orders, and effective discount rate
- Conversion rate, bounce rate, and average visit duration
- Average revenue per visit and average order value
- Repeat purchase rate
- Monthly and rolling 30-day revenue

The example analyses use these models to answer practical retail questions, including quarterly sales, the top three products by channel, average visit duration by channel, and the top three customers using the mobile channel in 2023.

## Data Quality

The project includes dbt tests for:

- Unique and non-null surrogate keys
- Referential integrity between fact and dimension models
- Positive gross purchase amounts
- Positive length-of-stay values
- Unit prices that are lower than total gross purchase amounts where applicable

These checks demonstrate how analytical contracts can be enforced alongside transformations.

## Technology

- Python and pandas for the example ingestion and synthetic-data workflow
- MySQL as the example operational source
- BigQuery as the example analytical warehouse
- dbt for transformation, testing, documentation, and semantic metrics
- `dbt_utils` and `dbt_date` packages

## How to Use the Project

The workflow below describes the complete path from synthetic source data to dbt models and analyses.

### 1. Clone the repository and install dependencies

Install Python and the packages required by the data-generation and ingestion scripts:

```bash
pip install pandas Faker mysql-connector-python pandas-gbq dbt-bigquery
```

Install the dbt packages from the project root:

```bash
dbt deps
```

### 2. Generate synthetic CSV data

The generator is currently named `ETL Scripts/Generate_mock_date.py`. Run it from the directory where you want the CSV files to be created:

```bash
cd "ETL Scripts"
python Generate_mock_date.py
```

The script creates five relationally valid files:

- `channels.csv`
- `products.csv`
- `customers.csv`
- `visitHistory.csv`
- `purchaseHistory.csv`

The checked-in copies are located in `seeds/`. If you generate a fresh set outside that directory, move or copy the files into `seeds/` when using the local dbt seed workflow described below. The generator currently produces records dated from January through July 2026. The date dimension and one example analysis use earlier date ranges, so update those project settings if you need the generated records to appear in those analyses.

### 3. Populate a MySQL source database

Create a MySQL database and load the five CSV files as tables using the source table names expected by the dbt project:

```text
channels
customers
products
visitHistory
purchaseHistory
```

The MySQL tables must contain the columns used by the staging models. In particular, `visitHistory` needs visit and bounce timestamps, and `purchaseHistory` needs customer, product, channel, quantity, discount, and order-date fields.

### 4. Configure and run the ingestion script

Open `ETL Scripts/ETL.py` and replace the placeholder values in `kwargs` with the connection details for your MySQL database and BigQuery project:

```python
kwargs = {
		"bq_project_id": "your_google_cloud_project",
		"dataset": "omnichannel_raw",
		"mysql_host": "your_mysql_host",
		"mysql_user": "your_mysql_user",
		"mysql_password": "your_mysql_password",
		"mysql_database": "your_mysql_database",
		"mysql_port": 3306,
}
```

Authenticate to Google Cloud using the method supported by your environment, then run the script:

```bash
python "ETL Scripts/ETL.py"
```

The script discovers every table in the configured MySQL database, extracts it with pandas, performs basic date conversion, and writes it to the configured BigQuery dataset using `if_exists="replace"`. Use a database containing only the intended source tables, or review the table-discovery behavior before using it with a wider operational database.

### 5. Configure the dbt BigQuery profile

The repository does not include `profiles.yml`, because dbt credentials are user-specific. Create a profile named `sales_and_marketing_Data_platform` in your local dbt profiles directory, normally `~/.dbt/profiles.yml`, and configure it for your BigQuery project and authentication method.

A service-account configuration follows this structure:

```yaml
sales_and_marketing_Data_platform:
	target: dev
	outputs:
		dev:
			type: bigquery
			method: service-account
			project: your_google_cloud_project
			dataset: your_dbt_dataset
			threads: 4
			keyfile: C:/path/to/service-account-key.json
			timeout_seconds: 300
			location: US
```

Use a secure authentication method appropriate for your environment and do not commit credentials or service-account keys to the repository.

### 6. Validate the dbt connection and build the project

From the project root, validate the profile and install state:

```bash
dbt debug
```

If you loaded the source tables into BigQuery through `ETL.py`, build the staging models, marts, tests, and documentation:

```bash
dbt build
```

The project expects the raw tables in the `omnichannel_raw` dataset. The source configuration currently points to the BigQuery project `dbt-ae-book`; update `models/staging/_omnichannel_raw_sources.yml` if your raw tables are in a different project.

### 7. Run the local seed alternative

If you want to test the dbt project without setting up MySQL and the Python ETL path, place the CSV files in `seeds/` and run:

```bash
dbt seed
dbt build --select staging marts
```

This loads the CSV files into the configured BigQuery project and schema, then builds the models. The source configuration still needs to reference the same project and dataset where dbt creates the seeded tables.

### 8. Run analyses and inspect documentation

Execute the example analyses after the models have been built:

```bash
dbt compile --select analysis
dbt docs generate
dbt docs serve
```

The analysis SQL files are compiled into `target/compiled/`. The documentation site exposes model descriptions, column metadata, lineage, metrics, and tests.

Useful focused commands during development are:

```bash
dbt run --select staging
dbt run --select marts
dbt test
dbt build --select fct_purchase_history+
```

## Scope and Assumptions

This is a synthetic portfolio project. The source records, business entities, and analytical results are intended to demonstrate a realistic retail data workflow; they do not represent a real retailer or real business performance. The ETL script contains placeholder connection settings that must be replaced before connecting to external systems.
