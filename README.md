# Inside Airbnb Data Engineering

## Project Overview

This project is a Day 1 data engineering pipeline for the Inside Airbnb dataset. The focus is dataset familiarization, profiling, cleaning, validation, processed outputs, and reproducible instructions.

Selected city: Stockholm, Sweden

Dataset source: Inside Airbnb

## Folder Structure

```text
inside-airbnb-data-engineering/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── 01_dataset_familiarization.ipynb
├── reports/
│   └── data_quality_report.md
├── src/
│   ├── config.py
│   ├── ingest.py
│   ├── profile_data.py
│   ├── clean.py
│   ├── database.py
│   └── run_day1_pipeline.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Setup Instructions

Create and activate a virtual environment, then install the required packages.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## How to Run the Pipeline

Run this command from the project root:

```bash
python src/run_day1_pipeline.py
```

## Expected Outputs

The pipeline creates these processed CSV files:

- `data/processed/listings_clean.csv`
- `data/processed/calendar_clean.csv`
- `data/processed/reviews_clean.csv`
- `data/processed/neighbourhoods_clean.csv`

It also creates:

- `data/processed/airbnb_stockholm.db`
- `reports/data_quality_report.md`

## Day 1 Completed Scope

- Loaded the raw listings, calendar, reviews, and neighbourhoods files.
- Profiled row counts, column counts, column names, data types, missing values, duplicate rows, sample values, and numeric summaries.
- Cleaned important listing, calendar, review, and neighbourhood fields.
- Added validation flags for invalid prices and coordinate ranges.
- Saved analysis-ready CSV outputs.
- Created a SQLite database with cleaned tables.
- Generated a Markdown data quality report.

## Day 2 Planned Scope

- Explore joins between listings, calendar, reviews, and neighbourhoods.
- Create visualizations for price, availability, room type, and review patterns.
- Investigate outliers and missing-value handling decisions.
- Prepare an analysis-ready feature table for future modeling.
- Add lightweight tests for important cleaning logic.

## AI Usage Note

AI usage note placeholder: describe how AI assistance was used, what was reviewed manually, and how outputs were validated.
