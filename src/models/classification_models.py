"""
models/classification_models.py
---------------------------------
Multi-model ML classification suite: Logistic Regression, Random Forest,
Gradient Boosting, XGBoost, LightGBM.

Integrates with the bi-predictive-analytics-platform architecture.
Companion to src/models/prophet-model.py (time-series forecasting).
"""
import numpy as np
import joblib
from pathlib import Path
from typing import Dict, Any, Optional
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
import logging

try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

try:
    from lightgbm import LGBMClassifier
    HAS_LGB = True
except ImportError:
    HAS_LGB = False

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Default model registry
# ---------------------------------------------------------------------------
MODELS: Dict[str, Any] = {
    "logistic_regression": LogisticRegression(
        C=1.0, max_iter=1000, random_state=42, class_weight="balanced"
    ),
    "random_forest": RandomForestClassifier(
        n_estimators=200, max_depth=10, min_samples_leaf=5,
        class_weight="balanced", random_state=42, n_jobs=-1
    ),
    "gradient_boosting": GradientBoostingClassifier(
        n_estimators=200, learning_rate=0.05, max_depth=4,
        subsample=0.8, random_state=42
    ),
}

PARAM_GRIDS: Dict[str, Dict] = {
    "logistic_regression": {"C": [0.01, 0.1, 1.0, 10.0], "solver": ["lbfgs", "saga"]},
    "random_forest": {"n_estimators": [100, 200, 300], "max_depth": [6, 10, None], "min_samples_leaf": [2, 5, 10]},
    "gradient_boosting": {"n_estimators": [100, 200], "learning_rate": [0.01, 0.05, 0.1], "max_depth": [3, 4, 5]},
}

if HAS_XGB:
    MODELS["xgboost"] = XGBClassifier(
        n_estimators=200, learning_rate=0.05, max_depth=4,
        subsample=0.8, colsample_bytree=0.8, eval_metric="logloss",
        random_state=42, n_jobs=-1
    )
    PARAM_GRIDS["xgboost"] = {"n_estimators": [100, 200], "learning_rate": [0.01, 0.05, 0.1], "max_depth": [3, 4, 6]}

if HAS_LGB:
    MODELS["lightgbm"] = LGBMClassifier(
        n_estimators=200, learning_rate=0.05, max_depth=4,
        random_state=42, n_jobs=-1, verbose=-1
    )


class ModelSuite:
    """
    Train, evaluate, compare, and persist all classification models.
    Provides a unified interface with stratified 5-fold cross-validation.

    Usage:
        suite = ModelSuite(cv_folds=5, save_dir="models/saved")
        suite.train_all(X_train, y_train)
        best = suite.best_model("f1")
        suite.save_all()
    """

    def __init__(self, cv_folds: int = 5, save_dir: str = "models/saved"):
        self.cv_folds = cv_folds
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.trained_models: Dict[str, Any] = {}
        self.cv_results: Dict[str, Dict] = {}

    def train_all(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        models: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Train all models with stratified cross-validation scoring."""
        model_dict = models or MODELS
        cv = StratifiedKFold(n_splits=self.cv_folds, shuffle=True, random_state=42)

        for name, model in model_dict.items():
            logger.info(f"Training {name}...")
            model.fit(X_train, y_train)
            self.trained_models[name] = model

            for metric in ["f1", "roc_auc", "accuracy"]:
                scores = cross_val_score(
                    model, X_train, y_train, cv=cv, scoring=metric, n_jobs=-1
                )
                if name not in self.cv_results:
                    self.cv_results[name] = {}
                self.cv_results[name][metric] = {
                    "mean": round(scores.mean(), 4),
                    "std": round(scores.std(), 4),
                    "scores": scores.tolist(),
                }
            logger.info(
                f"  {name} -> F1: {self.cv_results[name]['f1']['mean']:.4f} "
                f"+/- {self.cv_results[name]['f1']['std']:.4f}"
            )
        return self.trained_models

    def save(self, name: str):
        """Persist a single trained model to disk via joblib."""
        if name not in self.trained_models:
            raise ValueError(f"Model '{name}' not yet trained.")
        path = self.save_dir / f"{name}.joblib"
        joblib.dump(self.trained_models[name], path)
        logger.info(f"Saved {name} -> {path}")

    def load(self, name: str):
        """Load a persisted model from disk."""
        path = self.save_dir / f"{name}.joblib"
        model = joblib.load(path)
        self.trained_models[name] = model
        return model

    def save_all(self):
        """Save all trained models to disk."""
        for name in self.trained_models:
            self.save(name)

    def best_model(self, metric: str = "f1") -> str:
        """Return the name of the best-performing model by CV metric."""
        if not self.cv_results:
            raise ValueError("No CV results yet. Call train_all() first.")
        return max(
            self.cv_results,
            key=lambda n: self.cv_results[n].get(metric, {}).get("mean", 0)
        )
