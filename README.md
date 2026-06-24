# Inside Airbnb Data Engineering

## Project Overview

This project is a data engineering and analytics workflow for the Inside Airbnb dataset. Day 1 covers dataset familiarization, profiling, cleaning, validation, processed outputs, and reproducible instructions. Day 2 adds exploratory data analysis and business-focused insights for Stockholm.

Selected city: Stockholm, Sweden

Dataset source: Inside Airbnb

## Folder Structure

```text
inside-airbnb-data-engineering/
|-- data/
|   |-- raw/
|   `-- processed/
|-- notebooks/
|   |-- 01_dataset_familiarization.ipynb
|   `-- 02_exploratory_data_analysis.ipynb
|-- reports/
|   |-- figures/
|   |-- data_quality_report.md
|   `-- eda_report.md
|-- src/
|   |-- config.py
|   |-- ingest.py
|   |-- profile_data.py
|   |-- clean.py
|   |-- database.py
|   |-- run_day1_pipeline.py
|   `-- run_day2_eda.py
|-- README.md
|-- requirements.txt
`-- .gitignore
```

## Setup Instructions

Create and activate a virtual environment, then install the required packages.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## How to Run Day 1 Pipeline

Run this command from the project root:

```bash
python src/run_day1_pipeline.py
```

## How to Run Day 2 EDA

Run this command from the project root after the Day 1 SQLite database exists:

```bash
python src/run_day2_eda.py
```

## Expected Outputs

Day 1 creates these processed CSV files:

- `data/processed/listings_clean.csv`
- `data/processed/calendar_clean.csv`
- `data/processed/reviews_clean.csv`
- `data/processed/neighbourhoods_clean.csv`

Day 1 also creates:

- `data/processed/airbnb_stockholm.db`
- `reports/data_quality_report.md`

Day 2 creates:

- `reports/eda_report.md`
- `reports/figures/`
- `notebooks/02_exploratory_data_analysis.ipynb`

## Day 1 Completed Scope

- Loaded the raw listings, calendar, reviews, and neighbourhoods files.
- Profiled row counts, column counts, column names, data types, missing values, duplicate rows, sample values, and numeric summaries.
- Cleaned important listing, calendar, review, and neighbourhood fields.
- Added validation flags for invalid prices and coordinate ranges.
- Saved analysis-ready CSV outputs.
- Created a SQLite database with cleaned tables.
- Generated a Markdown data quality report.

## Day 2 Completed Scope

- Loaded cleaned data from `data/processed/airbnb_stockholm.db`.
- Used SQL queries and selected only required calendar columns for availability analysis.
- Generated charts for room type, listing price, neighbourhood price, property type, calendar availability, hosts, and reviews.
- Wrote the Day 2 EDA report to `reports/eda_report.md`.
- Saved PNG figures to `reports/figures/`.
- Used `listings_clean.price` for pricing analysis because calendar prices are missing.
- Used `calendar_clean` only for availability analysis.

## Stockholm Dataset Limitation

The Stockholm calendar dataset contains 100% missing values for price and adjusted_price in the raw source file. Therefore, calendar-based pricing analysis such as monthly price trends and weekday vs weekend price comparison cannot be performed using calendar data. Calendar data will be used for availability analysis only, while pricing analysis will use the listings dataset price field.

## Day 3 Planned Scope

- Run statistical tests for selected business questions.
- Create a simple ML baseline only after defining a clear target and feature table.
- Continue avoiding calendar-based price analysis unless a future dataset version includes calendar prices.

## AI Usage Note

AI usage note placeholder: describe how AI assistance was used, what was reviewed manually, and how outputs were validated.
