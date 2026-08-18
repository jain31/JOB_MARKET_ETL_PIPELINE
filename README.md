Markdown
#  Remote Job Market ETL Pipeline & Streamlit Dashboard

An end-to-end Data Engineering pipeline that extracts live remote job postings from the [Himalayas API], cleans and standardizes the data using **Pandas**, loads it into a **MySQL** relational database using **SQLAlchemy**, and visualizes market insights via an interactive **Streamlit** dashboard.

---

##  Project Architecture

                              ETL PIPELINE
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐       ┌──────────────────┐
│   Himalayas     │       │     Extract     │       │     Transform   │       │       Load       │
│   Remote API    │ ────> │   extract.py  │ ────> │   clean.py    │ ────> │    load.py     │
└─────────────────┘       └─────────────────┘       └─────────────────┘       └──────────────────┘
│
▼
┌─────────────────┐                                                           ┌──────────────────┐
│  Streamlit App  │ <──────────────────────────────────────────────────────── │     MySQL DB     │
│   (app.py)    │                      SQL Queries                          │   (dim_jobs)   │
└─────────────────┘                                                           └──────────────────┘


---

##  Tech Stack & Tools

- **Language:** Python 3.10+
- **Data Ingestion:** `requests` (REST API with Pagination)
- **Data Processing & Transformation:** `pandas`
- **Database & ORM:** MySQL, `PyMySQL`, `SQLAlchemy`
- **Visualization / Serving Layer:** `streamlit`
- **Environment Management:** `python-dotenv`

---

##  Directory Structure

```text
JOB_MARKET_ETL_PIPELINE/
├── data/
│   └── raw/                # Raw JSON output from API extraction
│       └── raw_jobs.json
├── scripts/
│   ├── __init__.py         # Package initialization
│   ├── extract.py          # API data fetching & pagination
│   ├── clean.py            # Pandas data wrangling & cleaning
│   ├── load.py             # MySQL database loading via SQLAlchemy
│   └── run_pipeline.py     # Pipeline orchestrator / entrypoint
├── .env                    # Environment variables (DB credentials, API URL)
├── .gitignore              # Ignored files (venv, .env, raw data)
├── app.py                  # Streamlit dashboard script
├── README.md               # Project documentation
└── requirements.txt        # Project dependencies