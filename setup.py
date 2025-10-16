"""
Setup script for Business Intelligence Platform
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
def read_requirements(filename):
    """Read requirements from file and return as list."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines() 
                if line.strip() and not line.startswith('#')]

# Version
__version__ = "1.0.0"

setup(
    name="bi-predictive-analytics-platform",
    version=__version__,
    author="Your Name",
    author_email="your.email@example.com",
    description="End-to-End Business Intelligence Dashboard with Predictive & Prescriptive Analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bi-predictive-analytics-platform",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/bi-predictive-analytics-platform/issues",
        "Documentation": "https://github.com/yourusername/bi-predictive-analytics-platform/docs",
        "Source Code": "https://github.com/yourusername/bi-predictive-analytics-platform",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: FastAPI",
        "Framework :: Dash",
    ],
    python_requires=">=3.11",
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": read_requirements("requirements-dev.txt"),
        "testing": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "factory-boy>=3.3.0",
            "httpx>=0.25.2",
        ],
        "docs": [
            "mkdocs>=1.5.3",
            "mkdocs-material>=9.5.2",
            "mkdocs-mermaid2-plugin>=1.1.1",
        ],
        "ml": [
            "tensorflow>=2.15.0",
            "torch>=2.1.2",
            "transformers>=4.36.2",
            "spacy>=3.7.2",
        ],
        "cloud": [
            "boto3>=1.34.0",
            "azure-storage-blob>=12.19.0",
            "google-cloud-storage>=2.10.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "bi-platform=src.main:main",
            "bi-dashboard=src.dashboard.app:main",
            "bi-train=scripts.train_models:main",
            "bi-migrate=scripts.migrate:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.json", "*.sql", "*.md"],
        "src": ["config/*", "alembic/*"],
    },
    zip_safe=False,
    keywords=[
        "business intelligence",
        "predictive analytics", 
        "prescriptive analytics",
        "machine learning",
        "dashboard",
        "fastapi",
        "plotly",
        "time series",
        "anomaly detection",
        "forecasting",
        "data science",
        "artificial intelligence"
    ],
)