# Phase 2 Statistical Analysis Report

Selected city: Stockholm, Sweden

Data source: Inside Airbnb

## Scope

This report adds simple statistical tests to the Phase 1 and Phase 2 work. Tests use cleaned listing data from the SQLite database. Calendar price fields are not used because Stockholm calendar `price` and `adjusted_price` are 100% missing in the raw source data.

## Important Notes

- Listing prices have 35.62% missing values; price-based tests exclude missing prices.
- Review scores have 17.54% missing values; review-score tests exclude missing scores.
- Statistical significance does not prove causation.
- Business significance is different from statistical significance. A result can be statistically significant but still too small or too biased to act on directly.

## Test 1: Entire Home/Apt vs Private Room Listing Prices

| Metric | Value |
|---|---:|
| Group A | Entire home/apt |
| Group B | Private room |
| Group A count | 2,540 |
| Group B count | 621 |
| Group A median price | 1,386.00 |
| Group B median price | 597.00 |
| Mann-Whitney U statistic | 1,277,757.00 |
| p-value | < 0.001 |

Business interpretation: Entire homes and private rooms represent different accommodation products, so a price difference is expected. This supports using room type as a required segment for pricing analysis and any future model.

## Test 2: Superhost vs Non-Superhost Review Scores

| Metric | Value |
|---|---:|
| Group A | Superhost |
| Group B | Non-superhost |
| Group A count | 828 |
| Group B count | 3,232 |
| Group A median score | 4.90 |
| Group B median score | 4.91 |
| Group A mean score | 4.88 |
| Group B mean score | 4.79 |
| Mann-Whitney U statistic | 1,328,374.50 |
| p-value | 0.7414 |

Business interpretation: This test does not provide evidence of a statistically significant difference in review scores between superhosts and non-superhosts. Review scores are highly clustered near the top, so small differences may be difficult to detect. Superhost status may still matter for trust and conversion, but this dataset and test do not show a clear review-score difference.

## Test 3: Price Difference by Review Volume

| Metric | Value |
|---|---:|
| Group A | More than 10 reviews |
| Group B | 10 or fewer reviews |
| Group A count | 1,564 |
| Group B count | 1,626 |
| Group A median price | 1,142.00 |
| Group B median price | 1,273.00 |
| Mann-Whitney U statistic | 1,204,812.50 |
| p-value | 0.0103 |

Business interpretation: Review count can indicate listing maturity or historical demand, but it is not the same as bookings. Any price difference by review volume should be treated as an association, not proof that reviews cause higher or lower prices.

## Test 4: Neighbourhood Price Differences

| Metric | Value |
|---|---:|
| Minimum priced listings per neighbourhood | 30 |
| Eligible neighbourhood count | 14 |
| Kruskal-Wallis statistic | 351.32 |
| p-value | < 0.001 |

Top neighbourhood median prices among eligible neighbourhoods:

| Neighbourhood | Priced listings | Median price |
|---|---:|---:|
| Norrmalms | 311 | 1,439.00 |
| Södermalms | 806 | 1,438.50 |
| Farsta | 111 | 1,429.00 |
| Östermalms | 213 | 1,360.00 |
| Bromma | 218 | 1,350.00 |
| Kungsholmens | 298 | 1,167.00 |
| Hägersten-Liljeholmens | 283 | 1,080.00 |
| Älvsjö | 127 | 990.00 |
| Hässelby-Vällingby | 111 | 969.00 |
| Skarpnäcks | 163 | 876.00 |

Business interpretation: Neighbourhood is associated with price differences and can be used for local pricing benchmarks. However, neighbourhood comparisons should still control for room type, property type, and listing capacity before making pricing recommendations.

## Overall Interpretation

- Room type, review-related signals, host status, and neighbourhood all provide useful segmentation lenses.
- The tests are useful for prioritizing business questions, not for proving causal effects.
- Future modeling should include room type and neighbourhood, and should treat missing listing prices explicitly.