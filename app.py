# ============================================================
# GHANA CREDIT RISK SCORER — STREAMLIT APPLICATION
# Author: Evans Ataaya
# Version: 1.0
# Date: April 2026
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Ghana Credit Risk Scorer",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1B4F72;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1rem;
        color: #5D6D7E;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #EBF5FB;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border-left: 5px solid #1B4F72;
    }
    .risk-high {
        background-color: #FDEDEC;
        border-left: 5px solid #E74C3C;
        padding: 1rem;
        border-radius: 8px;
        font-size: 1.2rem;
        font-weight: bold;
        color: #C0392B;
    }
    .risk-low {
        background-color: #EAFAF1;
        border-left: 5px solid #27AE60;
        padding: 1rem;
        border-radius: 8px;
        font-size: 1.2rem;
        font-weight: bold;
        color: #1E8449;
    }
    .risk-medium {
        background-color: #FEF9E7;
        border-left: 5px solid #F39C12;
        padding: 1rem;
        border-radius: 8px;
        font-size: 1.2rem;
        font-weight: bold;
        color: #D68910;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1B4F72;
        border-bottom: 2px solid #AED6F1;
        padding-bottom: 0.3rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-header">🏦 Ghana Credit Risk Scorer</div>',
    unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">'
    'ML-powered loan default prediction for Ghana\'s microfinance sector | '
    'Powered by XGBoost + SHAP Explainability'
    '</div>',
    unsafe_allow_html=True)

st.divider()

# ============================================================
# LOAD MODELS — FIXED PATHS (no ../models/)
# ============================================================

@st.cache_resource
def load_models():
    models = {}
    model_files = {
        'XGBoost (tuned)'    : 'models/xgboost_tuned.pkl',
        'Logistic Regression': 'models/logistic_regression.pkl',
        'Random Forest'      : 'models/random_forest.pkl',
    }
    for name, path in model_files.items():
        try:
            models[name] = joblib.load(path)
        except Exception as e:
            st.warning(f"Could not load {name}: {e}")
    return models

@st.cache_resource
def load_scaler():
    try:
        return joblib.load('models/scaler.pkl')
    except Exception as e:
        st.warning(f"Scaler not found: {e}")
        return None

models = load_models()
scaler = load_scaler()

# ============================================================
# SIDEBAR — BORROWER INPUT FORM
# ============================================================

st.sidebar.markdown("## Borrower Information")
st.sidebar.markdown(
    "Enter the borrower's details below to assess credit risk.")
st.sidebar.divider()

st.sidebar.markdown("**Borrower Demographics**")
age    = st.sidebar.slider("Age (years)", 21, 65, 35)
income = st.sidebar.number_input(
    "Annual Income (GHS)", 3000, 80000, 18000, step=500)

st.sidebar.divider()
st.sidebar.markdown("**Loan Details**")

loan_amount = st.sidebar.number_input(
    "Loan Amount (GHS)", 1000, 50000, 12000, step=500)
loan_tenure_months = st.sidebar.selectbox(
    "Loan Tenure (months)",
    [6, 12, 18, 24, 36, 48, 60], index=2)
loan_purpose = st.sidebar.selectbox(
    "Loan Purpose",
    ['Personal', 'Home', 'Education', 'Auto'])
loan_type = st.sidebar.selectbox(
    "Loan Type", ['Unsecured', 'Secured'])
residence_type = st.sidebar.selectbox(
    "Residence Type", ['Rented', 'Owned', 'Mortgage'])

st.sidebar.divider()
st.sidebar.markdown("**Credit Behaviour**")

num_open_accounts = st.sidebar.slider(
    "Number of Open Accounts", 1, 7, 2)
credit_utilization_ratio = st.sidebar.slider(
    "Credit Utilization Ratio", 0.0, 1.0, 0.3, 0.01)
delinquency_ratio = st.sidebar.slider(
    "Delinquency Ratio", 0.0, 1.0, 0.05, 0.01)
avg_dpd_per_delinquency = st.sidebar.slider(
    "Avg Days Past Due", 0, 90, 5)

st.sidebar.divider()
selected_model = st.sidebar.selectbox(
    "Select Scoring Model",
    list(models.keys()))

predict_button = st.sidebar.button(
    "Assess Credit Risk",
    type="primary",
    use_container_width=True)

# ============================================================
# ENCODE INPUT
# ============================================================

