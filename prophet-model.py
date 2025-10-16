"""
Prophet-based time series forecasting model for business metrics.
"""

import logging
import pickle
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any

import numpy as np
import pandas as pd
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import joblib

from src.models.base_model import BaseModel
from src.utils.exceptions import ModelTrainingException, PredictionException


logger = logging.getLogger(__name__)


class ProphetForecastingModel(BaseModel):
    """
    Prophet-based forecasting model with advanced features and hyperparameter optimization.
    """
    
    def __init__(
        self,
        name: str = "prophet_forecasting",
        seasonality_mode: str = "multiplicative",
        changepoint_prior_scale: float = 0.05,
        seasonality_prior_scale: float = 10.0,
        holidays_prior_scale: float = 10.0,
        mcmc_samples: int = 0,
        interval_width: float = 0.95,
        uncertainty_samples: int = 1000,
        **kwargs
    ):
        super().__init__(name=name, **kwargs)
        
        self.seasonality_mode = seasonality_mode
        self.changepoint_prior_scale = changepoint_prior_scale
        self.seasonality_prior_scale = seasonality_prior_scale
        self.holidays_prior_scale = holidays_prior_scale
        self.mcmc_samples = mcmc_samples
        self.interval_width = interval_width
        self.uncertainty_samples = uncertainty_samples
        
        self.model: Optional[Prophet] = None
        self.feature_columns: List[str] = []
        self.target_column: str = ""
        self.training_metrics: Dict[str, float] = {}
        
    def prepare_data(self, df: pd.DataFrame, target_col: str, date_col: str = "ds") -> pd.DataFrame:
        """
        Prepare data for Prophet model training.
        
        Args:
            df: Input dataframe
            target_col: Target column name
            date_col: Date column name
            
        Returns:
            Prepared dataframe with Prophet format
        """
        try:
            # Create a copy of the dataframe
            data = df.copy()
            
            # Rename columns to Prophet format
            if date_col != "ds":
                data = data.rename(columns={date_col: "ds"})
            if target_col != "y":
                data = data.rename(columns={target_col: "y"})
            
            # Ensure ds column is datetime
            data["ds"] = pd.to_datetime(data["ds"])
            
            # Sort by date
            data = data.sort_values("ds").reset_index(drop=True)
            
            # Handle missing values
            data["y"] = data["y"].fillna(method="ffill").fillna(method="bfill")
            
            # Remove outliers using IQR method
            Q1 = data["y"].quantile(0.25)
            Q3 = data["y"].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Cap outliers instead of removing them
            data["y"] = data["y"].clip(lower=lower_bound, upper=upper_bound)
            
            logger.info(f"Prepared data with {len(data)} records")
            return data
            
        except Exception as e:
            raise ModelTrainingException(f"Data preparation failed: {str(e)}")
    
    def add_regressors(self, model: Prophet, data: pd.DataFrame) -> Prophet:
        """
        Add external regressors to the Prophet model.
        
        Args:
            model: Prophet model instance
            data: Dataframe containing regressor columns
            
        Returns:
            Prophet model with added regressors
        """
        # Add common business regressors
        regressor_columns = [col for col in data.columns if col not in ["ds", "y"]]
        
        for col in regressor_columns:
            if data[col].dtype in [np.float64, np.int64, np.float32, np.int32]:
                model.add_regressor(col)
                self.feature_columns.append(col)
                logger.info(f"Added regressor: {col}")
        
        return model
    
    def add_custom_seasonalities(self, model: Prophet) -> Prophet:
        """
        Add custom seasonalities relevant to business data.
        
        Args:
            model: Prophet model instance
            
        Returns:
            Prophet model with custom seasonalities
        """
        # Add quarterly seasonality for business metrics
        model.add_seasonality(
            name="quarterly",
            period=365.25/4,
            fourier_order=5
        )
        
        # Add monthly seasonality
        model.add_seasonality(
            name="monthly",
            period=30.5,
            fourier_order=3
        )
        
        logger.info("Added custom seasonalities: quarterly, monthly")
        return model
    
    def fit(self, data: pd.DataFrame, target_col: str, date_col: str = "ds") -> 'ProphetForecastingModel':
        """
        Train the Prophet model.
        
        Args:
            data: Training data
            target_col: Target column name
            date_col: Date column name
            
        Returns:
            Trained model instance
        """
        try:
            logger.info("Starting Prophet model training...")
            
            # Prepare data
            prepared_data = self.prepare_data(data, target_col, date_col)
            self.target_column = target_col
            
            # Initialize Prophet model
            self.model = Prophet(
                seasonality_mode=self.seasonality_mode,
                changepoint_prior_scale=self.changepoint_prior_scale,
                seasonality_prior_scale=self.seasonality_prior_scale,
                holidays_prior_scale=self.holidays_prior_scale,
                mcmc_samples=self.mcmc_samples,
                interval_width=self.interval_width,
                uncertainty_samples=self.uncertainty_samples,
                daily_seasonality=False,
                weekly_seasonality=True,
                yearly_seasonality=True
            )
            
            # Add custom seasonalities
            self.model = self.add_custom_seasonalities(self.model)
            
            # Add regressors
            self.model = self.add_regressors(self.model, prepared_data)
            
            # Add country holidays (US by default)
            self.model.add_country_holidays(country_name='US')
            
            # Fit the model
            self.model.fit(prepared_data)
            
            # Calculate training metrics
            self._calculate_training_metrics(prepared_data)
            
            # Update metadata
            self.metadata.update({
                "training_samples": len(prepared_data),
                "feature_columns": self.feature_columns,
                "target_column": self.target_column,
                "training_date": datetime.now().isoformat(),
                "model_params": {
                    "seasonality_mode": self.seasonality_mode,
                    "changepoint_prior_scale": self.changepoint_prior_scale,
                    "seasonality_prior_scale": self.seasonality_prior_scale,
                    "holidays_prior_scale": self.holidays_prior_scale
                }
            })
            
            logger.info("Prophet model training completed successfully")
            return self
            
        except Exception as e:
            raise ModelTrainingException(f"Prophet model training failed: {str(e)}")
    
    def predict(
        self, 
        periods: int = 30, 
        freq: str = 'D',
        include_history: bool = True,
        future_regressors: Optional[pd.DataFrame] = None
    ) -> pd.DataFrame:
        """
        Generate forecasts using the trained Prophet model.
        
        Args:
            periods: Number of periods to forecast
            freq: Frequency of predictions ('D' for daily, 'W' for weekly, etc.)
            include_history: Whether to include historical fitted values
            future_regressors: Future values for regressors
            
        Returns:
            Dataframe with forecasts and confidence intervals
        """
        if self.model is None:
            raise PredictionException("Model has not been trained yet")
        
        try:
            # Create future dataframe
            future = self.model.make_future_dataframe(periods=periods, freq=freq, include_history=include_history)
            
            # Add future regressor values if provided
            if future_regressors is not None and len(self.feature_columns) > 0:
                for col in self.feature_columns:
                    if col in future_regressors.columns:
                        # Merge future regressor values
                        future = future.merge(
                            future_regressors[['ds', col]], 
                            on='ds', 
                            how='left'
                        )
                        # Forward fill missing values
                        future[col] = future[col].fillna(method='ffill')
            
            # Generate predictions
            forecast = self.model.predict(future)
            
            # Add additional metrics
            forecast['prediction_date'] = datetime.now()
            forecast['model_name'] = self.name
            forecast['confidence_width'] = forecast['yhat_upper'] - forecast['yhat_lower']
            forecast['relative_uncertainty'] = forecast['confidence_width'] / np.abs(forecast['yhat'])
            
            logger.info(f"Generated {len(forecast)} predictions")
            return forecast
            
        except Exception as e:
            raise PredictionException(f"Prediction failed: {str(e)}")
    
    def _calculate_training_metrics(self, data: pd.DataFrame):
        """Calculate and store training metrics."""
        try:
            # In-sample predictions
            forecast = self.model.predict(data)
            
            # Calculate metrics
            mape = mean_absolute_percentage_error(data['y'], forecast['yhat'])
            rmse = np.sqrt(mean_squared_error(data['y'], forecast['yhat']))
            mae = np.mean(np.abs(data['y'] - forecast['yhat']))
            
            self.training_metrics = {
                'mape': float(mape),
                'rmse': float(rmse),
                'mae': float(mae),
                'r2': float(np.corrcoef(data['y'], forecast['yhat'])[0, 1] ** 2)
            }
            
            logger.info(f"Training metrics - MAPE: {mape:.4f}, RMSE: {rmse:.4f}")
            
        except Exception as e:
            logger.warning(f"Could not calculate training metrics: {str(e)}")
    
    def cross_validate(
        self, 
        data: pd.DataFrame, 
        horizon: str = '30 days',
        initial: str = '365 days',
        period: str = '30 days',
        parallel: str = None
    ) -> pd.DataFrame:
        """
        Perform cross-validation on the model.
        
        Args:
            data: Historical data
            horizon: Forecast horizon for each split
            initial: Initial training period
            period: Period between cutoff dates
            parallel: Parallelization method
            
        Returns:
            Cross-validation results
        """
        if self.model is None:
            raise PredictionException("Model has not been trained yet")
        
        try:
            # Prepare data
            prepared_data = self.prepare_data(data, self.target_column)
            
            # Perform cross-validation
            cv_results = cross_validation(
                self.model,
                prepared_data,
                horizon=horizon,
                initial=initial,
                period=period,
                parallel=parallel
            )
            
            # Calculate performance metrics
            performance = performance_metrics(cv_results)
            
            logger.info(f"Cross-validation completed with {len(cv_results)} splits")
            return cv_results, performance
            
        except Exception as e:
            raise ModelTrainingException(f"Cross-validation failed: {str(e)}")
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance from the trained model.
        
        Returns:
            Dictionary of feature importance scores
        """
        if self.model is None:
            return {}
        
        try:
            # Get regressor coefficients
            importance = {}
            
            if hasattr(self.model, 'extra_regressors'):
                for regressor in self.model.extra_regressors:
                    # Get the regressor coefficient from the model
                    regressor_coef = self.model.extra_regressors[regressor].get('coef', 0)
                    importance[regressor] = abs(float(regressor_coef))
            
            return importance
            
        except Exception as e:
            logger.warning(f"Could not calculate feature importance: {str(e)}")
            return {}
    
    def save_model(self, filepath: str):
        """Save the trained model to disk."""
        if self.model is None:
            raise ValueError("No model to save")
        
        try:
            model_data = {
                'model': self.model,
                'feature_columns': self.feature_columns,
                'target_column': self.target_column,
                'training_metrics': self.training_metrics,
                'metadata': self.metadata
            }
            
            joblib.dump(model_data, filepath)
            logger.info(f"Prophet model saved to {filepath}")
            
        except Exception as e:
            raise Exception(f"Failed to save model: {str(e)}")
    
    def load_model(self, filepath: str):
        """Load a trained model from disk."""
        try:
            model_data = joblib.load(filepath)
            
            self.model = model_data['model']
            self.feature_columns = model_data['feature_columns']
            self.target_column = model_data['target_column']
            self.training_metrics = model_data['training_metrics']
            self.metadata = model_data['metadata']
            
            logger.info(f"Prophet model loaded from {filepath}")
            
        except Exception as e:
            raise Exception(f"Failed to load model: {str(e)}")
    
    def get_model_summary(self) -> Dict[str, Any]:
        """Get a summary of the trained model."""
        if self.model is None:
            return {"status": "not_trained"}
        
        return {
            "model_name": self.name,
            "model_type": "Prophet Forecasting",
            "training_metrics": self.training_metrics,
            "feature_columns": self.feature_columns,
            "target_column": self.target_column,
            "model_params": {
                "seasonality_mode": self.seasonality_mode,
                "changepoint_prior_scale": self.changepoint_prior_scale,
                "seasonality_prior_scale": self.seasonality_prior_scale,
                "holidays_prior_scale": self.holidays_prior_scale,
            },
            "metadata": self.metadata
        }