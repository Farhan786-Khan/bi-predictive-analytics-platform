# Business Intelligence Platform - .gitignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# poetry
poetry.lock

# pdm
.pdm.toml

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
.idea/

# VS Code
.vscode/
*.code-workspace

# Sublime Text
*.sublime-project
*.sublime-workspace

# Vim
*.swp
*.swo
*~

# Emacs
*~
\#*\#
/.emacs.desktop
/.emacs.desktop.lock
*.elc
auto-save-list
tramp
.\#*

# MacOS
.DS_Store
.AppleDouble
.LSOverride
Icon?
._*
.DocumentRevisions-V100
.fseventsd
.Spotlight-V100
.TemporaryItems
.Trashes
.VolumeIcon.icns
.com.apple.timemachine.donotpresent
.AppleDB
.AppleDesktop
Network Trash Folder
Temporary Items
.apdisk

# Windows
Thumbs.db
Thumbs.db:encryptable
ehthumbs.db
ehthumbs_vista.db
*.tmp
*.temp
Desktop.ini
$RECYCLE.BIN/
*.cab
*.msi
*.msix
*.msm
*.msp
*.lnk

# Linux
*~
.fuse_hidden*
.directory
.Trash-*
.nfs*

# Docker
docker-compose.override.yml
.dockerignore

# Database
*.db
*.sqlite
*.sqlite3
data/
backups/

# Logs
*.log
logs/
log/

# Configuration files with secrets
config/secrets.yaml
.env.local
.env.production
.env.staging

# API Keys and Secrets
api_keys/
secrets/
credentials/
keys/
*.pem
*.key
*.crt
*.p12

# ML Models and Data
models/
*.pkl
*.joblib
*.h5
*.pb
*.ckpt
*.model
*.bin
artifacts/
mlruns/
wandb/
outputs/

# Data files
data/raw/
data/processed/
data/external/
*.csv
*.json
*.parquet
*.xlsx
*.xls
*.h5
*.hdf5

# Temporary files
tmp/
temp/
.tmp/
*.tmp

# Cache directories
.cache/
cache/
.sass-cache/

# Node.js (if using frontend tools)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
.node_repl_history
.yarn-integrity

# Monitoring and metrics
prometheus_data/
grafana_data/
metrics/

# Airflow
airflow.cfg
webserver_config.py
logs/

# Redis dump
dump.rdb

# Jupyter
.jupyter/

# Profile data
*.prof
profile.stats

# Benchmark results
benchmark.json
.benchmarks/

# Security scan results
bandit-report.json
safety-report.json
security-scan-results/

# Performance data
*.pyc
.coverage
coverage.xml
.pytest_cache/

# Documentation build
docs/build/
docs/site/

# IDE specific
*.swp
*.swo
.idea/
.vscode/
*.sublime-project
*.sublime-workspace

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Backup files
*.bak
*.backup
*.old
*.orig

# Archive files
*.zip
*.tar.gz
*.rar
*.7z

# Local development
local/
dev/
playground/

# Certificates and SSL
*.crt
*.key
*.pem
ssl/

# Kubernetes
*.kubeconfig

# Terraform
*.tfstate
*.tfstate.*
.terraform/
terraform.tfvars

# Cloud provider configs
.aws/
.gcp/
.azure/

# Local configuration overrides
local_config.yaml
local_settings.py
override.yaml