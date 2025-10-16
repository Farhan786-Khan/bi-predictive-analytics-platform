# Business Intelligence Platform - Environment Configuration
# Copy this file to .env and update the values with your actual credentials

# =============================================================================
# APPLICATION SETTINGS
# =============================================================================

# Environment (development, testing, staging, production)
ENVIRONMENT=development

# Debug mode (true/false)
DEBUG=true

# Application host and port
HOST=0.0.0.0
PORT=8000

# Allowed origins for CORS (comma-separated)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,http://localhost:8050

# Allowed hosts (comma-separated)
ALLOWED_HOSTS=localhost,127.0.0.1

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

# PostgreSQL database URL
DATABASE_URL=postgresql://postgres:password@localhost:5432/bi_platform

# Database connection pool settings
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
DATABASE_ECHO=false

# =============================================================================
# REDIS CONFIGURATION
# =============================================================================

# Redis connection URL
REDIS_URL=redis://localhost:6379

# Redis connection pool settings
REDIS_MAX_CONNECTIONS=50

# =============================================================================
# SECURITY SETTINGS
# =============================================================================

# Secret key for JWT tokens (generate a strong random key)
SECRET_KEY=your-super-secret-key-change-this-in-production

# Token expiration times
ACCESS_TOKEN_EXPIRES_MINUTES=30
REFRESH_TOKEN_EXPIRES_DAYS=7

# =============================================================================
# EXTERNAL API KEYS
# =============================================================================

# Yahoo Finance API Key
YAHOO_FINANCE_API_KEY=your_yahoo_finance_api_key

# Alpha Vantage API Key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key

# World Bank API Key (optional)
WORLD_BANK_API_KEY=your_world_bank_api_key

# =============================================================================
# INTEGRATION SETTINGS
# =============================================================================

# Slack Integration
SLACK_TOKEN=xoxb-your-slack-bot-token
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/your/webhook/url

# Telegram Bot Integration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# Microsoft Teams Integration (optional)
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/your-teams-webhook

# =============================================================================
# EMAIL CONFIGURATION
# =============================================================================

# SendGrid API Key
SENDGRID_API_KEY=SG.your_sendgrid_api_key

# From email address
FROM_EMAIL=noreply@your-domain.com

# Admin email addresses (comma-separated)
ADMIN_EMAILS=admin@your-domain.com,alerts@your-domain.com

# =============================================================================
# MACHINE LEARNING SETTINGS
# =============================================================================

# Model cache TTL (seconds)
MODEL_CACHE_TTL=3600

# Model retrain interval (seconds)
MODEL_RETRAIN_INTERVAL=86400

# Forecasting settings
FORECAST_HORIZON_DAYS=90
CONFIDENCE_LEVEL=0.95

# =============================================================================
# FEATURE FLAGS
# =============================================================================

# Enable/disable features
ENABLE_ANOMALY_DETECTION=true
ENABLE_PRESCRIPTIVE_ANALYTICS=true
ENABLE_REAL_TIME_SCORING=true

# =============================================================================
# MONITORING & LOGGING
# =============================================================================

# Enable Prometheus metrics
ENABLE_METRICS=true
METRICS_PORT=9090

# Logging configuration
LOG_LEVEL=INFO
LOG_FORMAT=json

# =============================================================================
# RATE LIMITING
# =============================================================================

# API rate limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# =============================================================================
# AIRFLOW CONFIGURATION
# =============================================================================

# Airflow settings
AIRFLOW_WEBSERVER_PORT=8080
AIRFLOW_DAG_DIR=./dags

# Airflow database (separate from main app database)
AIRFLOW_DATABASE_URL=postgresql://airflow:airflow@localhost:5432/airflow

# =============================================================================
# CLOUD PROVIDER SETTINGS (Optional)
# =============================================================================

# AWS Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-1
AWS_S3_BUCKET=your-bi-platform-bucket

# Azure Configuration
AZURE_STORAGE_CONNECTION_STRING=your_azure_connection_string
AZURE_CONTAINER_NAME=bi-platform-data

# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/gcp-credentials.json
GCP_PROJECT_ID=your-gcp-project-id
GCP_BUCKET_NAME=your-gcp-bucket

# =============================================================================
# DEVELOPMENT SETTINGS
# =============================================================================

# Development-specific settings
RELOAD_ON_CHANGE=true
ENABLE_PROFILING=false

# Testing database (only for testing environment)
TEST_DATABASE_URL=postgresql://postgres:password@localhost:5432/test_bi_platform

# =============================================================================
# PRODUCTION SETTINGS
# =============================================================================

# Production-specific settings (uncomment for production)
# WORKERS=4
# MAX_REQUESTS=1000
# MAX_REQUESTS_JITTER=50
# TIMEOUT=30
# KEEPALIVE=2

# SSL/TLS settings (for production)
# SSL_CERT_PATH=/path/to/cert.pem
# SSL_KEY_PATH=/path/to/key.pem

# =============================================================================
# DOCKER SETTINGS
# =============================================================================

# Docker-specific environment variables
COMPOSE_PROJECT_NAME=bi-platform
COMPOSE_FILE=docker-compose.yml

# =============================================================================
# BACKUP & RECOVERY
# =============================================================================

# Backup settings
BACKUP_RETENTION_DAYS=30
BACKUP_S3_BUCKET=your-backup-bucket

# =============================================================================
# CUSTOM BUSINESS LOGIC
# =============================================================================

# Business-specific settings
DEFAULT_CURRENCY=USD
DEFAULT_TIMEZONE=UTC
BUSINESS_HOURS_START=09:00
BUSINESS_HOURS_END=17:00

# Alert thresholds
REVENUE_ALERT_THRESHOLD=0.1
ANOMALY_SENSITIVITY=0.95

# =============================================================================
# THIRD-PARTY INTEGRATIONS
# =============================================================================

# OpenAI API (for advanced NLP features)
OPENAI_API_KEY=your_openai_api_key

# Weights & Biases (for ML experiment tracking)
WANDB_API_KEY=your_wandb_api_key
WANDB_PROJECT=bi-platform

# MLflow (for model registry)
MLFLOW_TRACKING_URI=http://localhost:5000

# =============================================================================
# PERFORMANCE TUNING
# =============================================================================

# Database connection tuning
DB_POOL_PRE_PING=true
DB_POOL_RECYCLE=3600

# Redis connection tuning
REDIS_SOCKET_KEEPALIVE=true
REDIS_SOCKET_KEEPALIVE_OPTIONS={}

# =============================================================================
# SECURITY HEADERS
# =============================================================================

# Security headers configuration
ENABLE_HSTS=true
HSTS_MAX_AGE=31536000
ENABLE_CSP=true
CSP_DEFAULT_SRC='self'

# =============================================================================
# API DOCUMENTATION
# =============================================================================

# API documentation settings
API_DOCS_URL=/docs
API_REDOC_URL=/redoc
OPENAPI_URL=/openapi.json

# =============================================================================
# NOTIFICATIONS
# =============================================================================

# Notification settings
ALERT_COOLDOWN_MINUTES=30
MAX_ALERTS_PER_HOUR=10
NOTIFICATION_RETRY_ATTEMPTS=3