def encode_input():
    residence_map = {'Owned': 0, 'Rented': 1, 'Mortgage': 2}
    purpose_map   = {'Auto': 0, 'Education': 1,
                     'Home': 2, 'Personal': 3}
    type_map      = {'Secured': 0, 'Unsecured': 1}

    return pd.DataFrame([{
        'age'                      : age,
        'income'                   : income,
        'loan_amount'              : loan_amount,
        'loan_tenure_months'       : loan_tenure_months,
        'avg_dpd_per_delinquency'  : avg_dpd_per_delinquency,
        'delinquency_ratio'        : delinquency_ratio,
        'credit_utilization_ratio' : credit_utilization_ratio,
        'num_open_accounts'        : num_open_accounts,
        'residence_type'           : residence_map[residence_type],
        'loan_purpose'             : purpose_map[loan_purpose],
        'loan_type'                : type_map[loan_type]
    }])

# ============================================================
# MAIN DASHBOARD — DEFAULT STATE
# ============================================================

if not predict_button:

    st.markdown(
        '<div class="section-header">Model Performance Summary</div>',
        unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("XGBoost AUC-ROC", "0.7037",
                  delta="Best discriminator")
    with col2:
        st.metric("Logistic Regression Recall", "0.6578",
                  delta="Best default catcher")
    with col3:
        st.metric("Training Records", "10,000",
                  delta="Synthetic Ghana data")
    with col4:
        st.metric("Features Used", "11",
                  delta="SHAP explained")

    st.divider()

    st.markdown(
        '<div class="section-header">'
        'Top Default Risk Factors (SHAP Analysis)'
        '</div>',
        unsafe_allow_html=True)

    shap_data = pd.DataFrame({
        'Feature': [
            'num_open_accounts',
            'loan_tenure_months',
            'loan_type',
            'income',
            'age',
            'loan_purpose',
            'loan_amount',
            'delinquency_ratio',
            'avg_dpd_per_delinquency',
            'residence_type',
            'credit_utilization_ratio'
        ],
        'Mean |SHAP|': [
            0.465, 0.403, 0.358, 0.355,
            0.276, 0.251, 0.208, 0.175,
            0.129, 0.086, 0.065
        ]
    }).sort_values('Mean |SHAP|')

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(
        shap_data['Feature'],
        shap_data['Mean |SHAP|'],
        color='steelblue',
        edgecolor='white')
    ax.set_xlabel('Mean |SHAP Value|', fontsize=12)
    ax.set_title(
        'Global Feature Importance — XGBoost Tuned Model',
        fontsize=13, fontweight='bold')
    for bar, val in zip(bars, shap_data['Mean |SHAP|']):
        ax.text(
            val + 0.005,
            bar.get_y() + bar.get_height() / 2,
            f'{val:.3f}',
            va='center', fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.divider()
    st.info(
        "Enter borrower details in the left panel and click "
        "'Assess Credit Risk' to generate a prediction with "
        "full SHAP explanation.")

    st.divider()
    st.markdown(
        '<div class="section-header">About This Tool</div>',
        unsafe_allow_html=True)

    st.markdown("""
    This tool was developed as part of a professional data science
    portfolio project focused on Ghana's microfinance sector.

    | Item | Detail |
    |---|---|
    | Author | Evans Ataaya |
    | Degree | MTech, Data Science and Industrial Analytics |
    | Certifications | IBM Data Science Professional · IBM Gen AI Engineering Professional |
    | Models | Logistic Regression · Random Forest · XGBoost (tuned) |
    | Explainability | SHAP (SHapley Additive exPlanations) |
    | Dataset | 10,000 synthetic Ghana microfinance loan records |
    | Version | v1.0 — April 2026 |
    """)

# ============================================================
# PREDICTION STATE
# ============================================================

else:
    input_df = encode_input()
    model    = models[selected_model]

    # Scale input using saved scaler
    if scaler is not None:
        input_scaled = scaler.transform(input_df)
    else:
        input_scaled = input_df.values

    input_scaled_df = pd.DataFrame(
        input_scaled,
        columns=input_df.columns)

    # Predict probability
    prob      = model.predict_proba(input_scaled)[0][1]
    threshold = 0.35 if 'XGBoost' in selected_model else 0.5
    pred      = int(prob >= threshold)

    # Risk tier classification
    if prob < 0.3:
        risk_tier  = "Low Risk"
        risk_class = "risk-low"
        decision   = "APPROVE"
    elif prob < 0.5:
        risk_tier  = "Medium Risk"
        risk_class = "risk-medium"
        decision   = "REVIEW"
    else:
        risk_tier  = "High Risk"
        risk_class = "risk-high"
        decision   = "DECLINE"

    # ---- Two column layout ----
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(
            '<div class="section-header">'
            'Credit Risk Assessment</div>',
            unsafe_allow_html=True)

        st.markdown(
            f'<div class="{risk_class}">'
            f'Decision: {decision} &nbsp;|&nbsp; {risk_tier}'
            f'</div>',
            unsafe_allow_html=True)

        st.markdown("")
        st.metric(
            label="Default Probability",
            value=f"{prob * 100:.1f}%",
            delta=(f"Threshold: "
                   f"{'35%' if 'XGBoost' in selected_model else '50%'}"))

        st.markdown("")
        st.markdown(
            '<div class="section-header">'
            'Borrower Profile Summary</div>',
            unsafe_allow_html=True)

        summary = pd.DataFrame({
            'Feature': [
                'Age',
                'Annual Income (GHS)',
                'Loan Amount (GHS)',
                'Tenure (months)',
                'Loan Purpose',
                'Loan Type',
                'Residence Type',
                'Open Accounts',
                'Credit Utilization',
                'Delinquency Ratio',
                'Avg Days Past Due'
            ],
            'Value': [
                age,
                f"{income:,}",
                f"{loan_amount:,}",
                loan_tenure_months,
                loan_purpose,
                loan_type,
                residence_type,
                num_open_accounts,
                f"{credit_utilization_ratio:.2f}",
                f"{delinquency_ratio:.2f}",
                avg_dpd_per_delinquency
            ]
        })
        st.dataframe(
            summary.set_index('Feature'),
            use_container_width=True)

    with col2:
        st.markdown(
            '<div class="section-header">'
            'SHAP Feature Contribution</div>',
            unsafe_allow_html=True)

        try:
            explainer = shap.TreeExplainer(model)
            shap_vals = explainer.shap_values(input_scaled_df)

            explanation = shap.Explanation(
                values        = shap_vals[0],
                base_values   = explainer.expected_value,
                data          = input_df.values[0],
                feature_names = input_df.columns.tolist())

            fig2, ax2 = plt.subplots(figsize=(10, 6))
            shap.plots.waterfall(explanation, show=False)
            plt.tight_layout()
            st.pyplot(fig2)
            plt.close()

        except Exception as e:
            st.warning(
                f"SHAP waterfall unavailable for "
                f"{selected_model}: {e}")

            # Fallback — global importance chart
            shap_fallback = pd.DataFrame({
                'Feature': input_df.columns.tolist(),
                'Importance': [
                    0.276, 0.355, 0.208, 0.403,
                    0.129, 0.175, 0.065, 0.465,
                    0.251, 0.086, 0.358
                ]
            }).sort_values('Importance')

            fig3, ax3 = plt.subplots(figsize=(10, 6))
            ax3.barh(
                shap_fallback['Feature'],
                shap_fallback['Importance'],
                color='steelblue')
            ax3.set_title(
                'Global Feature Importance (SHAP)',
                fontweight='bold')
            ax3.set_xlabel('Mean |SHAP Value|')
            plt.tight_layout()
            st.pyplot(fig3)
            plt.close()

    st.divider()

    # Risk interpretation narrative
    st.markdown(
        '<div class="section-header">'
        'Risk Interpretation and Recommendation</div>',
        unsafe_allow_html=True)

    if decision == "APPROVE":
        st.success(
            f"This borrower presents a LOW default risk "
            f"({prob * 100:.1f}%). The model recommends loan "
            f"approval subject to standard monitoring. "
            f"Ensure income verification is on file.")

    elif decision == "REVIEW":
        st.warning(
            f"This borrower presents a MODERATE default risk "
            f"({prob * 100:.1f}%). Refer to a senior credit "
            f"officer for manual review. Consider requesting "
            f"additional income documentation, reducing the "
            f"loan amount, or shortening the repayment tenure.")

    else:
        st.error(
            f"This borrower presents a HIGH default risk "
            f"({prob * 100:.1f}%). The model recommends "
            f"declining this application. Key risk drivers "
            f"are visible in the SHAP contribution chart above. "
            f"The borrower may reapply with a reduced loan "
            f"amount, shorter tenure, or additional collateral.")

    st.divider()

    # Model info footer
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.caption(f"Model used: {selected_model}")
    with col_b:
        st.caption(
            f"Decision threshold: "
            f"{'35%' if 'XGBoost' in selected_model else '50%'}")
    with col_c:
        st.caption("Ghana Credit Risk Scorer v1.0 | April 2026")

    st.divider()
    st.caption(
        "Evans Ataaya | MTech Data Science and Industrial Analytics | "
        "IBM Data Science Professional | "
        "IBM Generative AI Engineering Professional | "
        "April 2026")