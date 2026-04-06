# Borrower Risk Assessment Guide
## Ghana Credit Risk Scorer — Quick Reference for Loan Officers

**Version:** 1.0  
**Author:** Evans Ataaya  
**Last Updated:** April 2026  
**Live App:** https://ghana-credit-risk-scorer-cydfwkxd5dbgxt5ln43smg.streamlit.app  
**GitHub:** https://github.com/Evans-Ataaya/ghana-credit-risk-scorer  

---

## How to Use the App

1. Open the live app link above on any browser
2. Enter the borrower's details in the left sidebar
3. Click the **"Assess Credit Risk"** button
4. Read the decision on the main screen

The app will return one of three decisions:

| Decision | Colour | Meaning |
|---|---|---|
| APPROVE | Green | Low default risk — proceed with loan |
| REVIEW | Amber | Medium risk — refer to senior credit officer |
| DECLINE | Red | High default risk — do not approve |

---

## Understanding the Risk Tiers

### APPROVE — Low Risk (Default Probability below 30%)

These borrowers present a strong repayment profile:

| Parameter | Favourable Range |
|---|---|
| Age | 45 to 60 years |
| Annual income (GHS) | 40,000 to 80,000 |
| Residence type | Owned |
| Loan amount (GHS) | 5,000 to 10,000 |
| Loan tenure | 6 to 12 months |
| Loan type | Secured |
| Loan purpose | Home or Education |
| Number of open accounts | 1 to 2 |
| Credit utilization ratio | 0.05 to 0.20 |
| Delinquency ratio | 0.00 to 0.05 |
| Average days past due | 0 to 5 days |

**What this means in practice:** A salaried worker aged 50,
earning GHS 50,000 per year, applying for a GHS 8,000
secured home improvement loan over 12 months, with
1 existing account and clean repayment history will
almost certainly receive an APPROVE decision.

---

### REVIEW — Medium Risk (Default Probability 30% to 50%)

These borrowers need closer examination by a senior
credit officer before a final decision is made:

| Parameter | Borderline Range |
|---|---|
| Age | 30 to 44 years |
| Annual income (GHS) | 12,000 to 25,000 |
| Residence type | Rented |
| Loan amount (GHS) | 12,000 to 20,000 |
| Loan tenure | 24 to 36 months |
| Loan type | Unsecured |
| Loan purpose | Personal or Auto |
| Number of open accounts | 3 to 4 |
| Credit utilization ratio | 0.40 to 0.60 |
| Delinquency ratio | 0.10 to 0.25 |
| Average days past due | 15 to 30 days |

**What this means in practice:** A trader aged 35,
earning GHS 18,000 per year, applying for a GHS 15,000
unsecured personal loan over 24 months, with 3 existing
accounts and occasional late payments will likely receive
a REVIEW decision. The senior officer should request
additional income verification or consider reducing
the loan amount or tenure.

---

### DECLINE — High Risk (Default Probability above 50%)

These borrowers present too high a default risk for
approval under current parameters:

| Parameter | High Risk Range |
|---|---|
| Age | 21 to 29 years |
| Annual income (GHS) | 3,000 to 8,000 |
| Residence type | Rented or Mortgage |
| Loan amount (GHS) | 25,000 to 50,000 |
| Loan tenure | 48 to 60 months |
| Loan type | Unsecured |
| Loan purpose | Personal |
| Number of open accounts | 5 to 7 |
| Credit utilization ratio | 0.70 to 1.00 |
| Delinquency ratio | 0.30 to 1.00 |
| Average days past due | 40 to 90 days |

**What this means in practice:** A young borrower aged 24,
earning GHS 5,000 per year, applying for a GHS 30,000
unsecured personal loan over 60 months, with 6 existing
accounts and frequent missed payments will almost
certainly receive a DECLINE decision.

---

## The Two Most Important Parameters

Based on the model's SHAP analysis, these two features
have the greatest influence on the final decision:

### 1. Number of Open Accounts (most important)
- 1 to 2 accounts → strongly favours APPROVE
- 3 to 4 accounts → pushes toward REVIEW
- 5 or more accounts → strongly pushes toward DECLINE

This reflects over-indebtedness — a borrower managing
too many loans simultaneously is a major red flag in
Ghana's microfinance sector.

### 2. Loan Tenure
- 6 to 12 months → strongly favours APPROVE
- 24 to 36 months → borderline
- 48 to 60 months → strongly pushes toward DECLINE

Longer loans expose borrowers to more income shocks
over time, especially in Ghana's informal economy.

---

## Important Notes for Loan Officers

1. **No single parameter decides the outcome.** The model
   weighs all 11 features together. A borrower with low
   income can still be APPROVED if all other parameters
   are strong.

2. **REVIEW does not mean DECLINE.** It means the case
   needs human judgement. A senior officer may approve
   after additional verification.

3. **The model is a decision-support tool, not a
   replacement for human judgement.** Always use your
   professional knowledge alongside the model output.

4. **The SHAP chart on the right side of the app**
   shows exactly which factors pushed the decision
   toward or away from default for that specific
   borrower. Red bars increase default risk. Blue
   bars reduce it.

5. **The model was trained on Ghana microfinance data**
   and is calibrated for the Ghanaian lending context.
   It should not be used for corporate credit or
   investment decisions.

---

## Glossary of Terms

| Term | Plain English Meaning |
|---|---|
| Default probability | Likelihood the borrower will not repay |
| Credit utilization ratio | How much of available credit is being used (0 = none, 1 = fully maxed out) |
| Delinquency ratio | Proportion of past payments that were late |
| Average days past due | How many days late payments typically were |
| Secured loan | Loan backed by collateral (e.g. property, vehicle) |
| Unsecured loan | Loan with no collateral backing |
| SHAP value | A score showing how much each factor influenced the decision |
| AUC-ROC | A measure of model accuracy (0.7037 = good performance) |

---

## Contact and Support

For technical issues with the app contact:  
**Evans Ataaya** — MTech Data Science and Industrial Analytics  
IBM Data Science Professional | IBM Generative AI Engineering Professional  

GitHub: https://github.com/Evans-Ataaya/ghana-credit-risk-scorer  
App: https://ghana-credit-risk-scorer-cydfwkxd5dbgxt5ln43smg.streamlit.app  

---

*Ghana Credit Risk Scorer v1.0 — April 2026*  
*This tool is for decision support only and does not constitute*  
*financial or legal advice.*