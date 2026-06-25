"""Run Day 3 statistical tests for the Stockholm Inside Airbnb project."""

import sqlite3
from pathlib import Path

import pandas as pd
from scipy import stats

from config import CITY_NAME, DATABASE_PATH, REPORTS_DIR


REPORT_PATH = REPORTS_DIR / "statistical_report.md"


def main() -> None:
    """Load listing data, run statistical tests, and write a Markdown report."""
    print("Starting Day 3 statistical analysis")
    print(f"Selected city: {CITY_NAME}")

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}. Run Day 1 first.")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    listings = load_listings()

    results = {
        "room_price": test_entire_home_vs_private_room_prices(listings),
        "superhost_scores": test_superhost_review_scores(listings),
        "review_count_price": test_review_count_price_groups(listings),
        "neighbourhood_price": test_neighbourhood_price_differences(listings),
    }

    write_report(listings, results)
    print(f"Statistical report saved to: {REPORT_PATH}")


def load_listings() -> pd.DataFrame:
    """Load only columns needed for Day 3 statistical tests."""
    query = """
        SELECT
            id,
            room_type,
            price,
            host_is_superhost,
            review_scores_rating,
            number_of_reviews,
            neighbourhood_cleansed
        FROM listings_clean
    """
    with sqlite3.connect(DATABASE_PATH) as connection:
        return pd.read_sql_query(query, connection)


def test_entire_home_vs_private_room_prices(listings: pd.DataFrame) -> dict:
    """Compare listing prices for entire homes and private rooms."""
    data = listings.dropna(subset=["price", "room_type"])
    entire = data.loc[data["room_type"] == "Entire home/apt", "price"]
    private = data.loc[data["room_type"] == "Private room", "price"]
    statistic, p_value = stats.mannwhitneyu(entire, private, alternative="two-sided")
    return {
        "group_a": "Entire home/apt",
        "group_b": "Private room",
        "count_a": int(entire.count()),
        "count_b": int(private.count()),
        "median_a": float(entire.median()),
        "median_b": float(private.median()),
        "statistic": float(statistic),
        "p_value": float(p_value),
    }


def test_superhost_review_scores(listings: pd.DataFrame) -> dict:
    """Compare review scores for superhosts and non-superhosts."""
    data = listings.dropna(subset=["review_scores_rating", "host_is_superhost"])
    superhost = data.loc[data["host_is_superhost"] == 1, "review_scores_rating"]
    non_superhost = data.loc[data["host_is_superhost"] == 0, "review_scores_rating"]
    statistic, p_value = stats.mannwhitneyu(superhost, non_superhost, alternative="two-sided")
    return {
        "group_a": "Superhost",
        "group_b": "Non-superhost",
        "count_a": int(superhost.count()),
        "count_b": int(non_superhost.count()),
        "median_a": float(superhost.median()),
        "median_b": float(non_superhost.median()),
        "mean_a": float(superhost.mean()),
        "mean_b": float(non_superhost.mean()),
        "statistic": float(statistic),
        "p_value": float(p_value),
    }


def test_review_count_price_groups(listings: pd.DataFrame) -> dict:
    """Compare prices for listings with more than 10 reviews vs 10 or fewer."""
    data = listings.dropna(subset=["price", "number_of_reviews"])
    high_review = data.loc[data["number_of_reviews"] > 10, "price"]
    low_review = data.loc[data["number_of_reviews"] <= 10, "price"]
    statistic, p_value = stats.mannwhitneyu(high_review, low_review, alternative="two-sided")
    return {
        "group_a": "More than 10 reviews",
        "group_b": "10 or fewer reviews",
        "count_a": int(high_review.count()),
        "count_b": int(low_review.count()),
        "median_a": float(high_review.median()),
        "median_b": float(low_review.median()),
        "statistic": float(statistic),
        "p_value": float(p_value),
    }


