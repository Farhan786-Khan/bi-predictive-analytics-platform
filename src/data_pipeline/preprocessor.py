"""
data_pipeline/preprocessor.py
-------------------------------
Feature engineering, encoding, scaling, and train/test splitting.
Sklearn-compatible transformer interface for pipeline integration.
"""
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from typing import List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class FeatureEngineer(BaseEstimator, TransformerMixin):
    """Adds derived features to improve churn prediction:
    - avg_monthly_spend, support_call_rate, engagement_score, charge_variance
    """
    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        df = X.copy()
        if "total_charges" in df.columns and "tenure_months" in df.columns:
            df["avg_monthly_spend"] = (df["total_charges"] / df["tenure_months"].replace(0, 1)).round(2)
        if "support_calls" in df.columns and "tenure_months" in df.columns:
            df["support_call_rate"] = (df["support_calls"] / df["tenure_months"].replace(0, 1)).round(4)
        if "satisfaction_score" in df.columns and "num_products" in df.columns:
            df["engagement_score"] = df["satisfaction_score"] * df["num_products"]
        if "monthly_charges" in df.columns and "total_charges" in df.columns:
            df["charge_variance"] = (df["total_charges"] - df["monthly_charges"] * df["tenure_months"].replace(0, 1)).round(2)
        logger.info(f"Feature engineering complete. Shape: {df.shape}")
        return df


class Preprocessor:
    """Full preprocessing pipeline: engineer -> encode -> scale -> split.

    Usage:
        pp = Preprocessor(target_col="churn", test_size=0.2)
        X_train, X_test, y_train, y_test = pp.fit_transform(df)
        X_new = pp.transform(new_df)  # for inference
    """
    def __init__(self, target_col: str = "churn", test_size: float = 0.2,
                 random_state: int = 42, drop_cols: Optional[List[str]] = None):
        self.target_col = target_col
        self.test_size = test_size
        self.random_state = random_state
        self.drop_cols = drop_cols or ["customer_id"]
        self.scaler = StandardScaler()
        self.feature_engineer = FeatureEngineer()
        self.cat_cols_: List[str] = []
        self.num_cols_: List[str] = []
        self.feature_names_: List[str] = []

    def fit_transform(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Full pipeline: engineer -> encode -> scale -> stratified split."""
        df = self.feature_engineer.fit_transform(df.copy())
        drop = [c for c in self.drop_cols if c in df.columns]
        df.drop(columns=drop, inplace=True)
        y = df.pop(self.target_col).values
        X = df
        self.cat_cols_ = X.select_dtypes(include=["object", "category"]).columns.tolist()
        self.num_cols_ = X.select_dtypes(include=np.number).columns.tolist()
        X = pd.get_dummies(X, columns=self.cat_cols_, drop_first=False)
        X.fillna(X.median(numeric_only=True), inplace=True)
        self.feature_names_ = X.columns.tolist()
        X_scaled = self.scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=self.test_size,
            random_state=self.random_state, stratify=y)
        logger.info(f"Train: {X_train.shape}, Test: {X_test.shape} | "
                    f"Churn train: {y_train.mean():.1%}, test: {y_test.mean():.1%}")
        return X_train, X_test, y_train, y_test

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        """Transform new data using fitted pipeline (inference)."""
        df = self.feature_engineer.transform(df.copy())
        drop = [c for c in self.drop_cols if c in df.columns]
        df.drop(columns=drop + [self.target_col], inplace=True, errors="ignore")
        df = pd.get_dummies(df, columns=self.cat_cols_, drop_first=False)
        for col in self.feature_names_:
            if col not in df.columns:
                df[col] = 0
        df = df[self.feature_names_]
        df.fillna(df.median(numeric_only=True), inplace=True)
        return self.scaler.transform(df)
