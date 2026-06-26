# ECB Exchange Rates Pipeline

An end-to-end data pipeline that ingests daily euro foreign-exchange reference rates from the European Central Bank (ECB), loads them into a cloud Postgres database, and transforms them into clean, tested analytical models with dbt.

Built to demonstrate the core building blocks of a modern data engineering workflow: **ingestion → storage → transformation → data quality testing**.

---

## Architecture

```
  ECB (XML)  ──►  Python (extract)  ──►  Neon / Postgres  ──►  dbt  ──►  analytics models
   source           requests +              raw_rates          staging      fct_daily_rates
                    xml parsing                                + marts       (+ data tests)
```

The dbt lineage (auto-generated from model references):

```
raw_rates  ──►  stg_rates  ──►  fct_daily_rates
```

> _Tip: replace this block with a screenshot of the dbt lineage graph (`dbt docs`)._

---

## What it does

1. **Extract** — pulls the latest daily reference rates from the ECB's public feed and parses the XML.
2. **Load** — writes the rates into a `raw_rates` table in a serverless Postgres database (Neon). The load is **idempotent**: re-running it for the same date replaces existing rows instead of duplicating them.
3. **Transform** — dbt builds two layers of models:
   - `stg_rates` (staging): cleans the raw data, filters invalid rows, and derives `eur_per_unit`.
   - `fct_daily_rates` (mart): the analytics-ready model, adding a currency-strength classification.
4. **Test** — dbt runs automated data quality checks (`not_null`, `unique`) on every build, so broken data fails loudly instead of flowing downstream.

---

## Tech stack

| Layer | Tool |
|---|---|
| Language | Python |
| Database | Postgres (Neon, serverless cloud) |
| Transformation | dbt (dbt-postgres) |
| Source | ECB daily reference rates (public XML feed) |
| Dev environment | GitHub Codespaces |

---

## Data quality

Data quality is enforced declaratively in dbt rather than checked manually:

- `currency` — must be present (`not_null`) and have no duplicates within a day (`unique`)
- `rate` — must be present (`not_null`)
- `rate_date` — must be present (`not_null`)

Every `dbt build` re-runs these tests, giving the pipeline a built-in safety net.

---

## Project structure

```
ecb-rates-pipeline/
├── README.md
├── requirements.txt
├── .env                  # connection string (not committed)
├── .gitignore
├── extract/
│   └── fetch_rates.py    # extract from ECB + load into Postgres
├── db/
│   └── create_table.py   # creates the raw_rates table
└── dbt_ecb/              # dbt project (staging + marts + tests)
    └── models/
        ├── staging/
        │   ├── stg_rates.sql
        │   └── stg_rates.yml
        └── marts/
            └── fct_daily_rates.sql
```

---

## How to run

### Prerequisites
- Python 3.10+
- A Postgres database (this project uses a free Neon database)

### Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your database connection string to a .env file
echo "DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require" > .env

# 3. Create the target table
python db/create_table.py

# 4. Extract + load the latest ECB rates
python extract/fetch_rates.py

# 5. Build and test the dbt models
cd dbt_ecb
dbt run
dbt test
```

---

## What I learned

- Building an idempotent extract-and-load step in Python
- Managing secrets safely with environment variables (keeping credentials out of source control)
- Structuring transformations in layers (staging → marts) with dbt
- Modeling dependencies with dbt `ref()` and reading the resulting lineage graph
- Enforcing data quality with automated tests instead of manual checks

---

## Possible next steps

- Schedule the pipeline to run daily with GitHub Actions (orchestration)
- Backfill and store historical rates to enable trend analysis
- Add a dashboard layer (Power BI / a simple chart) on top of `fct_daily_rates`
- Add more granular dbt tests (accepted ranges, relationships)