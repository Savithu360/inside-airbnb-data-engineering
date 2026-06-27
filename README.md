# Inside Airbnb Data Engineering

## Project Overview

This project is a data engineering and analytics workflow for the Inside Airbnb Stockholm dataset. It is structured into two workflow phases: a data engineering pipeline phase, followed by an analysis, statistical testing, ML baseline, and reporting phase.

Selected city: Stockholm, Sweden

Dataset source: Inside Airbnb

## Important Data Note

Users must download the Stockholm Inside Airbnb raw files before running Phase 1 and place them in `data/raw`:

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
|   |-- final_report.pdf
|   `-- ai_usage_disclosure.md
|-- src/
|   |-- config.py
|   |-- ingest.py
|   |-- profile_data.py
|   |-- clean.py
|   |-- database.py
|   |-- run_phase1_pipeline.py
|   |-- run_phase2_eda.py
|   |-- run_phase2_statistics.py
|   `-- run_phase2_ml.py
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
python src/run_phase1_pipeline.py
python src/run_phase2_eda.py
python src/run_phase2_statistics.py
python src/run_phase2_ml.py
```

## Expected Outputs

Phase 1 creates:

- Processed CSV files in `data/processed/`
- SQLite database: `data/processed/airbnb_stockholm.db`
- Data quality report: `reports/data_quality_report.md`

Phase 2 creates:

- EDA report: `reports/eda_report.md`
- EDA figures in `reports/figures/`
- Statistical report: `reports/statistical_report.md`
- ML experiment report: `reports/ml_experiment_report.md`
- Final report: `reports/final_report.md`
- Final report PDF: `reports/final_report.pdf`
- AI usage disclosure: `reports/ai_usage_disclosure.md`
- Notebooks and ML figures

## Phase 1: Data Engineering Pipeline

Completed work:

- Raw data ingestion
- Profiling
- Cleaning
- Validation
- Processed CSV generation
- SQLite database creation
- Data quality report

## Phase 2: Analysis, Statistical Testing, ML Baseline, and Reporting

Completed work:

- Exploratory data analysis
- Figures and EDA report
- Statistical testing
- Simple ML baseline
- Final report
- AI usage disclosure

## Git And Data Files

`data/raw` and `data/processed` are ignored by Git. This keeps large raw and generated data files out of the repository. A reviewer should download the raw Stockholm Inside Airbnb files, place them in `data/raw`, and run the commands above to reproduce the processed outputs locally.

Reports, notebooks, source code, README, requirements, and generated report figures are intended to be included in the repository.

## Primary Submission Files

- `reports/final_report.pdf`
- `reports/ai_usage_disclosure.md`
- `README.md`

## Main Reports

- Data quality report: `reports/data_quality_report.md`
- EDA report: `reports/eda_report.md`
- Statistical report: `reports/statistical_report.md`
- ML experiment report: `reports/ml_experiment_report.md`
- Final report: `reports/final_report.md`
- Final report PDF: `reports/final_report.pdf`
- AI usage disclosure: `reports/ai_usage_disclosure.md`

## AI Usage Note

AI tools used: ChatGPT and Codex. AI assisted with project structuring, code generation, report drafting, and explanation. Outputs were validated by running scripts locally against the actual Stockholm data and reviewing generated results. Full disclosure is available in `reports/ai_usage_disclosure.md`.
