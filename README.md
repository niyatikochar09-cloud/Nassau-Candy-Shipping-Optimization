# Nassau Candy Factory Reallocation & Shipping Optimization

A data-driven decision-support system developed for Nassau Candy Distributor to analyze shipping performance, predict shipping lead time, evaluate alternative factory assignments, and identify potential factory reallocation opportunities.

## Project Overview

This project combines data analytics, exploratory data analysis, route-level analysis, K-Means clustering, machine learning, what-if scenario simulation, and an interactive Streamlit dashboard.

The primary objective is to determine whether alternative factory assignments could potentially improve shipping lead time while considering recommendation confidence, profit stability, and risk.

## Dataset

The project uses a transaction-level Nassau Candy Distributor dataset containing:

- 10,194 transaction records
- 8,549 unique orders
- 15 products
- 5 factories
- 4 destination regions
- 4 shipping modes

## Methodology

The project workflow includes:

1. Data Cleaning and Validation
2. Feature Engineering
3. Exploratory Data Analysis
4. Route-Level Performance Analysis
5. K-Means Clustering
6. Predictive Modeling
7. Factory What-If Scenario Simulation
8. Recommendation Generation
9. Streamlit Dashboard Development

## Predictive Modeling

Three regression models were evaluated:

| Model | MAE | RMSE | R² Score |
|---|---:|---:|---:|
| Linear Regression | 181.39 | 182.51 | 0.5290 |
| Random Forest Regressor | 148.77 | 177.17 | 0.5562 |
| Gradient Boosting Regressor | 159.87 | 169.59 | 0.5933 |

Gradient Boosting Regressor was selected as the final model because it achieved the highest R² score and lowest RMSE among the evaluated models.

## Key Results

- 50,970 transaction-level factory scenarios were evaluated.
- 33 positive factory reallocation opportunities were identified.
- Average predicted lead-time reduction across identified opportunities: 7.07 days.
- Median predicted lead-time reduction: 5.44 days.
- Overall model-based predicted improvement: approximately 5.18 days or 0.39%.

## Dashboard

The Streamlit dashboard includes:

- Executive Overview
- Factory Recommendations
- Scenario Simulator
- Route Performance
- Predictive Model

## Project Structure

```text
Nassau-Candy-Shipping-Optimization/
│
├── assets/
├── dashboard/
├── data/
├── models/
├── notebooks/
├── outputs/
├── reports/
├── .gitignore
├── requirements.txt
└── README.md

## Project Reports

The following reports document the project objectives, analytical methodology, predictive modeling results, factory reallocation recommendations, and optimization findings.

* **Executive Summary (PDF):** [View Executive Summary](reports/Executive_Summary_Nassau_Candy.pdf)
* **Executive Summary (Word):** [View Executive Summary (DOCX)](reports/Executive_Summary_Nassau_Candy.docx)
* **Research Report (PDF):** [View Complete Research Report](reports/Nassau_Candy_Factory_Optimization_Research_Report.pdf)
* **Research Report (Word):** [View Research Report (DOCX)](reports/Nassau_Candy_Factory_Optimization_Research_Report.docx)


