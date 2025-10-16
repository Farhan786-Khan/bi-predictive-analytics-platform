"""
Configuration management for the Business Intelligence Platform.
"""

import os
from functools import lru_cache
from typing import List, Optional

from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    app_name: str = "Business Intelligence Platform"
    version: str = "1.0.0"
    debug: bool = Field(default=False, env="DEBUG")
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        env="ALLOWED_ORIGINS"
    )
    allowed_hosts: List[str] = Field(
        default=["localhost", "127.0.0.1"],
        env="ALLOWED_HOSTS"
    )
    
    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    database_echo: bool = Field(default=False, env="DATABASE_ECHO")
    database_pool_size: int = Field(default=10, env="DATABASE_POOL_SIZE")
    database_max_overflow: int = Field(default=20, env="DATABASE_MAX_OVERFLOW")
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    redis_decode_responses: bool = True
    redis_max_connections: int = Field(default=50, env="REDIS_MAX_CONNECTIONS")
    
    # Security
    secret_key: str = Field(..., env="SECRET_KEY")
    access_token_expires_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRES_MINUTES")
    refresh_token_expires_days: int = Field(default=7, env="REFRESH_TOKEN_EXPIRES_DAYS")
    algorithm: str = "HS256"
    
    # API Keys
    yahoo_finance_api_key: Optional[str] = Field(None, env="YAHOO_FINANCE_API_KEY")
    alpha_vantage_api_key: Optional[str] = Field(None, env="ALPHA_VANTAGE_API_KEY")
    world_bank_api_key: Optional[str] = Field(None, env="WORLD_BANK_API_KEY")
    
    # Integrations
    slack_token: Optional[str] = Field(None, env="SLACK_TOKEN")
    slack_webhook_url: Optional[str] = Field(None, env="SLACK_WEBHOOK_URL")
    telegram_bot_token: Optional[str] = Field(None, env="TELEGRAM_BOT_TOKEN")
    telegram_chat_id: Optional[str] = Field(None, env="TELEGRAM_CHAT_ID")
    
    # Email
    sendgrid_api_key: Optional[str] = Field(None, env="SENDGRID_API_KEY")
    from_email: str = Field(default="noreply@bi-platform.com", env="FROM_EMAIL")
    
    # ML Models
    model_cache_ttl: int = Field(default=3600, env="MODEL_CACHE_TTL")  # 1 hour
    model_retrain_interval: int = Field(default=86400, env="MODEL_RETRAIN_INTERVAL")  # 24 hours
    forecast_horizon_days: int = Field(default=90, env="FORECAST_HORIZON_DAYS")
    confidence_level: float = Field(default=0.95, env="CONFIDENCE_LEVEL")
    
    # Monitoring
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    metrics_port: int = Field(default=9090, env="METRICS_PORT")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")
    
    # Feature Flags
    enable_anomaly_detection: bool = Field(default=True, env="ENABLE_ANOMALY_DETECTION")
    enable_prescriptive_analytics: bool = Field(default=True, env="ENABLE_PRESCRIPTIVE_ANALYTICS")
    enable_real_time_scoring: bool = Field(default=True, env="ENABLE_REAL_TIME_SCORING")
    
    # Rate Limiting
    rate_limit_requests: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=60, env="RATE_LIMIT_WINDOW")  # seconds
    
    # Airflow
    airflow_webserver_port: int = Field(default=8080, env="AIRFLOW_WEBSERVER_PORT")
    airflow_dag_dir: str = Field(default="./dags", env="AIRFLOW_DAG_DIR")
    
    @validator("database_url")
    def validate_database_url(cls, v):
        """Validate database URL format."""
        if not v.startswith(("postgresql://", "postgresql+asyncpg://")):
            raise ValueError("Database URL must be a PostgreSQL connection string")
        return v
    
    @validator("allowed_origins", pre=True)
    def validate_allowed_origins(cls, v):
        """Parse allowed origins from string if needed."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("allowed_hosts", pre=True)
    def validate_allowed_hosts(cls, v):
        """Parse allowed hosts from string if needed."""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    @validator("confidence_level")
    def validate_confidence_level(cls, v):
        """Validate confidence level is between 0 and 1."""
        if not 0 < v < 1:
            raise ValueError("Confidence level must be between 0 and 1")
        return v
    
    @validator("log_level")
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class DevelopmentSettings(Settings):
    """Development environment settings."""
    debug: bool = True
    environment: str = "development"
    database_echo: bool = True
    log_level: str = "DEBUG"


class ProductionSettings(Settings):
    """Production environment settings."""
    debug: bool = False
    environment: str = "production"
    database_echo: bool = False
    log_level: str = "INFO"


class TestingSettings(Settings):
    """Testing environment settings."""
    debug: bool = True
    environment: str = "testing"
    database_url: str = "postgresql://postgres:password@localhost:5432/test_bi_platform"
    redis_url: str = "redis://localhost:6379/1"


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings based on environment.
    Uses LRU cache to avoid repeated environment variable lookups.
    """
    environment = os.getenv("ENVIRONMENT", "development").lower()
    
    if environment == "production":
        return ProductionSettings()
    elif environment == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()


# Global settings instance
settings = get_settings()