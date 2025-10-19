import os
from pathlib import Path

# Create the complete GitHub repository structure
repo_structure = {
    "bi-predictive-analytics-platform": {
        # Root files
        "README.md": "main_readme",
        "LICENSE": "license_file",
        ".gitignore": "gitignore_file",
        "requirements.txt": "requirements_file",
        "requirements-dev.txt": "dev_requirements_file",
        "docker-compose.yml": "docker_compose_file",
        "docker-compose.prod.yml": "docker_compose_prod_file",
        "Dockerfile": "dockerfile",
        ".env.example": "env_example",
        "setup.py": "setup_file",
        "pyproject.toml": "pyproject_file",
        "Makefile": "makefile",
        
        # GitHub workflows
        ".github": {
            "workflows": {
                "ci-cd.yml": "cicd_workflow",
                "test.yml": "test_workflow",
                "security.yml": "security_workflow"
            },
            "ISSUE_TEMPLATE": {
                "bug_report.md": "bug_template",
                "feature_request.md": "feature_template"
            },
            "pull_request_template.md": "pr_template"
        },
        
        # Source code
        "src": {
            "__init__.py": "empty",
            "main.py": "main_app",
            
            # API layer
            "api": {
                "__init__.py": "empty",
                "main.py": "api_main",
                "dependencies.py": "api_dependencies",
                "routes": {
                    "__init__.py": "empty",
                    "predictions.py": "predictions_routes",
                    "anomaly.py": "anomaly_routes",
                    "prescriptive.py": "prescriptive_routes",
                    "dashboard.py": "dashboard_routes"
                }
            },
            
            # Core business logic
            "core": {
                "__init__.py": "empty",
                "config.py": "config_file",
                "database.py": "database_config",
                "security.py": "security_config",
                "logging.py": "logging_config"
            },
            
            # Data processing
            "data": {
                "__init__.py": "empty",
                "connectors": {
                    "__init__.py": "empty",
                    "base_connector.py": "base_connector",
                    "yahoo_finance.py": "yahoo_connector",
                    "alpha_vantage.py": "alpha_vantage_connector",
                    "world_bank.py": "world_bank_connector"
                },
                "processors": {
                    "__init__.py": "empty",
                    "data_cleaner.py": "data_cleaner",
                    "feature_engineer.py": "feature_engineer",
                    "validator.py": "data_validator"
                }
            },
            
            # Machine Learning models
            "models": {
                "__init__.py": "empty",
                "base_model.py": "base_model",
                "forecasting": {
                    "__init__.py": "empty",
                    "prophet_model.py": "prophet_model",
                    "lstm_model.py": "lstm_model",
                    "ensemble_model.py": "ensemble_model"
                },
                "anomaly": {
                    "__init__.py": "empty",
                    "isolation_forest.py": "isolation_forest",
                    "lstm_autoencoder.py": "lstm_autoencoder",
                    "statistical_detector.py": "statistical_detector"
                },
                "prescriptive": {
                    "__init__.py": "empty",
                    "scenario_simulator.py": "scenario_simulator",
                    "optimizer.py": "optimizer",
                    "recommendation_engine.py": "recommendation_engine"
                }
            },
            
            # Dashboard
            "dashboard": {
                "__init__.py": "empty",
                "app.py": "dashboard_app",
                "layouts": {
                    "__init__.py": "empty",
                    "executive.py": "executive_layout",
                    "financial.py": "financial_layout",
                    "sales.py": "sales_layout"
                },
                "components": {
                    "__init__.py": "empty",
                    "charts.py": "chart_components",
                    "filters.py": "filter_components",
                    "tables.py": "table_components"
                }
            },
            
            # Integrations
            "integrations": {
                "__init__.py": "empty",
                "slack_bot.py": "slack_bot",
                "telegram_bot.py": "telegram_bot",
                "teams_bot.py": "teams_bot",
                "email_service.py": "email_service"
            },
            
            # Utilities
            "utils": {
                "__init__.py": "empty",
                "helpers.py": "helper_functions",
                "decorators.py": "custom_decorators",
                "exceptions.py": "custom_exceptions"
            }
        },
        
        # Tests
        "tests": {
            "__init__.py": "empty",
            "conftest.py": "pytest_config",
            "test_api": {
                "__init__.py": "empty",
                "test_predictions.py": "test_predictions",
                "test_anomaly.py": "test_anomaly"
            },
            "test_models": {
                "__init__.py": "empty",
                "test_forecasting.py": "test_forecasting",
                "test_anomaly_detection.py": "test_anomaly_detection"
            },
            "test_integrations": {
                "__init__.py": "empty",
                "test_slack_bot.py": "test_slack_bot"
            }
        },
        
        # Configuration
        "config": {
            "settings.yaml": "settings_config",
            "logging.yaml": "logging_yaml",
            "model_config.yaml": "model_config"
        },
        
        # Scripts
        "scripts": {
            "init_database.py": "init_db_script",
            "train_models.py": "train_models_script",
            "deploy.sh": "deploy_script",
            "backup_data.py": "backup_script"
        },
        
        # Database migrations
        "alembic": {
            "versions": {},
            "env.py": "alembic_env",
            "script.py.mako": "alembic_template",
            "alembic.ini": "alembic_config"
        },
        
        # Documentation
        "docs": {
            "README.md": "docs_readme",
            "API.md": "api_docs",
            "DEPLOYMENT.md": "deployment_docs",
            "CONTRIBUTING.md": "contributing_docs",
            "architecture.md": "architecture_docs",
            "user_guide.md": "user_guide"
        },
        
        # Monitoring
        "monitoring": {
            "prometheus": {
                "prometheus.yml": "prometheus_config"
            },
            "grafana": {
                "dashboards": {
                    "business_metrics.json": "grafana_dashboard"
                }
            }
        }
    }
}

print("Repository structure created!")
print("Total files to generate:", sum(1 for path, content in walk_structure(repo_structure) if content != "empty"))

def walk_structure(structure, path=""):
    """Recursively walk through the structure and yield file paths"""
    for name, content in structure.items():
        current_path = f"{path}/{name}" if path else name
        if isinstance(content, dict):
            yield from walk_structure(content, current_path)
        else:
            yield (current_path, content)

# Count files
file_count = 0
for path, content in walk_structure(repo_structure):
    if content != "empty":
        file_count += 1

print(f"Repository structure contains {file_count} files to be generated")