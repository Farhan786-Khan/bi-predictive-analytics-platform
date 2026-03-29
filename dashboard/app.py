"""
dashboard/app.py
-----------------
5-page Streamlit BI dashboard for the Customer Churn Prediction platform.
Run: streamlit run dashboard/app.py
"""
import sys
sys.path.append("..")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="BI Predictive Analytics Platform",
    page_icon="chart_with_upwards_trend", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .stApp { background-color: #0a0e1a; }
    .metric-card { background: rgba(26,86,219,0.08); border: 1px solid rgba(26,86,219,0.25);
        border-radius: 12px; padding: 20px; text-align: center; }
    .metric-value { font-size: 2.2rem; font-weight: 800; color: #1A56DB; }
    .metric-label { font-size: 0.85rem; color: #94A3B8; margin-top: 4px; }
    .section-header { font-size: 1.2rem; font-weight: 700; color: #E2E8F0;
        border-left: 4px solid #1A56DB; padding-left: 12px; margin: 24px 0 16px 0; }
    div[data-testid="stMetric"] { background: rgba(255,255,255,0.03); border-radius: 10px; padding: 12px; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    try:
        return pd.read_csv("data/sample_churn_data.csv")
    except FileNotFoundError:
        import sys; sys.path.insert(0, ".")
        from src.data_pipeline.data_loader import DataLoader
        loader = DataLoader()
        df = loader.generate_sample_churn_data(n=5000)
        df.to_csv("data/sample_churn_data.csv", index=False)
        return df


@st.cache_resource
def train_models(df):
    from src.data_pipeline.preprocessor import Preprocessor
    from src.models.classification_models import ModelSuite
    pp = Preprocessor(target_col="churn", test_size=0.2)
    X_train, X_test, y_train, y_test = pp.fit_transform(df)
    suite = ModelSuite(cv_folds=3)
    suite.train_all(X_train, y_train)
    return suite, pp, X_train, X_test, y_train, y_test


with st.sidebar:
    st.markdown("## BI Analytics Platform")
    st.markdown("*Customer Churn Intelligence*")
    st.divider()
    page = st.radio("Navigation",
        ["Overview", "EDA", "Models", "Predict", "Business Impact"],
        label_visibility="collapsed")
    st.divider()
    st.markdown("**Built by:** Mohammed Farhan Khan")
    st.markdown("**Stack:** Python · Scikit-learn · XGBoost · Streamlit · Plotly")
    st.markdown("[GitHub](https://github.com/Farhan786-Khan) · [LinkedIn](https://www.linkedin.com/in/mohammed-farhan-55976920b)")

with st.spinner("Loading data..."):
    df = load_data()

if page == "Overview":
    st.markdown("# BI Predictive Analytics Platform")
    st.markdown("**Customer Churn Prediction · Multi-Model ML · Interactive BI Dashboard**")
    st.divider()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Customers", f"{len(df):,}")
    c2.metric("Churn Rate", f"{df['churn'].mean():.1%}")
    c3.metric("Avg Tenure", f"{df['tenure_months'].mean():.1f} months")
    c4.metric("Avg Monthly Charge", f"INR {df['monthly_charges'].mean():.0f}")
    st.markdown('<div class="section-header">Dataset Preview</div>', unsafe_allow_html=True)
    st.dataframe(df.head(10), use_container_width=True, height=250)
    st.markdown('<div class="section-header">Feature Summary</div>', unsafe_allow_html=True)
    st.dataframe(df.describe().T.style.background_gradient(cmap="Blues"), use_container_width=True)

elif page == "EDA":
    st.markdown("# Exploratory Data Analysis")
    st.divider()
    from src.visualization.plotly_charts import BIVisualizer
    viz = BIVisualizer()
    tab1,tab2,tab3,tab4,tab5 = st.tabs(["Churn Overview","Tenure","Charges","Contracts","Satisfaction"])
    with tab1: st.plotly_chart(viz.churn_overview(df), use_container_width=True)
    with tab2: st.plotly_chart(viz.tenure_churn_analysis(df), use_container_width=True)
    with tab3: st.plotly_chart(viz.charges_analysis(df), use_container_width=True)
    with tab4: st.plotly_chart(viz.contract_churn_heatmap(df), use_container_width=True)
    with tab5: st.plotly_chart(viz.satisfaction_impact(df), use_container_width=True)

elif page == "Models":
    st.markdown("# Model Training & Evaluation")
    st.divider()
    with st.spinner("Training models... (first run ~30s)"):
        suite, pp, X_train, X_test, y_train, y_test = train_models(df)
    from src.models.evaluator import Evaluator
    from src.visualization.plotly_charts import BIVisualizer
    evaluator = Evaluator(output_dir="reports/figures")
    viz = BIVisualizer()
    summary = evaluator.evaluate(suite.trained_models, X_test, y_test, feature_names=pp.feature_names_)
    st.markdown('<div class="section-header">Model Leaderboard</div>', unsafe_allow_html=True)
    best_idx = summary["f1_score"].idxmax()
    st.dataframe(summary.style.highlight_max(subset=["f1_score","roc_auc","accuracy"], color="#1A56DB33"),
                 use_container_width=True, height=200)
    best_name = summary.loc[best_idx,"model"]
    st.success(f"Best model: **{best_name}** | F1={summary.loc[best_idx,'f1_score']:.4f}")
    st.plotly_chart(viz.model_comparison_bar(summary), use_container_width=True)
    st.markdown('<div class="section-header">CV Results</div>', unsafe_allow_html=True)
    for name, results in suite.cv_results.items():
        with st.expander(f"{name}"):
            cols = st.columns(3)
            for i,(metric,vals) in enumerate(results.items()):
                cols[i].metric(metric.replace("_"," ").title(), f"{vals['mean']:.4f}", f"+/-{vals['std']:.4f}")

elif page == "Predict":
    st.markdown("# Single Customer Churn Predictor")
    st.divider()
    with st.spinner("Preparing models..."):
        suite, pp, X_train, X_test, y_train, y_test = train_models(df)
    best_name = suite.best_model("f1")
    model = suite.trained_models[best_name]
    with st.form("predict_form"):
        c1,c2,c3 = st.columns(3)
        with c1:
            tenure = st.slider("Tenure (months)", 1, 72, 24)
            monthly = st.slider("Monthly Charges (INR)", 20, 120, 65)
            total = st.number_input("Total Charges (INR)", value=float(tenure*monthly), step=100.0)
        with c2:
            products = st.slider("Number of Products", 1, 4, 2)
            calls = st.slider("Support Calls", 0, 10, 2)
            satisfaction = st.slider("Satisfaction Score (1-5)", 1, 5, 3)
        with c3:
            contract = st.selectbox("Contract Type", ["Month-to-Month","One Year","Two Year"])
            payment = st.selectbox("Payment Method", ["Electronic Check","Mailed Check","Bank Transfer","Credit Card"])
            internet = st.selectbox("Internet Service", ["DSL","Fiber Optic","No Internet"])
        submitted = st.form_submit_button("Predict Churn Risk", type="primary", use_container_width=True)
    if submitted:
        customer = pd.DataFrame([{"customer_id":"DEMO001","tenure_months":tenure,
            "monthly_charges":monthly,"total_charges":total,"num_products":products,
            "support_calls":calls,"satisfaction_score":satisfaction,"contract_type":contract,
            "payment_method":payment,"internet_service":internet,"churn":0}])
        prob = model.predict_proba(pp.transform(customer))[0][1]
        risk = "HIGH RISK" if prob > 0.6 else "MEDIUM RISK" if prob > 0.35 else "LOW RISK"
        bar_color = "#EF4444" if prob > 0.6 else "#F59E0B" if prob > 0.35 else "#22C55E"
        col1,col2 = st.columns([1,2])
        with col1:
            st.markdown(f"### {risk}")
            st.metric("Churn Probability", f"{prob:.1%}")
            st.metric("Model Used", best_name.replace("_"," ").title())
        with col2:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=prob*100,
                number={"suffix":"%","font":{"size":36,"color":bar_color}},
                gauge={"axis":{"range":[0,100]},"bar":{"color":bar_color},
                       "steps":[{"range":[0,35],"color":"#0d1117"},{"range":[35,100],"color":"#1E293B"}],
                       "threshold":{"line":{"color":"white","width":3},"value":60}},
                title={"text":"Churn Risk Score"}))
            fig.update_layout(template="plotly_dark", height=260, paper_bgcolor="#0a0e1a")
            st.plotly_chart(fig, use_container_width=True)

elif page == "Business Impact":
    st.markdown("# Business Impact Analysis")
    st.divider()
    with st.spinner("Calculating impact..."):
        suite, pp, X_train, X_test, y_train, y_test = train_models(df)
    from src.models.evaluator import Evaluator
    evaluator = Evaluator()
    avg_val = st.slider("Avg Annual Customer Value (INR)", 500, 5000, 1200, 100)
    ret_cost = st.slider("Retention Campaign Cost per Customer (INR)", 50, 500, 150, 25)
    best_name = suite.best_model("f1")
    impact = evaluator.business_impact(suite.trained_models[best_name], X_test, y_test, avg_val, ret_cost)
    st.markdown(f"*Using **{best_name.replace('_',' ').title()}** (best model)*")
    st.divider()
    c1,c2,c3 = st.columns(3)
    c1.metric("Churners Caught", impact["churners_caught"])
    c2.metric("Churners Missed", impact["churners_missed"])
    c3.metric("False Alarms", impact["false_alarms"])
    c4,c5,c6 = st.columns(3)
    c4.metric("Revenue Saved", impact["estimated_revenue_saved"])
    c5.metric("Retention Cost", impact["retention_program_cost"])
    c6.metric("Net Business Value", impact["net_business_value"])
    st.warning(f"Revenue Still at Risk: {impact['revenue_still_at_risk']}")
    st.info("Tip: Lower the decision threshold to catch more churners at the cost of more false alarms.")
