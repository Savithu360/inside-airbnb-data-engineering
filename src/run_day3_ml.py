"""Run a simple Day 3 listing price prediction baseline."""

import os
import sqlite3

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from config import CITY_NAME, DATABASE_PATH, PROJECT_ROOT, REPORTS_DIR


os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / ".matplotlib-cache"))

import matplotlib.pyplot as plt
import seaborn as sns

FIGURES_DIR = REPORTS_DIR / "figures"
REPORT_PATH = REPORTS_DIR / "ml_experiment_report.md"
MODEL_COMPARISON_PATH = FIGURES_DIR / "ml_model_comparison.png"
FEATURE_IMPORTANCE_PATH = FIGURES_DIR / "ml_feature_importance.png"

CATEGORICAL_FEATURES = ["room_type", "property_type", "neighbourhood_cleansed"]
NUMERIC_FEATURES = [
    "accommodates",
    "bedrooms",
    "bathrooms",
    "beds",
    "minimum_nights",
    "maximum_nights",
    "availability_365",
    "number_of_reviews",
    "review_scores_rating",
    "host_is_superhost",
    "host_listings_count",
    "instant_bookable",
]
FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES


def main() -> None:
    """Train simple baseline models and write an experiment report."""
    print("Starting Day 3 ML baseline")
    print(f"Selected city: {CITY_NAME}")

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_PATH}. Run Day 1 first.")

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    listings = load_modeling_data()
    prepared, prep_notes = prepare_modeling_data(listings)
    results, trained_models, split_data = train_and_evaluate_models(prepared)
    best_tree_model_name = choose_best_tree_model(results)
    feature_importance = get_feature_importance(trained_models[best_tree_model_name])

    save_model_comparison_figure(results)
    save_feature_importance_figure(feature_importance)
    write_report(listings, prepared, prep_notes, results, best_tree_model_name, feature_importance)

    print(f"ML experiment report saved to: {REPORT_PATH}")
    print(f"Model comparison figure saved to: {MODEL_COMPARISON_PATH}")
    print(f"Feature importance figure saved to: {FEATURE_IMPORTANCE_PATH}")
    _ = split_data


def load_modeling_data() -> pd.DataFrame:
    """Load only fields needed for the baseline model."""
    columns = ", ".join(["price"] + FEATURES)
    query = f"SELECT {columns} FROM listings_clean"
    with sqlite3.connect(DATABASE_PATH) as connection:
        return pd.read_sql_query(query, connection)


