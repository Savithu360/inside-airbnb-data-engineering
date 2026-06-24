"""Save processed tables into a small SQLite database."""

import sqlite3
from pathlib import Path

import pandas as pd


def save_to_sqlite(tables: dict[str, pd.DataFrame], database_path: Path) -> None:
    """Write each processed DataFrame to SQLite."""
    database_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(database_path) as connection:
        for name, df in tables.items():
            table_name = f"{name}_clean"
            print(f"[DATABASE] Writing table {table_name}")
            df.to_sql(table_name, connection, if_exists="replace", index=False)
