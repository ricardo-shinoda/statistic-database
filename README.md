# Statistic Database Pipeline

An automated data ingestion pipeline designed to extract personal financial data from multiple sources (Google Drive spreadsheets and raw credit card invoices), apply transformations, and load the structured data into a local PostgreSQL instance.

## Architecture & Data Flow

[ Google Drive: Excel Sheets ] ───► [ Python Ingestion Scripts ] ───► [ Local PostgreSQL ]
[ Local /invoices Directory  ] ───►       (Pandas / ETL)         ───►   (DDL/DML Schema)


1. **Automated Data Ingestion:**
   * Fetches financial data (Pix transactions, income stream entries, and investment logs) from specialized Excel spreadsheets hosted on Google Drive using `credentials.json`.
   * Scans local data directories for raw credit card invoice documents (PDFs/CSVs).
2. **Transformation:** Python ETL components clean, structure, and convert raw inputs into a unified transactional schema using Pandas.
3. **Loading:** Data is incrementally appended or synced into a containerized PostgreSQL target database.

---

## Repository Structure

Based on the project organization seen in your workspace:

```text
statistic-database/
├── database/                   # Database schema management and queries
│   ├── ddl/                    # Data Definition Language scripts
│   │   └── create_manual_items_table.sql
│   ├── dml/                    # Data Manipulation Language scripts
│   │   └── insert_market_data.sql
│   └── queries/                # Analytical and transactional SQL scripts
│       └── transactions_queries.sql
├── data_samples/               # Mock data for portfolio evaluation and testing
│   ├── drive_mock_sample.xlsx  # Dummy spreadsheet simulating Google Drive input
│   └── invoice_mock_sample.csv # Dummy credit card statement structure
├── src/script/                 # Core Python ETL pipeline components
│   ├── append_ingest_expenses.py   # Incremental ingestion pipeline for expenses
│   ├── delete_ingest_expenses.py   # Idempotent cleanup and rerun utilities
│   ├── send_email.py               # Notification and alerting utility
│   └── sync_merchant_expenses.py   # Google Drive and invoice synchronization script
├── .env.example                # Template for environment variables (Safe for Git)
├── credentials.json            # Google Drive API service account credentials (Ignored)
├── docker-compose.yml          # Local PostgreSQL database container configuration
├── requirements.txt            # Python dependencies (Pandas, SQLAlchemy, psycopg2, etc.)
└── Postgres local.session.sql  # Database client session configuration
```

Core Engineering Principles

    Idempotency: The pipeline utilizes delete_ingest_expenses.py to wipe specific transactional windows before re-running ingestion tasks. This ensures that duplicate execution does not cause primary key conflicts, data drift, or row duplication.

    Decoupled Architecture: Schema definition and database migration state (SQL) are fully decoupled from the pipeline transformation and orchestration logic (Python).

    Secure Environment Design: Production credentials and API access tokens are entirely isolated via environment variables (.env) and explicitly blocked from version control using strict .gitignore rules.

Environment Setup
1. Prerequisites

Ensure you have Docker, Docker Compose, and Python 3.11+ installed on your host system.
2. Infrastructure Setup

Spin up the local PostgreSQL container instance:

```Bash
docker compose up -d
``` 
3. Python Environment & Dependencies

Initialize the virtual environment and install dependencies:

```Bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
``` 

4. Configuration

This is where things get tricky, I will think of an example data, so you will be able to test this script without needing me to share sensitive personal data.