def test_neighbourhood_price_differences(listings: pd.DataFrame, min_priced_listings: int = 30) -> dict:
    """Test whether listing prices differ across neighbourhoods with enough priced listings."""
    data = listings.dropna(subset=["price", "neighbourhood_cleansed"])
    counts = data["neighbourhood_cleansed"].value_counts()
    eligible_neighbourhoods = counts[counts >= min_priced_listings].index.tolist()
    eligible = data[data["neighbourhood_cleansed"].isin(eligible_neighbourhoods)]

    grouped_prices = [
        group["price"]
        for _, group in eligible.groupby("neighbourhood_cleansed")
    ]
    statistic, p_value = stats.kruskal(*grouped_prices)

    top_medians = (
        eligible.groupby("neighbourhood_cleansed")["price"]
        .agg(count="count", median_price="median")
        .sort_values("median_price", ascending=False)
        .head(10)
        .reset_index()
    )

    return {
        "min_priced_listings": min_priced_listings,
        "eligible_neighbourhood_count": len(eligible_neighbourhoods),
        "statistic": float(statistic),
        "p_value": float(p_value),
        "top_medians": top_medians,
    }


def write_report(listings: pd.DataFrame, results: dict) -> None:
    """Write statistical findings and business interpretation to Markdown."""
    missing_price_pct = listings["price"].isna().mean() * 100
    missing_score_pct = listings["review_scores_rating"].isna().mean() * 100

    lines = [
        "# Day 3 Statistical Analysis Report",
        "",
        f"Selected city: {CITY_NAME}",
        "",
        "Data source: Inside Airbnb",
        "",
        "## Scope",
        "",
        "This report adds simple statistical tests to the Day 1 and Day 2 work. Tests use cleaned listing data from the SQLite database. Calendar price fields are not used because Stockholm calendar `price` and `adjusted_price` are 100% missing in the raw source data.",
        "",
        "## Important Notes",
        "",
        f"- Listing prices have {missing_price_pct:.2f}% missing values; price-based tests exclude missing prices.",
        f"- Review scores have {missing_score_pct:.2f}% missing values; review-score tests exclude missing scores.",
        "- Statistical significance does not prove causation.",
        "- Business significance is different from statistical significance. A result can be statistically significant but still too small or too biased to act on directly.",
        "",
        "## Test 1: Entire Home/Apt vs Private Room Listing Prices",
        "",
        result_table(
            [
                ("Group A", results["room_price"]["group_a"]),
                ("Group B", results["room_price"]["group_b"]),
                ("Group A count", f"{results['room_price']['count_a']:,}"),
                ("Group B count", f"{results['room_price']['count_b']:,}"),
                ("Group A median price", f"{results['room_price']['median_a']:,.2f}"),
                ("Group B median price", f"{results['room_price']['median_b']:,.2f}"),
                ("Mann-Whitney U statistic", f"{results['room_price']['statistic']:,.2f}"),
                ("p-value", format_p_value(results["room_price"]["p_value"])),
            ]
        ),
        "",
        "Business interpretation: Entire homes and private rooms represent different accommodation products, so a price difference is expected. This supports using room type as a required segment for pricing analysis and any future model.",
        "",
        "## Test 2: Superhost vs Non-Superhost Review Scores",
        "",
        result_table(
            [
                ("Group A", results["superhost_scores"]["group_a"]),
                ("Group B", results["superhost_scores"]["group_b"]),
                ("Group A count", f"{results['superhost_scores']['count_a']:,}"),
                ("Group B count", f"{results['superhost_scores']['count_b']:,}"),
                ("Group A median score", f"{results['superhost_scores']['median_a']:.2f}"),
                ("Group B median score", f"{results['superhost_scores']['median_b']:.2f}"),
                ("Group A mean score", f"{results['superhost_scores']['mean_a']:.2f}"),
                ("Group B mean score", f"{results['superhost_scores']['mean_b']:.2f}"),
                ("Mann-Whitney U statistic", f"{results['superhost_scores']['statistic']:,.2f}"),
                ("p-value", format_p_value(results["superhost_scores"]["p_value"])),
            ]
        ),
        "",
        "Business interpretation: This test does not provide evidence of a statistically significant difference in review scores between superhosts and non-superhosts. Review scores are highly clustered near the top, so small differences may be difficult to detect. Superhost status may still matter for trust and conversion, but this dataset and test do not show a clear review-score difference.",
        "",
        "## Test 3: Price Difference by Review Volume",
        "",
        result_table(
            [
                ("Group A", results["review_count_price"]["group_a"]),
                ("Group B", results["review_count_price"]["group_b"]),
                ("Group A count", f"{results['review_count_price']['count_a']:,}"),
                ("Group B count", f"{results['review_count_price']['count_b']:,}"),
                ("Group A median price", f"{results['review_count_price']['median_a']:,.2f}"),
                ("Group B median price", f"{results['review_count_price']['median_b']:,.2f}"),
                ("Mann-Whitney U statistic", f"{results['review_count_price']['statistic']:,.2f}"),
                ("p-value", format_p_value(results["review_count_price"]["p_value"])),
            ]
        ),
        "",
        "Business interpretation: Review count can indicate listing maturity or historical demand, but it is not the same as bookings. Any price difference by review volume should be treated as an association, not proof that reviews cause higher or lower prices.",
        "",
        "## Test 4: Neighbourhood Price Differences",
        "",
        result_table(
            [
                ("Minimum priced listings per neighbourhood", f"{results['neighbourhood_price']['min_priced_listings']:,}"),
                ("Eligible neighbourhood count", f"{results['neighbourhood_price']['eligible_neighbourhood_count']:,}"),
                ("Kruskal-Wallis statistic", f"{results['neighbourhood_price']['statistic']:,.2f}"),
                ("p-value", format_p_value(results["neighbourhood_price"]["p_value"])),
            ]
        ),
        "",
        "Top neighbourhood median prices among eligible neighbourhoods:",
        "",
        dataframe_to_markdown(results["neighbourhood_price"]["top_medians"]),
        "",
        "Business interpretation: Neighbourhood is associated with price differences and can be used for local pricing benchmarks. However, neighbourhood comparisons should still control for room type, property type, and listing capacity before making pricing recommendations.",
        "",
        "## Overall Interpretation",
        "",
        "- Room type, review-related signals, host status, and neighbourhood all provide useful segmentation lenses.",
        "- The tests are useful for prioritizing business questions, not for proving causal effects.",
        "- Future modeling should include room type and neighbourhood, and should treat missing listing prices explicitly.",
    ]

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def result_table(rows: list[tuple[str, str]]) -> str:
    """Format two-column result rows as Markdown."""
    lines = ["| Metric | Value |", "|---|---:|"]
    for metric, value in rows:
        lines.append(f"| {metric} | {value} |")
    return "\n".join(lines)


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """Format a small DataFrame as Markdown without optional dependencies."""
    output = ["| Neighbourhood | Priced listings | Median price |", "|---|---:|---:|"]
    for _, row in df.iterrows():
        output.append(
            f"| {clean_display_text(row['neighbourhood_cleansed'])} | {int(row['count']):,} | {row['median_price']:,.2f} |"
        )
    return "\n".join(output)


def clean_display_text(value: object) -> str:
    """Fix common UTF-8 mojibake in display labels without changing source data."""
    text = str(value)
    replacements = {
        "Ã…": "Å",
        "Ã„": "Ä",
        "Ã–": "Ö",
        "Ã¥": "å",
        "Ã¤": "ä",
        "Ã¶": "ö",
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text


def format_p_value(p_value: float) -> str:
    """Format p-values consistently for reports."""
    if p_value < 0.001:
        return "< 0.001"
    return f"{p_value:.4f}"


if __name__ == "__main__":
    main()
