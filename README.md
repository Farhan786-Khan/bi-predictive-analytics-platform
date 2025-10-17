# 1) Clone
git clone https://github.com/Farhan786-Khan/bi-predictive-analytics-platform.git
cd bi-predictive-analytics-platform

# 2) Create & activate virtual env (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Run a sample script / entry point (pick one that exists in your repo)
python src-main.py
bi-predictive-analytics-platform/
├── src/                     # Core Python modules
├── dashboards/              # Dashboard definitions/assets (if any)
├── models/                  # Saved or sample models
├── requirements.txt         # Python dependencies
├── requirements-dev.txt     # Dev-only dependencies (optional)
├── docker-compose.yml       # Optional container orchestration
├── env-example.md           # Environment notes
├── setup.py                 # Packaging stub (if used)
├── LICENSE                  # License file
└── README.md
# Train or run a model
python prophet-model.py

# Run main pipeline
python src-main.py
