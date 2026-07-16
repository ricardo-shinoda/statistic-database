# Financial Data Ingestion & ETL Pipeline

An automated, end-to-end data pipeline designed to ingest, process, and centralize personal financial transactions and stock market data. This project eliminates manual data entry by programmatically fetching raw credit card statements (ZIP files) and Excel ledger files directly from Google Drive, processing them, and loading the structured data into a local PostgreSQL database container.

## 🚀 Key Features

* **Zero-Touch Ingestion:** Automates Google Drive integration to download and parse zipped credit card statements and ledger spreadsheets.
* **Asset Tracking:** Fetches real-time or historical stock market price data to evaluate portfolio performance.
* **Dockerized Database:** Spins up a local PostgreSQL instance seamlessly via Docker Compose.
* **Data Activation:** Built-in alerting system to send automated email updates/reports with pipeline statistics.
* **Local Analytics:** Ready-to-use analytical SQL queries and Python-based visualization/dashboard modules.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Database:** PostgreSQL (running on Docker)
* **Infrastructure:** Docker & Docker Compose
* **APIs & Integrations:** Google Drive API (via Service Account), Financial APIs (for stock price ingestion)
* **Libraries:** Pandas (data processing), SQLAlchemy / Psycopg (database connection)

## 📁 Repository Structure

```text
STATISTIC/
├── configs/                     # API credentials and service accounts
│   ├── credentials.json
│   └── service.account.json
├── database/                    # SQL scripts for database initialization
│   ├── ddl/                     # Table schemas and DDL scripts
│   ├── dml/                     # Data seeding scripts
│   └── queries/                 # Analytical queries (dividends, expenses, portfolio)
├── src/                         
│   ├── script/                  
│   │   ├── dashboard/           # Scripts for local reporting and visualization
│   │   ├── data_activation/     # Notification engines (e.g., email alerts)
│   │   └── pipelines_elt/       # Core Python ingestion and processing scripts
│   └── utils.py                 # Shared helper functions
├── docker-compose.yml           # PostgreSQL container orchestrator
├── requirements.txt             # Python dependencies
└── .env                         # Local environment variables configuration