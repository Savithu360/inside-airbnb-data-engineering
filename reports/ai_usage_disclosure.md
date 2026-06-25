# AI Usage Disclosure

## AI Tools Used

- ChatGPT
- Codex

## Sections Assisted by AI

- Project structure planning
- Day 1 pipeline scaffolding and code review
- Data quality report drafting
- Day 2 EDA script and report drafting
- Day 3 statistical testing and ML baseline implementation
- README and reproducibility documentation
- Final report organization

## How AI Was Used

AI was used as a coding and mentoring assistant to help structure the project, write Python scripts, generate Markdown reports, and explain analysis choices in beginner-friendly language. AI suggestions were applied only after checking them against the actual project files and generated outputs.

## How Outputs Were Validated

- Scripts were run locally against the actual Stockholm Inside Airbnb raw and processed data.
- Row counts were checked between processed CSV files and SQLite tables.
- Reports were reviewed to ensure calendar price fields were not used.
- Generated figures were checked for existence and file validity.
- Statistical and ML results were generated from the SQLite database rather than invented manually.

## Manual Changes Made

- The selected city configuration and documentation were reviewed and corrected for Stockholm consistency.
- The calendar price limitation was explicitly documented.
- Reports were polished for clarity and business interpretation.
- The final wording and scope were reviewed for assignment suitability.

## Rejected or Modified AI Suggestions

- Calendar-based pricing analysis was rejected because `calendar.price` and `calendar.adjusted_price` are 100% missing.
- Advanced tools such as Airflow, Spark, dbt, Great Expectations, dashboards, RAG, and complex ML were avoided to keep the assignment focused and realistic.
- Any suggestions that would imply causal conclusions from descriptive or statistical analysis were softened.

## Responsibility Statement

Final responsibility, review, validation, and submission decisions were done by me. AI assisted with implementation and explanation, but the outputs were checked against the actual data and project requirements.
