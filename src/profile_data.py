"""Simple dataset profiling helpers for Day 1 familiarization."""

from typing import Any

import pandas as pd


def profile_dataframe(name: str, df: pd.DataFrame) -> dict[str, Any]:
    """Return a beginner-friendly profile dictionary for one DataFrame."""
    if df.empty:
        return {
            "name": name,
            "row_count": 0,
            "column_count": 0,
            "columns": [],
            "dtypes": {},
            "null_counts": {},
            "null_percentages": {},
            "duplicate_rows": 0,
            "sample_values": {},
            "numeric_summary": {},
        }

    null_counts = df.isna().sum()
    numeric_summary = df.describe(include="number").round(2).to_dict()

    return {
        "name": name,
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "columns": list(df.columns),
        "dtypes": {column: str(dtype) for column, dtype in df.dtypes.items()},
        "null_counts": null_counts.astype(int).to_dict(),
        "null_percentages": ((null_counts / len(df)) * 100).round(2).to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "sample_values": _sample_values(df),
        "numeric_summary": numeric_summary,
    }


def profile_datasets(datasets: dict[str, pd.DataFrame]) -> dict[str, dict[str, Any]]:
    """Profile every loaded dataset."""
    profiles = {}
    for name, df in datasets.items():
        print(f"[PROFILE] Profiling {name}")
        profiles[name] = profile_dataframe(name, df)
    return profiles


def _sample_values(df: pd.DataFrame, max_columns: int = 30) -> dict[str, list[str]]:
    """Collect a few non-null sample values per column without making reports huge."""
    samples = {}
    for column in list(df.columns)[:max_columns]:
        values = df[column].dropna().astype(str).head(3).tolist()
        samples[column] = values
    return samples
