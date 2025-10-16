# Business Intelligence Platform - Makefile
# Provides convenient commands for development, testing, and deployment

.PHONY: help install install-dev test test-cov lint format clean docker-build docker-up docker-down deploy docs

# Default target
help:
	@echo "Business Intelligence Platform - Available Commands:"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  install         Install production dependencies"
	@echo "  install-dev     Install development dependencies"
	@echo "  setup           Complete development setup"
	@echo ""
	@echo "Development:"
	@echo "  run             Run the development server"
	@echo "  run-dashboard   Run the dashboard server"
	@echo "  shell           Start IPython shell with app context"
	@echo ""
	@echo "Code Quality:"
	@echo "  format          Format code with black and isort"
	@echo "  lint            Run linting with flake8"
	@echo "  type-check      Run type checking with mypy"
	@echo "  security-check  Run security checks with bandit"
	@echo "  quality         Run all code quality checks"
	@echo ""
	@echo "Testing:"
	@echo "  test            Run all tests"
	@echo "  test-cov        Run tests with coverage report"
	@echo "  test-unit       Run unit tests only"
	@echo "  test-integration Run integration tests only"
	@echo "  test-performance Run performance tests"
	@echo ""
	@echo "Database:"
	@echo "  db-upgrade      Run database migrations"
	@echo "  db-downgrade    Rollback database migrations"
	@echo "  db-reset        Reset database (WARNING: destroys data)"
	@echo "  db-seed         Seed database with sample data"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build    Build Docker images"
	@echo "  docker-up       Start all services with Docker Compose"
	@echo "  docker-down     Stop all Docker services"
	@echo "  docker-clean    Clean up Docker resources"
	@echo ""
	@echo "Machine Learning:"
	@echo "  train-models    Train all ML models"
	@echo "  evaluate-models Evaluate model performance"
	@echo "  model-metrics   Display model metrics"
	@echo ""
	@echo "Deployment:"
	@echo "  deploy-staging  Deploy to staging environment"
	@echo "  deploy-prod     Deploy to production environment"
	@echo "  backup          Create database backup"
	@echo ""
	@echo "Documentation:"
	@echo "  docs            Generate documentation"
	@echo "  docs-serve      Serve documentation locally"
	@echo ""
	@echo "Utilities:"
	@echo "  clean           Clean up temporary files"
	@echo "  logs            Show application logs"
	@echo "  monitor         Open monitoring dashboard"

# Setup and Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt
	pre-commit install

setup: install-dev
	@echo "Setting up development environment..."
	cp .env.example .env
	@echo "Please edit .env file with your configuration"
	@echo "Then run: make db-upgrade && make db-seed"

# Development
run:
	uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

run-dashboard:
	python src/dashboard/app.py

shell:
	ipython -i -c "from src.main import app; from src.core.database import get_db"

# Code Quality
format:
	black src tests
	isort src tests

lint:
	flake8 src tests

type-check:
	mypy src

security-check:
	bandit -r src -f json -o bandit-report.json
	safety check

quality: format lint type-check security-check
	@echo "All code quality checks completed"

# Testing
test:
	pytest -v

test-cov:
	pytest --cov=src --cov-report=html --cov-report=term-missing --cov-report=xml

test-unit:
	pytest tests/test_models tests/test_api tests/test_core -v

test-integration:
	pytest tests/test_integrations -v

test-performance:
	pytest tests/performance --benchmark-json=benchmark.json

# Database
db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1

db-reset:
	@echo "WARNING: This will destroy all data. Press Ctrl+C to cancel."
	@sleep 5
	alembic downgrade base
	alembic upgrade head

db-seed:
	python scripts/seed_database.py

# Docker
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-clean:
	docker-compose down -v --rmi all
	docker system prune -f

# Machine Learning
train-models:
	python scripts/train_models.py

evaluate-models:
	python scripts/evaluate_models.py

model-metrics:
	python scripts/show_model_metrics.py

# Deployment
deploy-staging:
	@echo "Deploying to staging..."
	docker-compose -f docker-compose.staging.yml up -d

deploy-prod:
	@echo "Deploying to production..."
	@echo "Make sure you have proper access and have run tests!"
	@sleep 3
	docker-compose -f docker-compose.prod.yml up -d

backup:
	python scripts/backup_database.py

# Documentation
docs:
	mkdocs build

docs-serve:
	mkdocs serve

# Utilities
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

logs:
	docker-compose logs -f api

monitor:
	@echo "Opening monitoring dashboard..."
	@echo "Grafana: http://localhost:3000 (admin/admin)"
	@echo "Prometheus: http://localhost:9090"
	@echo "Airflow: http://localhost:8080 (admin/admin)"

# Development helpers
jupyter:
	jupyter lab --ip=0.0.0.0 --port=8888 --allow-root --no-browser

notebook:
	jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --no-browser

# CI/CD helpers
ci-install:
	pip install -r requirements-dev.txt

ci-test: quality test-cov

ci-build: docker-build

# Load testing
load-test:
	locust -f tests/load_testing/locustfile.py --host=http://localhost:8000

# Performance profiling
profile:
	python -m cProfile -o profile.stats src/main.py
	python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(20)"

# Memory profiling
memory-profile:
	python -m memory_profiler src/main.py

# Generate requirements from pip freeze (development helper)
freeze:
	pip freeze > requirements-frozen.txt

# Check for outdated packages
outdated:
	pip list --outdated

# Security audit
audit:
	safety check
	bandit -r src
	pip-audit

# Database inspection
db-inspect:
	python -c "from src.core.database import engine; from sqlalchemy import inspect; print([table for table in inspect(engine).get_table_names()])"

# Generate sample data
generate-data:
	python scripts/generate_sample_data.py

# Stress test the API
stress-test:
	python scripts/stress_test_api.py

# Check service health
health-check:
	curl -f http://localhost:8000/health || exit 1
	curl -f http://localhost:8050/ || exit 1

# Export environment for reproducibility
export-env:
	conda env export > environment.yml

# Quick start for new developers
quickstart: setup docker-up db-upgrade db-seed
	@echo ""
	@echo "🎉 Setup complete! Your BI Platform is ready!"
	@echo ""
	@echo "📊 Dashboard: http://localhost:8050"
	@echo "🔧 API Docs: http://localhost:8000/docs"
	@echo "📈 Monitoring: http://localhost:3000"
	@echo "🔄 Airflow: http://localhost:8080"
	@echo ""
	@echo "Next steps:"
	@echo "1. Edit .env file with your API keys"
	@echo "2. Run 'make train-models' to train ML models"
	@echo "3. Check 'make logs' for any issues"

# Production readiness check
prod-check:
	@echo "Running production readiness checks..."
	@make test-cov
	@make security-check
	@make quality
	@echo "✅ Production readiness check completed"

# Development status
status:
	@echo "Development Environment Status:"
	@echo "================================"
	@docker-compose ps
	@echo ""
	@echo "Recent Git Activity:"
	@git log --oneline -5
	@echo ""
	@echo "Branch Status:"
	@git status --porcelain