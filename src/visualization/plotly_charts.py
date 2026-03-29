"""
visualization/plotly_charts.py
--------------------------------
Interactive Plotly charts for churn EDA and model comparison.
Consistent dark theme throughout. All charts are interactive (hover/zoom/download).
"""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging

logger = logging.getLogger(__name__)
DARK = "plotly_dark"
COLORS = ["#1A56DB", "#7C3AED", "#06B6D4", "#22C55E", "#F59E0B", "#EF4444"]


class BIVisualizer:
    """Business Intelligence visualizations for churn analysis.
    All Plotly charts are fully interactive (hover, zoom, download).
    """

    def churn_overview(self, df: pd.DataFrame) -> go.Figure:
        """Donut + bar chart showing overall churn rate."""
        counts = df["churn"].value_counts().rename({0: "Retained", 1: "Churned"})
        fig = make_subplots(rows=1, cols=2,
            specs=[[{"type": "pie"}, {"type": "bar"}]],
            subplot_titles=["Churn Distribution", "Customer Count by Segment"])
        fig.add_trace(go.Pie(labels=counts.index, values=counts.values,
            marker_colors=["#1A56DB","#EF4444"], hole=0.45, textinfo="label+percent"), row=1, col=1)
        fig.add_trace(go.Bar(x=counts.index, y=counts.values,
            marker_color=["#1A56DB","#EF4444"], text=counts.values, textposition="outside"), row=1, col=2)
        fig.update_layout(template=DARK, showlegend=False, title="Customer Churn Overview",
                          title_font=dict(size=18, color="#E2E8F0"))
        return fig

    def tenure_churn_analysis(self, df: pd.DataFrame) -> go.Figure:
        """Violin + box plot of tenure by churn status."""
        return px.violin(df, x=df["churn"].map({0:"Retained",1:"Churned"}),
            y="tenure_months", color=df["churn"].map({0:"Retained",1:"Churned"}),
            box=True, points="outliers",
            color_discrete_map={"Retained":"#1A56DB","Churned":"#EF4444"},
            title="Tenure Distribution by Churn Status",
            labels={"x":"Segment","tenure_months":"Tenure (Months)"}, template=DARK)

    def charges_analysis(self, df: pd.DataFrame) -> go.Figure:
        """Scatter of monthly vs total charges coloured by churn."""
        sample = df.sample(min(1000, len(df)), random_state=42)
        return px.scatter(sample, x="monthly_charges", y="total_charges",
            color=sample["churn"].map({0:"Retained",1:"Churned"}),
            color_discrete_map={"Retained":"#1A56DB","Churned":"#EF4444"},
            opacity=0.65, title="Monthly vs Total Charges by Churn",
            labels={"monthly_charges":"Monthly Charges (INR)","total_charges":"Total Charges (INR)"},
            template=DARK)

    def contract_churn_heatmap(self, df: pd.DataFrame) -> go.Figure:
        """Churn rate heatmap by contract type and internet service."""
        pivot = df.groupby(["contract_type","internet_service"])["churn"].mean().unstack().fillna(0)
        return px.imshow(pivot, text_auto=".1%", aspect="auto",
            color_continuous_scale=["#0d1117","#1A56DB","#EF4444"],
            title="Churn Rate Heatmap: Contract x Internet Service", template=DARK)

    def satisfaction_impact(self, df: pd.DataFrame) -> go.Figure:
        """Churn rate by satisfaction score - grouped bar."""
        grp = df.groupby("satisfaction_score")["churn"].agg(["mean","count"]).reset_index()
        grp.columns = ["satisfaction_score","churn_rate","count"]
        fig = px.bar(grp, x="satisfaction_score", y="churn_rate",
            text=grp["churn_rate"].map("{:.1%}".format),
            color="churn_rate", color_continuous_scale=["#1A56DB","#EF4444"],
            title="Churn Rate by Customer Satisfaction Score",
            labels={"satisfaction_score":"Satisfaction (1=Low, 5=High)","churn_rate":"Churn Rate"},
            template=DARK)
        fig.update_traces(textposition="outside")
        return fig

    def correlation_matrix(self, df: pd.DataFrame) -> go.Figure:
        """Interactive correlation heatmap of numeric features."""
        num_df = df.select_dtypes(include=np.number).drop(columns=["churn"], errors="ignore")
        return px.imshow(num_df.corr(), text_auto=".2f", aspect="auto",
            color_continuous_scale="RdBu_r", title="Feature Correlation Matrix", template=DARK)

    def model_comparison_bar(self, summary_df: pd.DataFrame) -> go.Figure:
        """Side-by-side bar chart comparing model metrics."""
        fig = go.Figure()
        for metric, color in zip(["accuracy","f1_score","roc_auc"], ["#1A56DB","#7C3AED","#06B6D4"]):
            if metric in summary_df.columns:
                fig.add_trace(go.Bar(name=metric.replace("_"," ").title(),
                    x=summary_df["model"], y=summary_df[metric],
                    marker_color=color,
                    text=summary_df[metric].map("{:.3f}".format), textposition="outside"))
        fig.update_layout(barmode="group", template=DARK, title="Model Performance Comparison",
            yaxis=dict(range=[0, 1.05]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02))
        return fig
