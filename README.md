# Inside Airbnb Data Engineering

## Project Overview

This project is a data engineering and analytics workflow for the Inside Airbnb Stockholm dataset. It demonstrates a simple, reproducible pipeline for data ingestion, profiling, cleaning, validation, exploratory data analysis, statistical testing, and a baseline machine learning experiment.

Selected city: Stockholm, Sweden

Dataset source: Inside Airbnb

## Important Data Note

Users must download the Stockholm Inside Airbnb raw files before running Day 1 and place them in `data/raw`:

- `listings.csv.gz`
- `calendar.csv.gz`
- `reviews.csv.gz`
- `neighbourhoods.csv`

The Stockholm calendar dataset contains 100% missing values for `price` and `adjusted_price` in the raw source file. Calendar data is used for availability analysis only. Pricing analysis and the ML baseline use `listings_clean.price`.

## Folder Structure

```text
inside-airbnb-data-engineering/
|-- data/
|   |-- raw/
|   `-- processed/
|-- notebooks/
|   |-- 01_dataset_familiarization.ipynb
|   |-- 02_exploratory_data_analysis.ipynb
|   |-- 03_statistical_analysis.ipynb
|   `-- 04_price_prediction_baseline.ipynb
|-- reports/
|   |-- figures/
|   |-- data_quality_report.md
|   |-- eda_report.md
|   |-- statistical_report.md
|   |-- ml_experiment_report.md
|   |-- final_report.md
|   `-- ai_usage_disclosure.md
|-- src/
|   |-- config.py
|   |-- ingest.py
|   |-- profile_data.py
|   |-- clean.py
|   |-- database.py
|   |-- run_day1_pipeline.py
|   |-- run_day2_eda.py
|   |-- run_day3_statistics.py
|   `-- run_day3_ml.py
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

## Full Run Order

Run these commands from the project root:

```bash
python src/run_day1_pipeline.py
python src/run_day2_eda.py
python src/run_day3_statistics.py
python src/run_day3_ml.py
```

## Expected Outputs

Day 1 creates:

- `data/processed/listings_clean.csv`
- `data/processed/calendar_clean.csv`
- `data/processed/reviews_clean.csv`
- `data/processed/neighbourhoods_clean.csv`
- `data/processed/airbnb_stockholm.db`
- `reports/data_quality_report.md`

Day 2 creates:

- `reports/eda_report.md`
- PNG charts in `reports/figures/`
- `notebooks/02_exploratory_data_analysis.ipynb`

Day 3 creates:

- `reports/statistical_report.md`
- `reports/ml_experiment_report.md`
- `reports/final_report.md`
- `reports/ai_usage_disclosure.md`
- `reports/figures/ml_model_comparison.png`
- `reports/figures/ml_feature_importance.png`
- `notebooks/03_statistical_analysis.ipynb`
- `notebooks/04_price_prediction_baseline.ipynb`

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

## Day 3 Completed Scope

- Ran Mann-Whitney U tests for room type prices, superhost review scores, and price by review-volume group.
- Ran a Kruskal-Wallis test for neighbourhood price differences.
- Built a simple listing price prediction baseline using median baseline, linear regression, random forest, and gradient boosting models.
- Saved ML comparison and feature-importance figures.
- Created final report and AI usage disclosure.

## Git And Data Files

`data/raw` and `data/processed` are ignored by Git. This keeps large raw and generated data files out of the repository. A reviewer should download the raw Stockholm Inside Airbnb files, place them in `data/raw`, and run the commands above to reproduce the processed outputs.

Reports, notebooks, source code, README, requirements, and generated report figures are intended to be included in the repository.

## Main Reports

- Data quality report: `reports/data_quality_report.md`
- EDA report: `reports/eda_report.md`
- Statistical report: `reports/statistical_report.md`
- ML experiment report: `reports/ml_experiment_report.md`
- Final report: `reports/final_report.md`
- AI usage disclosure: `reports/ai_usage_disclosure.md`

## AI Usage Note

AI tools used: ChatGPT and Codex. AI assisted with project structuring, code generation, report drafting, and explanation. Outputs were validated by running scripts locally against the actual Stockholm data and reviewing generated results. Full disclosure is available in `reports/ai_usage_disclosure.md`.