def prepare_modeling_data(listings: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Exclude missing targets and cap extreme prices for modeling only."""
    total_rows = len(listings)
    missing_price_rows = int(listings["price"].isna().sum())
    priced = listings.dropna(subset=["price"]).copy()

    price_cap_99 = priced["price"].quantile(0.99)
    prepared = priced[priced["price"] <= price_cap_99].copy()
    removed_extreme_rows = len(priced) - len(prepared)

    notes = {
        "total_rows": total_rows,
        "missing_price_rows": missing_price_rows,
        "missing_price_pct": missing_price_rows / total_rows * 100,
        "price_cap_99": float(price_cap_99),
        "removed_extreme_rows": removed_extreme_rows,
        "modeling_rows": len(prepared),
    }
    return prepared, notes


def train_and_evaluate_models(data: pd.DataFrame) -> tuple[pd.DataFrame, dict, tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]]:
    """Train baseline models and return comparison metrics."""
    X = data[FEATURES]
    y = data["price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    models = {
        "Median price baseline": DummyRegressor(strategy="median"),
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(
            n_estimators=200,
            random_state=42,
            min_samples_leaf=5,
            n_jobs=-1,
        ),
        "Gradient Boosting Regressor": GradientBoostingRegressor(random_state=42),
    }

    results = []
    trained_models = {}
    for name, model in models.items():
        pipeline = Pipeline(
            steps=[
                ("preprocess", build_preprocessor()),
                ("model", model),
            ]
        )
        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)
        results.append(
            {
                "model": name,
                "MAE": mean_absolute_error(y_test, predictions),
                "RMSE": mean_squared_error(y_test, predictions) ** 0.5,
                "R2": r2_score(y_test, predictions),
            }
        )
        trained_models[name] = pipeline

    results_df = pd.DataFrame(results).sort_values("MAE").reset_index(drop=True)
    return results_df, trained_models, (X_train, X_test, y_train, y_test)


def build_preprocessor() -> ColumnTransformer:
    """Create simple preprocessing for numeric and categorical features."""
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, NUMERIC_FEATURES),
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )


def choose_best_tree_model(results: pd.DataFrame) -> str:
    """Select the best tree-based model by MAE for feature importance."""
    tree_results = results[results["model"].isin(["Random Forest Regressor", "Gradient Boosting Regressor"])]
    return tree_results.sort_values("MAE").iloc[0]["model"]


def get_feature_importance(model: Pipeline) -> pd.DataFrame:
    """Extract feature importance from a fitted tree-based pipeline."""
    preprocessor = model.named_steps["preprocess"]
    estimator = model.named_steps["model"]
    feature_names = list(preprocessor.get_feature_names_out())
    importances = estimator.feature_importances_

    feature_importance = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": importances,
        }
    )
    feature_importance["feature"] = (
        feature_importance["feature"]
        .str.replace("numeric__", "", regex=False)
        .str.replace("categorical__", "", regex=False)
    )
    feature_importance["feature"] = feature_importance["feature"].map(clean_display_text)
    return feature_importance.sort_values("importance", ascending=False).head(15)


def clean_display_text(value: object) -> str:
    """Fix common UTF-8 mojibake in report labels without changing source data."""
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


def save_model_comparison_figure(results: pd.DataFrame) -> None:
    """Save a model comparison chart using MAE."""
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))
    plot_data = results.sort_values("MAE", ascending=False)
    sns.barplot(data=plot_data, x="MAE", y="model", color="#4C78A8")
    plt.title("ML Baseline Model Comparison by MAE")
    plt.xlabel("Mean Absolute Error")
    plt.ylabel("Model")
    plt.tight_layout()
    plt.savefig(MODEL_COMPARISON_PATH, dpi=150)
    plt.close()


def save_feature_importance_figure(feature_importance: pd.DataFrame) -> None:
    """Save feature importance chart for the best tree-based model."""
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 7))
    plot_data = feature_importance.sort_values("importance", ascending=True)
    sns.barplot(data=plot_data, x="importance", y="feature", color="#59A14F")
    plt.title("Top Feature Importances From Best Tree-Based Model")
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.tight_layout()
    plt.savefig(FEATURE_IMPORTANCE_PATH, dpi=150)
    plt.close()


def write_report(
    listings: pd.DataFrame,
    prepared: pd.DataFrame,
    prep_notes: dict,
    results: pd.DataFrame,
    best_tree_model_name: str,
    feature_importance: pd.DataFrame,
) -> None:
    """Write the ML experiment report."""
    best_model = results.iloc[0]
    lines = [
        "# Day 3 ML Baseline Experiment Report",
        "",
        f"Selected city: {CITY_NAME}",
        "",
        "Data source: Inside Airbnb",
        "",
        "## Problem Framing",
        "",
        "This experiment builds a simple baseline model to predict listing price from cleaned listing attributes. It is intended as a learning and assessment baseline, not as a production pricing system.",
        "",
        "## Target Variable",
        "",
        "- Target: `price` from `listings_clean`.",
        "- Calendar `price` and `adjusted_price` are not used because they are 100% missing in the raw Stockholm calendar data.",
        "",
        "## Features Used",
        "",
        ", ".join(f"`{feature}`" for feature in FEATURES),
        "",
        "## Preprocessing Steps",
        "",
        f"- Started with {prep_notes['total_rows']:,} listing rows.",
        f"- Excluded {prep_notes['missing_price_rows']:,} rows with missing price ({prep_notes['missing_price_pct']:.2f}%).",
        f"- Removed {prep_notes['removed_extreme_rows']:,} rows above the 99th percentile price cap ({prep_notes['price_cap_99']:,.2f}) for modeling only.",
        f"- Final modeling row count: {prep_notes['modeling_rows']:,}.",
        "- Numeric features use median imputation.",
        "- Categorical features use most-frequent imputation and one-hot encoding.",
        "- Source data is not modified.",
        "",
        "## Model Comparison Results",
        "",
        dataframe_to_markdown(results),
        "",
        f"![ML model comparison](figures/{MODEL_COMPARISON_PATH.name})",
        "",
        "## Best Model",
        "",
        f"Best model by MAE: `{best_model['model']}`.",
        "",
        f"- MAE: {best_model['MAE']:,.2f}",
        f"- RMSE: {best_model['RMSE']:,.2f}",
        f"- R2: {best_model['R2']:.4f}",
        "",
        f"Feature importance is shown for the best tree-based model: `{best_tree_model_name}`.",
        "",
        f"![ML feature importance](figures/{FEATURE_IMPORTANCE_PATH.name})",
        "",
        "Top feature importances:",
        "",
        feature_importance_to_markdown(feature_importance),
        "",
        "## Business Interpretation",
        "",
        "The baseline results show whether simple listing attributes contain useful signal for estimating price. Features such as room type, property type, neighbourhood, capacity, and review-related fields are practical pricing signals, but model outputs should support human judgment rather than replace it.",
        "",
        "## Limitations",
        "",
        "- This is a simple baseline, not a production model.",
        "- Rows with missing listing prices are excluded.",
        "- Extreme prices above the 99th percentile are removed for modeling only to reduce distortion.",
        "- Calendar prices are not used.",
        "- The model does not include external demand, events, seasonality, competitor prices, or true booking data.",
        "- Feature importance in tree models is directional guidance, not causal explanation.",
        "",
        "## Why This Is Not Production-Ready",
        "",
        "A production price model would need stronger validation, fresh data, monitoring, bias checks, richer demand signals, and clear business rules. This baseline is useful for demonstrating a reproducible ML workflow and identifying promising features for future work.",
        "",
        "## Future Improvements",
        "",
        "- Add cross-validation.",
        "- Engineer better location and amenity features.",
        "- Compare performance by room type and neighbourhood.",
        "- Add explainability checks.",
        "- Revisit calendar price analysis only if a future Stockholm calendar dataset includes price values.",
    ]

    _ = listings, prepared
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """Format model results as Markdown."""
    lines = ["| Model | MAE | RMSE | R2 |", "|---|---:|---:|---:|"]
    for _, row in df.iterrows():
        lines.append(f"| {row['model']} | {row['MAE']:,.2f} | {row['RMSE']:,.2f} | {row['R2']:.4f} |")
    return "\n".join(lines)


def feature_importance_to_markdown(df: pd.DataFrame) -> str:
    """Format feature importances as Markdown."""
    lines = ["| Feature | Importance |", "|---|---:|"]
    for _, row in df.iterrows():
        lines.append(f"| {row['feature']} | {row['importance']:.4f} |")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
