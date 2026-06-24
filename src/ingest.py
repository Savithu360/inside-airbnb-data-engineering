"""Read raw Inside Airbnb datasets from disk."""

from pathlib import Path

import pandas as pd

from config import RAW_FILES


def load_csv_safely(dataset_name: str, file_path: Path) -> pd.DataFrame:
    """Load one CSV file and return an empty DataFrame if it is missing."""
    if not file_path.exists():
        print(f"[WARN] Missing raw file for {dataset_name}: {file_path}")
        return pd.DataFrame()

    try:
        print(f"[LOAD] Reading {dataset_name} from {file_path}")
        return pd.read_csv(file_path, low_memory=False)
    except Exception as exc:
        print(f"[ERROR] Could not load {dataset_name}: {exc}")
        return pd.DataFrame()


def load_raw_datasets() -> dict[str, pd.DataFrame]:
    """Load all expected raw datasets."""
    datasets = {}
    for dataset_name, file_path in RAW_FILES.items():
        datasets[dataset_name] = load_csv_safely(dataset_name, file_path)
    return datasets
