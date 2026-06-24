"""Run the Day 1 Inside Airbnb data engineering pipeline."""

from datetime import datetime

import pandas as pd

from clean import clean_all_datasets
from config import CITY_NAME, DATABASE_PATH, PROCESSED_DIR, PROCESSED_FILES, RAW_FILES, REPORT_PATH, REPORTS_DIR
from database import save_to_sqlite
from ingest import load_raw_datasets
from profile_data import profile_datasets


def main() -> None:
    """Orchestrate loading, profiling, cleaning, saving, and reporting."""
    print("Starting Day 1 Inside Airbnb pipeline")
    print(f"Selected city: {CITY_NAME}")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    raw_datasets = load_raw_datasets()
    raw_profiles = profile_datasets(raw_datasets)

    print("[CLEAN] Cleaning raw datasets")
    cleaned_datasets, cleaning_actions = clean_all_datasets(raw_datasets)
    cleaned_profiles = profile_datasets(cleaned_datasets)

    save_processed_csvs(cleaned_datasets)
    save_to_sqlite(cleaned_datasets, DATABASE_PATH)
    generate_data_quality_report(raw_profiles, cleaned_profiles, cleaning_actions, cleaned_datasets)

    print("Day 1 pipeline completed successfully")
    print(f"Processed files saved in: {PROCESSED_DIR}")
    print(f"SQLite database saved to: {DATABASE_PATH}")
    print(f"Data quality report saved to: {REPORT_PATH}")


def save_processed_csvs(cleaned_datasets: dict[str, pd.DataFrame]) -> None:
    """Save cleaned DataFrames as CSV files."""
    for name, df in cleaned_datasets.items():
        output_path = PROCESSED_FILES[name]
        print(f"[SAVE] Writing {output_path}")
        df.to_csv(output_path, index=False)


