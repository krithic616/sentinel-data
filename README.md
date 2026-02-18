Sentinel-Data — Automated Data Quality & Anomaly Detection Engine

Overview:

Sentinel-Data is a production-ready data observability pipeline that monitors pricing data for deterministic
validation failures and probabilistic anomalies. It integrates statistical detection, structured logging,
formatted Telegram alerting, and GitHub Actions automation to simulate an enterprise-grade data
monitoring system.


Architecture Flow:

Data Generation → Validation → ML Detection → Alerting → CI/CD Automation


The pipeline performs: 

Historical baseline creation
Daily snapshot generation
Deterministic validation checks
Isolation Forest anomaly detection
Baseline deviation percentage calculation
Structured JSON logging
Telegram tabular alert formatting
GitHub Actions automation


Key Features:

Deterministic data validation layer
Unsupervised anomaly detection (Isolation Forest) 
Deviation percentage computation vs historical baseline 
Top-N anomaly summarization 
Dynamically aligned tabular Telegram alerts 
Structured JSON logging system 
Production vs Test mode toggle via environment variables 
GitHub Actions CI/CD automation 
Secure secrets management


Example Telegram Alert:

11 pricing anomalies detected at 2026-02-17 04:08:19 UTC.
Top deviations: Product P0022 (Shoes) deviated 3.50% from baseline. Product P0187 (Electronics) deviated
2.94% from baseline. Product P0291 (Shoes) deviated -1.77% from baseline.
Time: 2026-02-17 04:08:19 UTC
product_id | category | price | deviation_percent
P0022 | Shoes | 4063 | +3.50% P0187 | Electronics | 3167 | +2.94% P0291 | Shoes | 3476 | -1.77%


Tech Stack:
 
Python 3.11 
Pandas / NumPy 
Scikit-Learn 
Great Expectations 
Telegram Bot API 
GitHub Actions 
Structured Logging


Local Setup:

Clone Repository
git clone https://github.com/your-username/sentinel-data.git cd sentinel-data
Create Virtual Environment
python -m venv venv venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt
Create .env File
TELEGRAM_TOKEN=your_bot_token TELEGRAM_CHAT_ID=your_chat_id PRODUCTION_MODE=true
Run Pipeline
python -m src.main


GitHub Actions Automation:

Workflow file location:
.github/workflows/sentinel_pipeline.yml
Required Repository Secrets: - TELEGRAM_TOKEN- TELEGRAM_CHAT_ID- PRODUCTION_MODE 
To trigger manually: GitHub → Actions → Sentinel Data Pipeline → Run workflow



Production Behavior:

When PRODUCTION_MODE=true: - No synthetic anomalies injected- Only statistical outliers detected- Alerts are reproducible 
When PRODUCTION_MODE=false: - Controlled synthetic anomalies injected for testing



What This Project Demonstrates:

End-to-end data pipeline design 
Data observability engineering 
Statistical anomaly detection 
Structured production logging 
Secure CI/CD implementation 
Automated alerting system

