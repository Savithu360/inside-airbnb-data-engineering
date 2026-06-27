"""Run Phase 2 exploratory data analysis for the Stockholm Inside Airbnb data."""

import os
import sqlite3
from pathlib import Path

import pandas as pd

from config import CITY_NAME, DATABASE_PATH, PROJECT_ROOT, REPORTS_DIR

os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / ".matplotlib-cache"))

import matplotlib.pyplot as plt
import seaborn as sns


FIGURES_DIR = REPORTS_DIR / "figures"
EDA_REPORT_PATH = REPORTS_DIR / "eda_report.md"
DATA_SOURCE = "Inside Airbnb"


def main() -> None:
    """Load processed data from SQLite, create figures, and write the EDA report."""
    print("Starting Phase 2 EDA")
    print(f"Selected city: {CITY_NAME}")
    print(f"Reading SQLite database: {DATABASE_PATH}")

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"SQLite database not found at {DATABASE_PATH}. Run python src/run_phase1_pipeline.py first."
        )

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DATABASE_PATH) as connection:
        listings = load_listings(connection)
        calendar = load_calendar_for_availability(connection)
        reviews = load_reviews_for_volume(connection)
        metrics = calculate_summary_metrics(connection, listings)

    print("[EDA] Creating analysis datasets")
    analysis = build_analysis_tables(listings, calendar, reviews)

    print("[EDA] Saving figures")
    figure_paths = create_all_figures(listings, calendar, reviews, analysis)

    print("[REPORT] Writing EDA report")
    write_eda_report(metrics, analysis, figure_paths)

    print("Phase 2 EDA completed successfully")
    print(f"EDA report saved to: {EDA_REPORT_PATH}")
    print(f"Figures saved to: {FIGURES_DIR}")


def load_listings(connection: sqlite3.Connection) -> pd.DataFrame:
    """Load only the listing columns needed for Phase 2 EDA."""
    query = """
        SELECT
            id,
            host_id,
            host_name,
            neighbourhood_cleansed,
            property_type,
            room_type,
            price,
            availability_365,
            number_of_reviews,
            review_scores_rating
        FROM listings_clean
    """
    return pd.read_sql_query(query, connection)


def load_calendar_for_availability(connection: sqlite3.Connection) -> pd.DataFrame:
    """Load calendar columns needed for availability analysis only."""
    query = """
        SELECT
            listing_id,
            date,
            available,
            minimum_nights,
            maximum_nights
        FROM calendar_clean
    """
    calendar = pd.read_sql_query(query, connection, parse_dates=["date"])
    calendar["available"] = calendar["available"].astype("Int64")
    return calendar


def load_reviews_for_volume(connection: sqlite3.Connection) -> pd.DataFrame:
    """Load review dates for monthly review-volume analysis."""
    query = "SELECT date FROM reviews_clean WHERE date IS NOT NULL"
    return pd.read_sql_query(query, connection, parse_dates=["date"])


def calculate_summary_metrics(connection: sqlite3.Connection, listings: pd.DataFrame) -> dict[str, float]:
    """Calculate key summary metrics using SQL where possible."""
    sql_metrics = pd.read_sql_query(
        """
        SELECT
            (SELECT COUNT(*) FROM listings_clean) AS total_listings,
            (SELECT COUNT(DISTINCT host_id) FROM listings_clean) AS total_hosts,
            (SELECT COUNT(*) FROM neighbourhoods_clean) AS total_neighbourhoods,
            (SELECT AVG(CASE WHEN available = 1 THEN 1.0 ELSE 0.0 END) * 100 FROM calendar_clean)
                AS pct_available_calendar_days,
            (SELECT AVG(CASE WHEN price IS NULL THEN 1.0 ELSE 0.0 END) * 100 FROM listings_clean)
                AS pct_listings_missing_price,
            (SELECT AVG(CASE WHEN price IS NULL THEN 1.0 ELSE 0.0 END) * 100 FROM calendar_clean)
                AS pct_calendar_missing_price,
            (SELECT AVG(CASE WHEN adjusted_price IS NULL THEN 1.0 ELSE 0.0 END) * 100 FROM calendar_clean)
                AS pct_calendar_missing_adjusted_price
        """,
        connection,
    ).iloc[0]

    metrics = sql_metrics.to_dict()
    metrics["median_listing_price"] = float(listings["price"].median())
    metrics["average_review_score"] = float(listings["review_scores_rating"].mean())
    return metrics


