# Clone
git clone https://github.com/Farhan786-Khan/bi-predictive-analytics-platform.git
cd bi-predictive-analytics-platform

# Create & activate virtual env (optional)
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run main pipeline
python src-main.py
bi-predictive-analytics-platform/
├── src/
├── dashboards/
├── models/
├── requirements.txt
├── requirements-dev.txt
├── docker-compose.yml
├── env-example.md
├── setup.py
├── LICENSE
└── README.md
# Train or run a model
python prophet-model.py

# Run main pipeline
python src-main.py
