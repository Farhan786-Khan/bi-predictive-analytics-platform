"""
models/evaluator.py
--------------------
Model evaluation: classification metrics, ROC curves, confusion matrices,
feature importance plots, and business impact analysis in INR.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix, roc_auc_score, roc_curve,
    f1_score, average_precision_score,
)
from typing import Dict, Any, Optional, List
import logging, os

logger = logging.getLogger(__name__)
PALETTE = {"primary": "#1A56DB", "secondary": "#7C3AED", "accent": "#06B6D4",
           "success": "#22C55E", "danger": "#EF4444", "muted": "#94A3B8"}


class Evaluator:
    """Comprehensive model evaluation with metrics and visual outputs."""

    def __init__(self, output_dir: str = "reports/figures"):
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir

    def evaluate(self, models: Dict[str, Any], X_test: np.ndarray,
                 y_test: np.ndarray, feature_names: Optional[List[str]] = None) -> pd.DataFrame:
        """Evaluate all models and return a ranked summary DataFrame."""
        results = []
        for name, model in models.items():
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None
            row = {
                "model": name,
                "accuracy": round((y_pred == y_test).mean(), 4),
                "f1_score": round(f1_score(y_test, y_pred), 4),
                "roc_auc": round(roc_auc_score(y_test, y_prob), 4) if y_prob is not None else None,
                "avg_precision": round(average_precision_score(y_test, y_prob), 4) if y_prob is not None else None,
            }
            results.append(row)
            logger.info(f"{name}: F1={row['f1_score']}, ROC-AUC={row['roc_auc']}")
        return pd.DataFrame(results).sort_values("f1_score", ascending=False).reset_index(drop=True)

    def plot_roc_curves(self, models: Dict, X_test: np.ndarray, y_test: np.ndarray, save: bool = True):
        """Plot ROC curves for all models on one chart."""
        fig, ax = plt.subplots(figsize=(9, 6))
        fig.patch.set_facecolor("#0d1117"); ax.set_facecolor("#0d1117")
        colors = [PALETTE["primary"], PALETTE["secondary"], PALETTE["accent"], PALETTE["success"], PALETTE["danger"]]
        for (name, model), color in zip(models.items(), colors):
            if hasattr(model, "predict_proba"):
                y_prob = model.predict_proba(X_test)[:, 1]
                fpr, tpr, _ = roc_curve(y_test, y_prob)
                auc = roc_auc_score(y_test, y_prob)
                ax.plot(fpr, tpr, label=f"{name} (AUC={auc:.3f})", color=color, lw=2.5)
        ax.plot([0,1],[0,1],"--",color="#475569",lw=1.5,label="Random (0.500)")
        ax.set_xlabel("False Positive Rate", color="#94A3B8"); ax.set_ylabel("True Positive Rate", color="#94A3B8")
        ax.set_title("ROC Curves - Model Comparison", color="#E2E8F0", fontsize=14, fontweight="bold")
        ax.legend(facecolor="#1E293B", edgecolor="#334155", labelcolor="#E2E8F0")
        ax.tick_params(colors="#94A3B8"); ax.spines[:].set_color("#334155")
        plt.tight_layout()
        if save:
            path = f"{self.output_dir}/roc_curves.png"
            plt.savefig(path, dpi=150, bbox_inches="tight", facecolor="#0d1117")
            logger.info(f"Saved ROC curve -> {path}")
        plt.close()

    def plot_confusion_matrix(self, model, X_test, y_test, model_name: str, save: bool = True):
        """Plot a styled confusion matrix."""
        cm = confusion_matrix(y_test, model.predict(X_test))
        fig, ax = plt.subplots(figsize=(6, 5))
        fig.patch.set_facecolor("#0d1117"); ax.set_facecolor("#0d1117")
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                    xticklabels=["No Churn","Churn"], yticklabels=["No Churn","Churn"],
                    linewidths=1, linecolor="#1E293B", ax=ax,
                    annot_kws={"size": 14, "weight": "bold", "color": "white"})
        ax.set_xlabel("Predicted", color="#94A3B8"); ax.set_ylabel("Actual", color="#94A3B8")
        ax.set_title(f"Confusion Matrix - {model_name}", color="#E2E8F0", fontsize=13, fontweight="bold")
        ax.tick_params(colors="#94A3B8"); plt.tight_layout()
        if save:
            path = f"{self.output_dir}/confusion_matrix_{model_name}.png"
            plt.savefig(path, dpi=150, bbox_inches="tight", facecolor="#0d1117")
        plt.close()

    def plot_feature_importance(self, model, feature_names: List[str], model_name: str,
                                top_n: int = 15, save: bool = True):
        """Plot feature importances for tree-based models."""
        if not hasattr(model, "feature_importances_"):
            logger.warning(f"{model_name} has no feature_importances_. Skipping.")
            return
        importances = model.feature_importances_
        indices = np.argsort(importances)[-top_n:]
        feats = [feature_names[i] for i in indices]; vals = importances[indices]
        fig, ax = plt.subplots(figsize=(9, 6))
        fig.patch.set_facecolor("#0d1117"); ax.set_facecolor("#0d1117")
        colors = [PALETTE["primary"] if v > np.median(vals) else PALETTE["muted"] for v in vals]
        ax.barh(feats, vals, color=colors, edgecolor="none", height=0.65)
        ax.set_xlabel("Importance Score", color="#94A3B8")
        ax.set_title(f"Feature Importance - {model_name} (Top {top_n})", color="#E2E8F0", fontsize=13, fontweight="bold")
        ax.tick_params(colors="#94A3B8"); ax.spines[:].set_color("#1E293B"); plt.tight_layout()
        if save:
            path = f"{self.output_dir}/feature_importance_{model_name}.png"
            plt.savefig(path, dpi=150, bbox_inches="tight", facecolor="#0d1117")
        plt.close()

    def business_impact(self, model, X_test: np.ndarray, y_test: np.ndarray,
                        avg_customer_value: float = 1200.0, retention_cost: float = 150.0) -> Dict:
        """Translate model accuracy into estimated business value (INR)."""
        y_pred = model.predict(X_test)
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        saved = int(tp); missed = int(fn); alarms = int(fp)
        revenue_saved = saved * avg_customer_value
        retention_spend = (saved + alarms) * retention_cost
        return {
            "churners_caught": saved, "churners_missed": missed, "false_alarms": alarms,
            "estimated_revenue_saved": f"INR {revenue_saved:,.0f}",
            "retention_program_cost": f"INR {retention_spend:,.0f}",
            "net_business_value": f"INR {revenue_saved - retention_spend:,.0f}",
            "revenue_still_at_risk": f"INR {missed * avg_customer_value:,.0f}",
        }