def generate_data_quality_report(
    raw_profiles: dict[str, dict],
    cleaned_profiles: dict[str, dict],
    cleaning_actions: dict[str, list[str]],
    cleaned_datasets: dict[str, pd.DataFrame],
) -> None:
    """Create a Markdown data quality report from actual profile results."""
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Day 1 Data Quality Report",
        "",
        f"Generated at: {generated_at}",
        "",
        f"Selected city: {CITY_NAME}",
        "",
        "## Raw Files Used",
        "",
    ]

    for name, path in RAW_FILES.items():
        status = "found" if path.exists() else "missing"
        lines.append(f"- {name}: `{path.as_posix()}` ({status})")

    lines.extend(
        [
            "",
            "## Dataset Summary",
            "",
            "| Dataset | Raw rows | Raw columns | Clean rows | Clean columns | Raw duplicates | Clean duplicates |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for name in raw_profiles:
        raw = raw_profiles[name]
        clean = cleaned_profiles.get(name, {})
        lines.append(
            f"| {name} | {raw['row_count']} | {raw['column_count']} | "
            f"{clean.get('row_count', 0)} | {clean.get('column_count', 0)} | "
            f"{raw['duplicate_rows']} | {clean.get('duplicate_rows', 0)} |"
        )

    for name, profile in raw_profiles.items():
        lines.extend(_schema_section(name, profile))
        lines.extend(_missing_section(name, profile))
        lines.extend(_sample_section(name, profile))
        lines.extend(_numeric_section(name, profile))

    lines.extend(
        [
            "",
            "## Duplicate Summary",
            "",
            "| Dataset | Duplicate rows in raw data | Duplicate rows after cleaning |",
            "|---|---:|---:|",
        ]
    )
    for name, raw in raw_profiles.items():
        clean = cleaned_profiles.get(name, {})
        lines.append(f"| {name} | {raw['duplicate_rows']} | {clean.get('duplicate_rows', 0)} |")

    lines.extend(["", "## Validation Checks", ""])
    lines.extend(_validation_lines(cleaned_datasets, cleaned_profiles))

    lines.extend(["", "## Cleaning Actions Performed", ""])
    for name, actions in cleaning_actions.items():
        lines.append(f"### {name}")
        if actions:
            for action in actions:
                lines.append(f"- {action}")
        else:
            lines.append("- No cleaning actions were needed.")
        lines.append("")

    lines.extend(
        [
            "## Assumptions",
            "",
            "- Raw files are the Stockholm Inside Airbnb CSV files placed in `data/raw`.",
            "- Currency fields are assumed to represent listing prices in the source dataset's currency format.",
            "- Percentage fields are stored as numeric values from 0 to 100 after removing `%`.",
            "- Rows are retained during Day 1 cleaning; invalid values are flagged instead of dropped.",
            "",
            "## Limitations",
            "",
            "- Day 1 focuses on familiarization, profiling, cleaning, and storage only.",
            "- The Stockholm calendar dataset contains 100% missing values for price and adjusted_price in the raw source file. Therefore, calendar-based pricing analysis such as monthly price trends and weekday vs weekend price comparison cannot be performed using calendar data. Calendar data will be used for availability analysis only, while pricing analysis will use the listings dataset price field.",
            "- Text fields such as review comments and amenities are not deeply parsed yet.",
            "- No feature engineering, modeling, orchestration, or dashboarding is included yet.",
            "",
            "## Next Steps for Day 2",
            "",
            "- Explore relationships between listings, calendar availability, reviews, and neighbourhoods.",
            "- Use `listings_clean.price` for pricing analysis.",
            "- Use `calendar_clean` only for availability analysis.",
            "- Do not plan calendar-based price analysis unless a future dataset version includes calendar prices.",
            "- Add focused visualizations for listing price, availability, room type, and review patterns.",
            "- Decide on analysis-ready features for later ML without training a model yet.",
            "- Add lightweight tests for key cleaning functions.",
        ]
    )

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def _schema_section(name: str, profile: dict) -> list[str]:
    lines = ["", f"## Schema Summary: {name}", "", "| Column | Data type |", "|---|---|"]
    for column, dtype in profile["dtypes"].items():
        lines.append(f"| {column} | {dtype} |")
    return lines


def _missing_section(name: str, profile: dict) -> list[str]:
    lines = ["", f"## Missing Value Summary: {name}", "", "| Column | Null count | Null percentage |", "|---|---:|---:|"]
    sorted_columns = sorted(profile["null_counts"], key=profile["null_counts"].get, reverse=True)
    for column in sorted_columns:
        null_count = profile["null_counts"][column]
        null_pct = profile["null_percentages"][column]
        lines.append(f"| {column} | {null_count} | {null_pct}% |")
    return lines


def _sample_section(name: str, profile: dict) -> list[str]:
    lines = ["", f"## Sample Values: {name}", "", "| Column | Sample values |", "|---|---|"]
    for column, samples in profile["sample_values"].items():
        sample_text = ", ".join(str(value).replace("|", "/") for value in samples)
        lines.append(f"| {column} | {sample_text} |")
    return lines


def _numeric_section(name: str, profile: dict) -> list[str]:
    if not profile["numeric_summary"]:
        return ["", f"## Numeric Summary: {name}", "", "No numeric columns found."]

    lines = ["", f"## Numeric Summary: {name}", ""]
    for column, stats in profile["numeric_summary"].items():
        lines.append(f"### {column}")
        for stat_name, value in stats.items():
            lines.append(f"- {stat_name}: {value}")
        lines.append("")
    return lines


def _validation_lines(cleaned_datasets: dict[str, pd.DataFrame], cleaned_profiles: dict[str, dict]) -> list[str]:
    lines = []
    for name, profile in cleaned_profiles.items():
        lines.append(f"- {name}: {profile['row_count']} rows available after cleaning.")

    listings = cleaned_datasets.get("listings", pd.DataFrame())
    if not listings.empty:
        lines.append(f"- listings: invalid latitude values flagged: {_true_count(listings, 'invalid_latitude')}.")
        lines.append(f"- listings: invalid longitude values flagged: {_true_count(listings, 'invalid_longitude')}.")
        lines.append(f"- listings: invalid listing prices flagged: {_true_count(listings, 'invalid_price')}.")

    calendar = cleaned_datasets.get("calendar", pd.DataFrame())
    if not calendar.empty:
        lines.append(f"- calendar: invalid calendar prices flagged: {_true_count(calendar, 'invalid_price')}.")
        if {"price", "adjusted_price"}.issubset(calendar.columns):
            price_missing_pct = calendar["price"].isna().mean() * 100
            adjusted_price_missing_pct = calendar["adjusted_price"].isna().mean() * 100
            if price_missing_pct == 100 and adjusted_price_missing_pct == 100:
                lines.append(
                    "- calendar: raw `price` and `adjusted_price` are 100.0% missing, so calendar pricing "
                    "analysis is not available from this Stockholm source file."
                )

    reviews = cleaned_datasets.get("reviews", pd.DataFrame())
    if not reviews.empty and "date" in reviews.columns:
        lines.append(f"- reviews: rows with unparseable or missing review dates: {int(reviews['date'].isna().sum())}.")

    lines.extend(
        [
            "- date fields are converted with invalid parses set to null for later review.",
        ]
    )
    return lines


def _true_count(df: pd.DataFrame, column: str) -> int:
    """Count True values in a nullable boolean validation column."""
    if column not in df.columns:
        return 0
    return int(df[column].fillna(False).sum())


if __name__ == "__main__":
    main()
