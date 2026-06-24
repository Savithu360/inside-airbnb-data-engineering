"""Cleaning functions for the Day 1 processed Airbnb tables."""

import re

import pandas as pd


LISTINGS_COLUMNS = [
    "id",
    "name",
    "host_id",
    "host_name",
    "host_since",
    "host_is_superhost",
    "host_response_rate",
    "host_acceptance_rate",
    "host_listings_count",
    "neighbourhood_cleansed",
    "latitude",
    "longitude",
    "property_type",
    "room_type",
    "accommodates",
    "bathrooms",
    "bedrooms",
    "beds",
    "amenities",
    "price",
    "minimum_nights",
    "maximum_nights",
    "availability_365",
    "number_of_reviews",
    "review_scores_rating",
    "review_scores_cleanliness",
    "review_scores_location",
    "review_scores_communication",
    "instant_bookable",
]

CALENDAR_COLUMNS = [
    "listing_id",
    "date",
    "available",
    "price",
    "adjusted_price",
    "minimum_nights",
    "maximum_nights",
]

REVIEWS_COLUMNS = [
    "listing_id",
    "review_id",
    "date",
    "reviewer_id",
    "reviewer_name",
    "comments",
]


def clean_all_datasets(datasets: dict[str, pd.DataFrame]) -> tuple[dict[str, pd.DataFrame], dict[str, list[str]]]:
    """Clean all datasets and collect plain-English cleaning notes."""
    cleaned = {}
    actions = {}

    cleaned["listings"], actions["listings"] = clean_listings(datasets.get("listings", pd.DataFrame()))
    cleaned["calendar"], actions["calendar"] = clean_calendar(datasets.get("calendar", pd.DataFrame()))
    cleaned["reviews"], actions["reviews"] = clean_reviews(datasets.get("reviews", pd.DataFrame()))
    cleaned["neighbourhoods"], actions["neighbourhoods"] = clean_neighbourhoods(
        datasets.get("neighbourhoods", pd.DataFrame())
    )

    return cleaned, actions


def clean_listings(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Clean the listings table and keep the assignment's important columns."""
    actions = []
    if df.empty:
        return pd.DataFrame(columns=LISTINGS_COLUMNS), ["Source file was missing or empty."]

    cleaned = df.copy()

    for column in ["price"]:
        if column in cleaned.columns:
            cleaned[column] = _money_to_number(cleaned[column])
            actions.append(f"Converted {column} to numeric.")

    for column in ["host_response_rate", "host_acceptance_rate"]:
        if column in cleaned.columns:
            cleaned[column] = _percent_to_number(cleaned[column])
            actions.append(f"Removed percent signs and converted {column} to numeric.")

    for column in ["host_is_superhost", "instant_bookable"]:
        if column in cleaned.columns:
            cleaned[column] = _tf_to_boolean(cleaned[column])
            actions.append(f"Converted {column} from t/f to boolean.")

    for column in ["host_since", "first_review", "last_review"]:
        if column in cleaned.columns:
            cleaned[column] = pd.to_datetime(cleaned[column], errors="coerce")
            actions.append(f"Converted {column} to datetime.")

    if "latitude" in cleaned.columns:
        cleaned["invalid_latitude"] = ~cleaned["latitude"].between(-90, 90)
    if "longitude" in cleaned.columns:
        cleaned["invalid_longitude"] = ~cleaned["longitude"].between(-180, 180)
    if "price" in cleaned.columns:
        cleaned["invalid_price"] = cleaned["price"].le(0).fillna(False)
        actions.append("Flagged listing prices less than or equal to zero.")

    cleaned = _ensure_columns(cleaned, LISTINGS_COLUMNS + ["invalid_latitude", "invalid_longitude", "invalid_price"])
    return cleaned, actions


def clean_calendar(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Clean the calendar table."""
    actions = []
    if df.empty:
        return pd.DataFrame(columns=CALENDAR_COLUMNS), ["Source file was missing or empty."]

    cleaned = df.copy()

    if "date" in cleaned.columns:
        cleaned["date"] = pd.to_datetime(cleaned["date"], errors="coerce")
        actions.append("Converted date to datetime.")

    if "available" in cleaned.columns:
        cleaned["available"] = _tf_to_boolean(cleaned["available"])
        actions.append("Converted available from t/f to boolean.")

    for column in ["price", "adjusted_price"]:
        if column in cleaned.columns:
            cleaned[column] = _money_to_number(cleaned[column])
            actions.append(f"Converted {column} to numeric.")

    if "price" in cleaned.columns:
        cleaned["invalid_price"] = cleaned["price"].le(0).fillna(False)
        actions.append("Flagged calendar prices less than or equal to zero.")

    cleaned = _ensure_columns(cleaned, CALENDAR_COLUMNS + ["invalid_price"])
    return cleaned, actions


def clean_reviews(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Clean the reviews table."""
    actions = []
    if df.empty:
        return pd.DataFrame(columns=REVIEWS_COLUMNS), ["Source file was missing or empty."]

    cleaned = df.copy()

    if "id" in cleaned.columns and "review_id" not in cleaned.columns:
        cleaned = cleaned.rename(columns={"id": "review_id"})
        actions.append("Renamed id to review_id.")

    if "date" in cleaned.columns:
        cleaned["date"] = pd.to_datetime(cleaned["date"], errors="coerce")
        actions.append("Converted date to datetime.")

    cleaned = _ensure_columns(cleaned, REVIEWS_COLUMNS)
    return cleaned, actions


def clean_neighbourhoods(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Clean the neighbourhood reference table."""
    if df.empty:
        return pd.DataFrame(), ["Source file was missing or empty."]

    cleaned = df.copy()
    cleaned.columns = [_clean_column_name(column) for column in cleaned.columns]
    return cleaned, ["Cleaned neighbourhood column names."]


def _ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Add missing expected columns as null and return columns in a stable order."""
    for column in columns:
        if column not in df.columns:
            df[column] = pd.NA
    return df[columns]


def _money_to_number(series: pd.Series) -> pd.Series:
    """Convert values like '$1,234.00' to floats."""
    return pd.to_numeric(series.astype(str).str.replace(r"[$,]", "", regex=True), errors="coerce")


def _percent_to_number(series: pd.Series) -> pd.Series:
    """Convert values like '98%' to 98.0."""
    return pd.to_numeric(series.astype(str).str.replace("%", "", regex=False), errors="coerce")


def _tf_to_boolean(series: pd.Series) -> pd.Series:
    """Convert Inside Airbnb t/f fields to pandas nullable booleans."""
    return series.map({"t": True, "f": False, True: True, False: False}).astype("boolean")


def _clean_column_name(column: str) -> str:
    """Make a column name lowercase and underscore-separated."""
    cleaned = re.sub(r"[^0-9a-zA-Z]+", "_", column.strip().lower())
    return cleaned.strip("_")
