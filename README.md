# BI Predictive Analytics Platform

> **Customer Churn Intelligence · Multi-Model ML Pipeline · Interactive BI Dashboard**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-EC4E1D?style=flat-square)](https://xgboost.readthedocs.io)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## What This Is

A **production-grade Business Intelligence platform** combining predictive machine learning with interactive analytics dashboards. Built around **customer churn prediction** — which costs companies billions annually and is a top use case in enterprise AI.

This platform demonstrates the full ML engineering lifecycle:

```
Raw Data -> EDA -> Feature Engineering -> Multi-Model Training -> Evaluation -> Dashboard -> Business Impact
```

---

## Key Results

| Model | F1-Score | ROC-AUC | Accuracy |
|---|---|---|---|
| **Random Forest** | **~0.79** | **~0.88** | **~0.83** |
| XGBoost | ~0.78 | ~0.87 | ~0.82 |
| Gradient Boosting | ~0.76 | ~0.86 | ~0.81 |
| Logistic Regression | ~0.70 | ~0.81 | ~0.76 |

> *Results on 5,000-row synthetic dataset with stratified 5-fold CV.*

---

## Architecture

```
bi-predictive-analytics-platform/
|
+-- src/                          # Core source modules
|   +-- api/                      # FastAPI REST endpoints
|   +-- data_pipeline/
|   |   +-- data_loader.py        # Multi-format ingestion + data profiling
|   |   +-- preprocessor.py      # Feature engineering + sklearn pipeline
|   +-- models/
|   |   +-- classification_models.py  # RF, XGBoost, LightGBM, LogReg suite
|   |   +-- evaluator.py         # Metrics, ROC, confusion matrix, business impact
|   |   +-- prophet-model.py     # Time-series forecasting (Prophet)
|   +-- visualization/
|   |   +-- plotly_charts.py     # Interactive Plotly dark-theme charts
|   +-- utils/
|   +-- main.py                  # FastAPI app entry point
|
+-- dashboard/
|   +-- app.py                   # 5-page Streamlit BI dashboard
|
+-- config/                      # Environment configs
+-- docs/                        # Documentation
+-- scripts/                     # Utility scripts
+-- Dockerfile
+-- docker-compose.yml
+-- pyproject.toml
+-- requirements.txt
```

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/Farhan786-Khan/bi-predictive-analytics-platform.git
cd bi-predictive-analytics-platform

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the interactive Streamlit dashboard
streamlit run dashboard/app.py

# 5. OR run the FastAPI backend
uvicorn src.main:app --reload
```

---

## Dashboard Pages

| Page | What It Shows |
|------|--------------|
| **Overview** | Dataset KPIs, data preview, feature summary |
| **EDA** | 5 interactive Plotly charts: churn dist, tenure violin, charges scatter, contract heatmap, satisfaction bar |
| **Models** | Live training, leaderboard, CV results, model comparison chart |
| **Predict** | Single customer churn predictor with gauge chart |
| **Business Impact** | Revenue saved, retention ROI, at-risk revenue calculator (INR) |

---

## ML Engineering Highlights

**Feature Engineering** (`src/data_pipeline/preprocessor.py`)
- Derived features: `avg_monthly_spend`, `support_call_rate`, `engagement_score`, `charge_variance`
- Sklearn-compatible `TransformerMixin` for pipeline integration
- Stratified train/test split preserving class balance

**Multi-Model Suite** (`src/models/classification_models.py`)
- 4 models with unified interface: Logistic Regression, Random Forest, XGBoost, LightGBM
- 5-fold Stratified Cross Validation on F1, ROC-AUC, Accuracy
- Model persistence with `joblib` + `best_model()` selector

**Time-Series Forecasting** (`src/models/prophet-model.py`)
- Meta Prophet with multiplicative seasonality
- Hyperparameter tuning and cross-validation
- Churn trend forecasting over time

**Business Impact Quantification** (`src/models/evaluator.py`)
- Translates model metrics into INR revenue saved / at risk
- Configurable customer value and retention campaign cost
- False alarm vs missed churn cost trade-off analysis

**REST API** (`src/main.py`)
- FastAPI backend with Prometheus monitoring
- Endpoints: /predict, /anomaly, /prescriptive, /dashboard
- Docker + docker-compose for easy deployment

---

## Customise for Your Data

```python
from src.data_pipeline.data_loader import DataLoader
from src.data_pipeline.preprocessor import Preprocessor
from src.models.classification_models import ModelSuite

loader = DataLoader()
df = loader.load("your_data.csv")

preprocessor = Preprocessor(target_col="your_churn_column")
X_train, X_test, y_train, y_test = preprocessor.fit_transform(df)

suite = ModelSuite()
suite.train_all(X_train, y_train)
print("Best model:", suite.best_model("f1"))
```

---

## Roadmap

- [x] Multi-model classification suite (RF, XGBoost, LightGBM, LogReg)
- [x] Prophet time-series forecasting
- [x] FastAPI REST backend with Prometheus monitoring
- [x] 5-page Streamlit interactive dashboard
- [x] Docker + docker-compose deployment
- [ ] SHAP values for model explainability
- [ ] Hyperparameter tuning with Optuna
- [ ] Real-time data ingestion from SQL / Kafka
- [ ] Automated HTML report generation

---

## Author

**Mohammed Farhan Khan**
*AI/ML Engineer · Data Scientist · Bengaluru, India*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/mohammed-farhan-55976920b)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github)](https://github.com/Farhan786-Khan)
[![Email](https://img.shields.io/badge/Email-Contact-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:mfk78686@gmail.com)

---

## License

MIT License — free to use, modify, and distribute with attribution.
