"""
data_pipeline/data_loader.py - Unified data ingestion: CSV, Excel, Parquet, JSON.
Includes data profiling and synthetic churn dataset generation for demos.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union
import logging

logger = logging.getLogger(__name__)


class DataLoader:
    """Unified data loader supporting multiple file formats.
    Usage: loader = DataLoader(); df = loader.load("data.csv")
    """
    SUPPORTED_FORMATS = {".csv", ".xlsx", ".xls", ".parquet", ".json"}

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)

    def load(self, path: Union[str, Path], **kwargs) -> pd.DataFrame:
        path = Path(path)
        ext = path.suffix.lower()
        if ext not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {ext}")
        readers = {".csv": pd.read_csv, ".xlsx": pd.read_excel, ".xls": pd.read_excel,
                   ".parquet": pd.read_parquet, ".json": pd.read_json}
        logger.info(f"Loading {path}")
        df = readers[ext](path, **kwargs)
        logger.info(f"Loaded {len(df):,} rows x {len(df.columns)} cols")
        return df

    def profile(self, df: pd.DataFrame) -> dict:
        result = {}
        for col in df.columns:
            s = df[col]
            result[col] = {"dtype": str(s.dtype), "nulls": int(s.isna().sum()),
                           "unique": int(s.nunique())}
            if pd.api.types.is_numeric_dtype(s):
                result[col].update({"mean": round(float(s.mean()), 4),
                                    "min": float(s.min()), "max": float(s.max())})
        return result

    def generate_sample_churn_data(self, n: int = 5000, seed: int = 42) -> pd.DataFrame:
        """Generate synthetic customer churn dataset for demos and testing."""
        rng = np.random.default_rng(seed)
        tenure = rng.integers(1, 72, n)
        monthly_charge = rng.uniform(20, 120, n).round(2)
        total_charges = (tenure * monthly_charge * rng.uniform(0.85, 1.15, n)).round(2)
        num_products = rng.integers(1, 5, n)
        support_calls = rng.integers(0, 10, n)
        satisfaction = rng.integers(1, 6, n)
        churn_prob = np.clip(
            0.6 * (1 - tenure / 72) + 0.3 * (monthly_charge / 120) +
            0.2 * (support_calls / 10) - 0.3 * (satisfaction / 5), 0.02, 0.85)
        churn = (rng.random(n) < churn_prob).astype(int)
        return pd.DataFrame({
            "customer_id": [f"CUST{i:05d}" for i in range(n)],
            "tenure_months": tenure, "monthly_charges": monthly_charge,
            "total_charges": total_charges, "num_products": num_products,
            "support_calls": support_calls, "satisfaction_score": satisfaction,
            "contract_type": rng.choice(["Month-to-Month","One Year","Two Year"], n, p=[0.55,0.25,0.20]),
            "payment_method": rng.choice(["Electronic Check","Mailed Check","Bank Transfer","Credit Card"], n),
            "internet_service": rng.choice(["DSL","Fiber Optic","No Internet"], n, p=[0.34,0.44,0.22]),
            "churn": churn,
        })
