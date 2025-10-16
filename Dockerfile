# Multi-stage Dockerfile for Business Intelligence Platform

# Base stage with common dependencies
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

# Copy requirements
COPY requirements.txt requirements-dev.txt ./

# Development stage
FROM base as development

# Install all dependencies including dev dependencies
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy source code
COPY . .

# Change ownership to app user
RUN chown -R app:app /app

USER app

# Expose ports
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production stage
FROM base as production

# Install only production dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code (excluding dev files)
COPY src/ ./src/
COPY config/ ./config/
COPY scripts/ ./scripts/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Change ownership to app user
RUN chown -R app:app /app

USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Production command with gunicorn
CMD ["gunicorn", "src.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]

# Dashboard stage for Plotly Dash
FROM base as dashboard

# Install dashboard-specific dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy dashboard code
COPY src/dashboard/ ./src/dashboard/
COPY src/core/ ./src/core/
COPY src/utils/ ./src/utils/
COPY config/ ./config/

# Change ownership to app user
RUN chown -R app:app /app

USER app

# Expose dashboard port
EXPOSE 8050

# Health check for dashboard
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8050/ || exit 1

# Dashboard command
CMD ["python", "src/dashboard/app.py"]

# ML Training stage
FROM base as ml-training

# Install ML dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional ML tools
RUN pip install --no-cache-dir \
    mlflow==2.9.2 \
    wandb==0.16.1 \
    dvc==3.35.0

# Copy ML training code
COPY src/models/ ./src/models/
COPY src/data/ ./src/data/
COPY src/core/ ./src/core/
COPY src/utils/ ./src/utils/
COPY scripts/train_models.py ./scripts/
COPY config/ ./config/

# Change ownership to app user
RUN chown -R app:app /app

USER app

# Default command for training
CMD ["python", "scripts/train_models.py"]

# Testing stage
FROM development as testing

# Copy test files
COPY tests/ ./tests/
COPY pytest.ini ./
COPY .coveragerc ./

# Run tests
CMD ["pytest", "--cov=src", "--cov-report=html", "--cov-report=term-missing"]