"""Project configuration for the Day 1 Airbnb data pipeline."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

RAW_FILES = {
    "listings": RAW_DIR / "listings.csv.gz",
    "calendar": RAW_DIR / "calendar.csv.gz",
    "reviews": RAW_DIR / "reviews.csv.gz",
    "neighbourhoods": RAW_DIR / "neighbourhoods.csv",
}

PROCESSED_FILES = {
    "listings": PROCESSED_DIR / "listings_clean.csv",
    "calendar": PROCESSED_DIR / "calendar_clean.csv",
    "reviews": PROCESSED_DIR / "reviews_clean.csv",
    "neighbourhoods": PROCESSED_DIR / "neighbourhoods_clean.csv",
}

DATABASE_PATH = PROCESSED_DIR / "airbnb_stockholm.db"
REPORT_PATH = REPORTS_DIR / "data_quality_report.md"

CITY_NAME = "Stockholm, Sweden"