def build_analysis_tables(
    listings: pd.DataFrame,
    calendar: pd.DataFrame,
    reviews: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """Prepare grouped tables used by charts and report text."""
    priced_listings = listings.dropna(subset=["price"]).copy()
    price_cap_99 = priced_listings["price"].quantile(0.99)
    price_for_chart = priced_listings[priced_listings["price"] <= price_cap_99].copy()

    room_counts = listings["room_type"].value_counts(dropna=False).rename_axis("room_type").reset_index(name="count")
    room_prices = (
        priced_listings.groupby("room_type", dropna=False)["price"]
        .median()
        .sort_values(ascending=False)
        .reset_index(name="median_price")
    )

    top_neighbourhoods = listings["neighbourhood_cleansed"].value_counts().head(10).index
    neighbourhood_prices = (
        priced_listings[priced_listings["neighbourhood_cleansed"].isin(top_neighbourhoods)]
        .groupby("neighbourhood_cleansed")["price"]
        .median()
        .sort_values(ascending=False)
        .reset_index(name="median_price")
    )

    top_property_types = listings["property_type"].value_counts().head(10).index
    property_type_prices = (
        priced_listings[priced_listings["property_type"].isin(top_property_types)]
        .groupby("property_type")["price"]
        .median()
        .sort_values(ascending=False)
        .reset_index(name="median_price")
    )

    availability_counts = (
        calendar["available"]
        .map({1: "Available", 0: "Unavailable"})
        .value_counts()
        .rename_axis("availability_status")
        .reset_index(name="count")
    )

    calendar["month"] = calendar["date"].dt.to_period("M").dt.to_timestamp()
    monthly_availability = (
        calendar.groupby("month")["available"]
        .mean()
        .mul(100)
        .reset_index(name="availability_rate")
    )

    calendar_room = calendar.merge(
        listings[["id", "room_type"]],
        left_on="listing_id",
        right_on="id",
        how="left",
    )
    availability_by_room_type = (
        calendar_room.groupby("room_type")["available"]
        .mean()
        .mul(100)
        .sort_values(ascending=False)
        .reset_index(name="availability_rate")
    )

    top_hosts = (
        listings.groupby(["host_id", "host_name"], dropna=False)
        .size()
        .sort_values(ascending=False)
        .head(10)
        .reset_index(name="listing_count")
    )
    top_hosts["host_label"] = top_hosts["host_name"].fillna("Unknown") + " (" + top_hosts["host_id"].astype(str) + ")"

    host_listing_counts = listings.groupby("host_id").size().rename("host_listing_count").reset_index()
    host_listing_counts["host_segment"] = host_listing_counts["host_listing_count"].apply(assign_host_segment)
    listings_with_segments = listings.merge(host_listing_counts, on="host_id", how="left")
    host_segment_counts = (
        host_listing_counts["host_segment"]
        .value_counts()
        .reindex(["single-listing hosts", "small multi-listing hosts", "professional hosts"])
        .fillna(0)
        .astype(int)
        .rename_axis("host_segment")
        .reset_index(name="host_count")
    )
    host_segment_price = (
        listings_with_segments.dropna(subset=["price"])
        .groupby("host_segment")["price"]
        .median()
        .reindex(["single-listing hosts", "small multi-listing hosts", "professional hosts"])
        .reset_index(name="median_price")
    )

    review_scores = listings.dropna(subset=["review_scores_rating"]).copy()
    neighbourhood_review_scores = (
        review_scores.groupby("neighbourhood_cleansed")
        .agg(avg_review_score=("review_scores_rating", "mean"), listing_count=("id", "count"))
        .query("listing_count >= 20")
        .sort_values("avg_review_score", ascending=False)
        .head(10)
        .reset_index()
    )

    reviews["month"] = reviews["date"].dt.to_period("M").dt.to_timestamp()
    reviews_by_month = reviews.groupby("month").size().reset_index(name="review_count")

    price_vs_reviews = price_for_chart[["number_of_reviews", "price", "room_type"]].copy()

    return {
        "priced_listings": priced_listings,
        "price_for_chart": price_for_chart,
        "price_cap_99": pd.DataFrame({"price_cap_99": [price_cap_99]}),
        "room_counts": room_counts,
        "room_prices": room_prices,
        "neighbourhood_prices": neighbourhood_prices,
        "property_type_prices": property_type_prices,
        "availability_counts": availability_counts,
        "monthly_availability": monthly_availability,
        "availability_by_room_type": availability_by_room_type,
        "top_hosts": top_hosts,
        "host_segment_counts": host_segment_counts,
        "host_segment_price": host_segment_price,
        "neighbourhood_review_scores": neighbourhood_review_scores,
        "reviews_by_month": reviews_by_month,
        "price_vs_reviews": price_vs_reviews,
    }


def assign_host_segment(listing_count: int) -> str:
    """Convert a host listing count into a simple business segment."""
    if listing_count == 1:
        return "single-listing hosts"
    if listing_count <= 5:
        return "small multi-listing hosts"
    return "professional hosts"


def create_all_figures(
    listings: pd.DataFrame,
    calendar: pd.DataFrame,
    reviews: pd.DataFrame,
    analysis: dict[str, pd.DataFrame],
) -> dict[str, Path]:
    """Create and save all required charts."""
    sns.set_theme(style="whitegrid")
    figure_paths = {}

    figure_paths["listings_by_room_type"] = save_bar_chart(
        analysis["room_counts"],
        x="count",
        y="room_type",
        title="Listings by Room Type",
        xlabel="Number of listings",
        ylabel="Room type",
        filename="listings_by_room_type.png",
    )
    figure_paths["median_price_by_room_type"] = save_bar_chart(
        analysis["room_prices"],
        x="median_price",
        y="room_type",
        title="Median Listing Price by Room Type",
        xlabel="Median listing price",
        ylabel="Room type",
        filename="median_price_by_room_type.png",
    )
    figure_paths["listing_price_distribution_capped"] = save_histogram(
        analysis["price_for_chart"],
        column="price",
        title="Listing Price Distribution, Capped at 99th Percentile for Visualization",
        xlabel="Listing price",
        filename="listing_price_distribution_capped.png",
    )
    figure_paths["median_price_top_neighbourhoods"] = save_bar_chart(
        analysis["neighbourhood_prices"],
        x="median_price",
        y="neighbourhood_cleansed",
        title="Median Listing Price by Top 10 Neighbourhoods",
        xlabel="Median listing price",
        ylabel="Neighbourhood",
        filename="median_price_top_neighbourhoods.png",
    )
    figure_paths["median_price_by_property_type"] = save_bar_chart(
        analysis["property_type_prices"],
        x="median_price",
        y="property_type",
        title="Median Listing Price by Top Property Types",
        xlabel="Median listing price",
        ylabel="Property type",
        filename="median_price_by_property_type.png",
    )
    figure_paths["availability_counts"] = save_bar_chart(
        analysis["availability_counts"],
        x="count",
        y="availability_status",
        title="Available vs Unavailable Calendar Days",
        xlabel="Calendar rows",
        ylabel="Availability status",
        filename="availability_counts.png",
    )
    figure_paths["availability_by_month"] = save_line_chart(
        analysis["monthly_availability"],
        x="month",
        y="availability_rate",
        title="Average Availability Rate by Month",
        xlabel="Month",
        ylabel="Availability rate (%)",
        filename="availability_by_month.png",
    )
    figure_paths["availability_by_room_type"] = save_bar_chart(
        analysis["availability_by_room_type"],
        x="availability_rate",
        y="room_type",
        title="Availability Rate by Room Type",
        xlabel="Availability rate (%)",
        ylabel="Room type",
        filename="availability_by_room_type.png",
    )
    figure_paths["top_hosts_by_listings"] = save_bar_chart(
        analysis["top_hosts"].sort_values("listing_count"),
        x="listing_count",
        y="host_label",
        title="Top 10 Hosts by Number of Listings",
        xlabel="Number of listings",
        ylabel="Host",
        filename="top_hosts_by_listings.png",
    )
    figure_paths["host_segment_price"] = save_bar_chart(
        analysis["host_segment_price"],
        x="median_price",
        y="host_segment",
        title="Median Listing Price by Host Segment",
        xlabel="Median listing price",
        ylabel="Host segment",
        filename="host_segment_price.png",
    )
    figure_paths["review_score_distribution"] = save_histogram(
        listings.dropna(subset=["review_scores_rating"]),
        column="review_scores_rating",
        title="Review Score Distribution",
        xlabel="Review score rating",
        filename="review_score_distribution.png",
    )
    figure_paths["top_neighbourhood_review_scores"] = save_bar_chart(
        analysis["neighbourhood_review_scores"],
        x="avg_review_score",
        y="neighbourhood_cleansed",
        title="Top Neighbourhoods by Average Review Score",
        xlabel="Average review score",
        ylabel="Neighbourhood",
        filename="top_neighbourhood_review_scores.png",
    )
    figure_paths["reviews_by_month"] = save_line_chart(
        analysis["reviews_by_month"],
        x="month",
        y="review_count",
        title="Review Volume by Month",
        xlabel="Month",
        ylabel="Number of reviews",
        filename="reviews_by_month.png",
    )
    figure_paths["price_vs_reviews"] = save_scatter_plot(
        analysis["price_vs_reviews"],
        x="number_of_reviews",
        y="price",
        title="Listing Price vs Number of Reviews",
        xlabel="Number of reviews",
        ylabel="Listing price",
        filename="price_vs_reviews.png",
    )

    # The arguments are intentionally used above; these names make the function call self-documenting.
    _ = calendar, reviews
    return figure_paths


def save_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    xlabel: str,
    ylabel: str,
    filename: str,
) -> Path:
    """Save a horizontal bar chart."""
    path = FIGURES_DIR / filename
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x=x, y=y, color="#4C78A8")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def save_histogram(df: pd.DataFrame, column: str, title: str, xlabel: str, filename: str) -> Path:
    """Save a histogram."""
    path = FIGURES_DIR / filename
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x=column, bins=40, color="#59A14F")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def save_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    xlabel: str,
    ylabel: str,
    filename: str,
) -> Path:
    """Save a line chart."""
    path = FIGURES_DIR / filename
    plt.figure(figsize=(11, 6))
    sns.lineplot(data=df, x=x, y=y, marker="o", color="#F28E2B")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def save_scatter_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    xlabel: str,
    ylabel: str,
    filename: str,
) -> Path:
    """Save a scatter plot."""
    path = FIGURES_DIR / filename
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=x, y=y, alpha=0.45, color="#9C755F", edgecolor=None)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def write_eda_report(metrics: dict[str, float], analysis: dict[str, pd.DataFrame], figure_paths: dict[str, Path]) -> None:
    """Write a Markdown report with chart findings and business interpretations."""
    price_cap = analysis["price_cap_99"]["price_cap_99"].iloc[0]
    top_room_type = analysis["room_counts"].iloc[0]
    highest_price_room = analysis["room_prices"].iloc[0]
    top_neighbourhood = analysis["neighbourhood_prices"].iloc[0]
    top_property_type = analysis["property_type_prices"].iloc[0]
    availability = analysis["availability_counts"]
    highest_availability_room = analysis["availability_by_room_type"].iloc[0]
    top_host = analysis["top_hosts"].iloc[0]
    highest_host_segment_price = analysis["host_segment_price"].sort_values("median_price", ascending=False).iloc[0]
    top_review_neighbourhood = analysis["neighbourhood_review_scores"].iloc[0]

    lines = [
        "# Phase 2 Exploratory Data Analysis Report",
        "",
        f"Selected city: {CITY_NAME}",
        "",
        f"Data source: {DATA_SOURCE}",
        "",
        "## Phase 2 EDA Scope",
        "",
        "This report explores the cleaned Stockholm Inside Airbnb data from the Phase 1 SQLite database. "
        "The focus is business-friendly analysis of listings, listing prices, availability, hosts, and reviews. "
        "Machine learning is handled separately in the Phase 2 ML baseline script.",
        "",
        "## Important Dataset Limitation",
        "",
        "The Stockholm calendar dataset contains 100% missing values for price and adjusted_price in the raw source file. "
        "Therefore, calendar-based pricing analysis such as monthly price trends and weekday vs weekend price comparison "
        "cannot be performed using calendar data. Calendar data is used for availability analysis only, while pricing "
        "analysis uses `listings_clean.price`.",
        "",
        "## Key Summary Metrics",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Total listings | {metrics['total_listings']:,.0f} |",
        f"| Total hosts | {metrics['total_hosts']:,.0f} |",
        f"| Total neighbourhoods | {metrics['total_neighbourhoods']:,.0f} |",
        f"| Median listing price | {metrics['median_listing_price']:,.2f} |",
        f"| Average review score | {metrics['average_review_score']:.2f} |",
        f"| Available calendar days | {metrics['pct_available_calendar_days']:.2f}% |",
        f"| Listings with missing price | {metrics['pct_listings_missing_price']:.2f}% |",
        f"| Calendar rows with missing price | {metrics['pct_calendar_missing_price']:.2f}% |",
        f"| Calendar rows with missing adjusted_price | {metrics['pct_calendar_missing_adjusted_price']:.2f}% |",
        "",
        f"Pricing note: All price-based analysis uses `listings_clean.price`, in the source dataset currency. Because {metrics['pct_listings_missing_price']:.2f}% of listings have missing price values, price-based charts and medians exclude listings where price is missing. No calendar prices are filled, imputed, or used.",
        "",
        "## Chart Findings and Business Interpretations",
        "",
        "### Listings by Room Type",
        "",
        f"![Listings by room type]({figure_paths['listings_by_room_type'].relative_to(REPORTS_DIR).as_posix()})",
        "",
        f"Finding: `{top_room_type['room_type']}` is the largest room-type category with {top_room_type['count']:,.0f} listings.",
        "",
        "Business interpretation: The largest room-type category represents the main supply pattern in Stockholm. "
        "Hosts, analysts, and marketplace operators should treat this segment as the baseline when comparing pricing, "
        "availability, and guest demand.",
        "",
        "### Median Listing Price by Room Type",
        "",
        f"![Median price by room type]({figure_paths['median_price_by_room_type'].relative_to(REPORTS_DIR).as_posix()})",
        "",
        f"Finding: `{highest_price_room['room_type']}` has the highest median listing price at "
        f"{highest_price_room['median_price']:,.2f}.",
        "",
        "Business interpretation: Room type is a major pricing driver. Price comparisons should be segmented by room type "
        "so that private rooms are not compared directly with entire homes or other fundamentally different products.",
        "",
        "### Listing Price Distribution",
        "",
        f"![Listing price distribution]({figure_paths['listing_price_distribution_capped'].relative_to(REPORTS_DIR).as_posix()})",
        "",
        f"Finding: The chart uses listings prices capped at the 99th percentile ({price_cap:,.2f}) for visualization only. "
        "The source data is not modified.",
        "",
        "Business interpretation: The distribution helps identify the common price range for typical listings while avoiding "
        "a small number of extreme values making the chart unreadable. Any future outlier handling should be documented "
        "as an analysis decision, not hidden as data cleaning.",
        "",
        "### Median Price by Top 10 Neighbourhoods",
        "",
        f"![Median price by neighbourhood]({figure_paths['median_price_top_neighbourhoods'].relative_to(REPORTS_DIR).as_posix()})",
        "",
        f"Finding: Among the top 10 neighbourhoods by listing count, `{top_neighbourhood['neighbourhood_cleansed']}` has "
        f"the highest median listing price at {top_neighbourhood['median_price']:,.2f}.",
        "",
        "Business interpretation: Neighbourhood affects pricing. This is useful for market positioning, but it should be "
        "combined with room type and property type before making pricing recommendations.",
        "",
        "### Median Price by Property Type",
        "",
        f"![Median price by property type]({figure_paths['median_price_by_property_type'].relative_to(REPORTS_DIR).as_posix()})",
        "",
        f"Finding: Among common property types, `{top_property_type['property_type']}` has the highest median listing price "
        f"at {top_property_type['median_price']:,.2f}.",
        "",
        "Business interpretation: Property type adds important context beyond neighbourhood. A compact apartment and a house "
        "in the same area may have very different expected prices.",
        "",
        "### Available vs Unavailable Calendar Days",
        "",
        f"![Availability counts]({figure_paths['availability_counts'].relative_to(REPORTS_DIR).as_posix()})",
        "",
        f"Finding: Calendar availability is {metrics['pct_available_calendar_days']:.2f}% across all calendar rows.",
        "",
        "Business interpretation: Availability gives a rough view of supply still open to guests. It should not be treated "
        "as occupancy without stronger assumptions, because unavailable days may mean booked, blocked, or otherwise inactive.",
        "",
        "### Monthly Availability Trend",
        "",
        f"![Availability by month]({figure_paths['availability_by_month'].relative_to(REPORTS_DIR).as_posix()})",
        "",
        "Finding: Monthly availability changes over the calendar period, showing how open supply varies by month.",
        "",
        "Business interpretation: Seasonal availability patterns can inform when supply pressure may be higher or lower. "
        "Because calendar prices are missing, this trend should not be combined with calendar-based price trends.",
        "",
        "### Availability by Room Type",
        "",
        f"![Availability by room type]({figure_paths['availability_by_room_type'].relative_to(REPORTS_DIR).as_posix()})",
        "",
        f"Finding: `{highest_availability_room['room_type']}` has the highest availability rate at "
        f"{highest_availability_room['availability_rate']:.2f}%.",
        "",
        "Business interpretation: Availability differs by product type. Higher availability may indicate more flexible supply, "
        "lower demand, or hosts leaving more dates open.",
        "",
        "### Top Hosts by Number of Listings",
        "",
        f"![Top hosts]({figure_paths['top_hosts_by_listings'].relative_to(REPORTS_DIR).as_posix()})",
        "",
        f"Finding: The top host in this data is `{top_host['host_name']}` with {top_host['listing_count']:,.0f} listings.",
        "",
        "Business interpretation: A small set of hosts with many listings can influence marketplace supply. Segmenting hosts "
        "helps distinguish occasional hosts from more professional operators.",
        "",
        "### Median Price by Host Segment",
        "",
        "Host portfolio segmentation:",
        "",
        "| Host segment | Host count |",
        "|---|---:|",
        *[
            f"| {row['host_segment']} | {row['host_count']:,.0f} |"
            for _, row in analysis["host_segment_counts"].iterrows()
        ],
        "",
        f"![Host segment price]({figure_paths['host_segment_price'].relative_to(REPORTS_DIR).as_posix()})",
        "",
        f"Finding: `{highest_host_segment_price['host_segment']}` have the highest median listing price at "
        f"{highest_host_segment_price['median_price']:,.2f}.",
        "",
        "Business interpretation: Host portfolio size may be related to pricing strategy. This does not prove causation, "
        "but it is a useful segmentation for Phase 2 statistical testing.",
        "",
        "### Review Score Distribution",
        "",
        f"![Review score distribution]({figure_paths['review_score_distribution'].relative_to(REPORTS_DIR).as_posix()})",
        "",
        f"Finding: The average review score is {metrics['average_review_score']:.2f}.",
        "",
        "Business interpretation: Review scores are generally useful for quality positioning, but they often cluster near "
        "high values. Future analysis should check whether score differences are large enough to be meaningful.",
        "",
        "### Price vs Number of Reviews",
        "",
        f"![Price vs reviews]({figure_paths['price_vs_reviews'].relative_to(REPORTS_DIR).as_posix()})",
        "",
        "Finding: The scatter plot compares listing price with review volume using listings prices only.",
        "",
        "Business interpretation: Review count can act as a rough demand or listing-age signal, but it is not the same as "
        "booking volume. Strong claims should wait for statistical testing.",
        "",
        "### Top Neighbourhoods by Average Review Score",
        "",
        f"![Top neighbourhood review scores]({figure_paths['top_neighbourhood_review_scores'].relative_to(REPORTS_DIR).as_posix()})",
        "",
        f"Finding: Among neighbourhoods with at least 20 scored listings, `{top_review_neighbourhood['neighbourhood_cleansed']}` "
        f"has the highest average review score at {top_review_neighbourhood['avg_review_score']:.2f}.",
        "",
        "Business interpretation: This can help identify areas with consistently strong guest satisfaction, but sample-size "
        "rules are important so small neighbourhoods do not dominate by chance.",
        "",
        "### Review Volume by Month",
        "",
        f"![Reviews by month]({figure_paths['reviews_by_month'].relative_to(REPORTS_DIR).as_posix()})",
        "",
        "Finding: Review volume varies over time and can be used as a rough signal of historical guest activity.",
        "",
        "Business interpretation: Reviews are delayed and incomplete compared with bookings, but they can still reveal demand "
        "seasonality and platform activity patterns.",
        "",
        "## Limitations",
        "",
        "- Calendar `price` and `adjusted_price` are 100% missing, so calendar-based pricing analysis is not possible.",
        f"- {metrics['pct_listings_missing_price']:.2f}% of listings have missing `price` values, so price-based analysis excludes those listings.",
        "- Prices are based on `listings_clean.price` and are reported in the source dataset currency.",
        "- Availability does not equal occupancy because unavailable dates may be booked, blocked, or inactive.",
        "- Review count is not the same as booking count.",
        "- The 99th percentile price cap is used only for visualization, not as a source-data change.",
        "- This is descriptive EDA only; it does not prove causal relationships.",
        "",
        "## Recommendations",
        "",
        "- Use `listings_clean.price` as the pricing source and clearly exclude missing prices from price-based calculations.",
        "- Segment pricing benchmarks by room type before comparing listings, because entire homes, private rooms, and shared rooms represent different products.",
        "- Use neighbourhood-level median prices as local benchmarks, but compare neighbourhoods together with room type and property type to avoid misleading pricing conclusions.",
        "- Use `calendar_clean` for availability analysis only. Interpret availability carefully because unavailable dates may reflect bookings, host blocks, or inactive inventory.",
        "- Use ML results as directional support only, not automated pricing decisions.",
        "- Keep the calendar price limitation visible in any presentation or interview discussion, especially when explaining why monthly price trends and weekday versus weekend pricing are not included.",
        "",
        "## Follow-Up Analysis Steps",
        "",
        "- Perform simple statistical tests for price differences by room type and host segment.",
        "- Build a simple ML baseline only after defining a clear target and feature table.",
        "- Add reusable SQL queries for common analysis metrics.",
        "- Validate whether missing listing prices should be excluded or handled explicitly in later analysis.",
    ]

    EDA_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
