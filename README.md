# Ghana Credit Risk Scorer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ghana-credit-risk-scorer-cydfwkxd5dbgxt5ln43smg.streamlit.app)

![Python](https://img.shields.io/badge/Python-3.10-blue)
![XGBoost](https://img.shields.io/badge/XGBoost-1.7.6-green)
![SHAP](https://img.shields.io/badge/SHAP-0.43.0-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Overview

A machine learning-powered credit risk assessment tool built
specifically for Ghana's microfinance and retail lending sector.
This project predicts the probability of loan default using
XGBoost with full SHAP explainability, deployed as an interactive
Streamlit web application.

## Live Demo

Run locally with:
```bash
streamlit run app.py
```

## Project Structure
```
ghana-credit-risk-scorer/
├── README.md
├── requirements.txt
├── ghana_credit_risk_scorer.ipynb
├── app.py
├── data/
│   ├── raw/
│   │   └── loan_data.csv
│   └── processed/
├── models/
│   ├── logistic_regression.pkl
│   ├── random_forest.pkl
│   ├── xgboost.pkl
│   ├── xgboost_tuned.pkl
│   └── scaler.pkl
└── outputs/
    └── figures/
```

## Model Performance

| Model | AUC-ROC | Precision | Recall | F1-Score |
|---|---|---|---|---|
| Logistic Regression | 0.6977 | 0.2149 | **0.6578** | **0.3240** |
| Random Forest | 0.6786 | 0.2104 | 0.3688 | 0.2680 |
| XGBoost (original) | 0.6891 | 0.4808 | 0.0951 | 0.1587 |
| XGBoost (tuned) | **0.7037** | 0.3478 | 0.2738 | 0.3064 |

## Top Default Risk Factors (SHAP)

| Rank | Feature | Mean SHAP |
|---|---|---|
| 1 | num_open_accounts | 0.465 |
| 2 | loan_tenure_months | 0.403 |
| 3 | loan_type | 0.358 |
| 4 | income | 0.355 |
| 5 | age | 0.276 |


## Quick Reference Guide

For non-technical users and loan officers, see the
[Borrower Risk Assessment Guide](BORROWER_RISK_GUIDE.md)
for plain-English explanation of risk tiers, borrower
profiles, and how to interpret app decisions.

## Key Findings

- Number of concurrent open accounts is the strongest
  default predictor — reflecting over-indebtedness in
  Ghana's fragmented microfinance sector
- Loan tenure and loan type are the second and third
  most important features
- Traditional delinquency metrics rank surprisingly low
- Credit utilisation ratio — dominant in Western scoring
  systems — is the weakest predictor in the Ghana context

## Tech Stack

- Python 3.10
- XGBoost 1.7.6
- SHAP 0.43.0
- Scikit-learn 1.3.2
- Imbalanced-learn 0.11.0
- Streamlit 1.32.0
- Pandas 2.1.4
- Matplotlib 3.8.2
- Seaborn 0.13.2

## Installation
```bash
git clone https://github.com/your-username/ghana-credit-risk-scorer
cd ghana-credit-risk-scorer
conda create -n ghana-portfolio python=3.10 -y
conda activate ghana-portfolio
pip install -r requirements.txt
streamlit run app.py
```

## Author

**Evans Ataaya**
- MTech, Data Science and Industrial Analytics
- IBM Data Science Professional Certificate (Coursera, Dec 2025)
- IBM Generative AI Engineering Professional Certificate
  (Coursera, Apr 2026)

## Sector

Financial | Ghana | Sub-Saharan Africa

## License

MIT License — open source and freely reproducible