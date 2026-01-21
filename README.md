# Faculty Finder: End-to-End Data Engineering & Search System

A professional-grade, modular system designed to scrape, clean, store, and serve faculty directory data. This project demonstrates a full-stack data engineering lifecycle—from raw web acquisition to an interactive search interface.

## Project Overview

**Faculty Finder** automates the ingestion of academic profiles. It handles the complexities of scraping multi-pattern university directories, standardizing irregular HTML data, and providing high-performance access via both a REST API and a visual dashboard.

### Key Milestones
- **Acquisition**: Successfully scraped **109 faculty profiles** from 5 recursive university directory structures.
- **Data Engineering**: Built a robust ETL pipeline ensuring 100% data standardization (zero null values).
- **Storage**: Implemented a relational SQLite database with secondary indexing for optimal query speeds.
- **Accessibility**: Developed a triple-entry access system: REST API, Interactive UI, and a dedicated Export Utility.

---

## Project Architecture & Structure

The project follows a modular "Service-Oriented" directory structure to ensure maintainability and scalability.

```
faculty_finder/
├── app/                  # Service & UI Layer
│   ├── main.py           # FastAPI server entry point
│   ├── api.py            # Core logic for database-to-API mapping
│   ├── schemas.py        # Pydantic models for data validation
│   └── main_app.py       # Streamlit interactive search dashboard
├── data/                 # Data Persistence
│   ├── raw/              # 109 individual HTML profile source files
│   └── processed/        # Standardized CSV dataset (export-ready)
├── database/             # Relational Storage
│   └── faculty.db        # SQLite master database
├── notebooks/            # Verification & Evaluation
│   ├── 01_web_scraping.ipynb   # Scraper test & validation
│   ├── 02_data_cleaning.ipynb   # ETL logic verification
│   ├── 03_data_storage.ipynb    # SQL schema & count audit
│   ├── 04_evaluation.ipynb      # API endpoint stress testing
│   └── 05_data_export.ipynb     # [NEW] One-click data export utility
├── src/                  # Core Engineering Modules
│   ├── config.py         # Global constants (URLs, paths, retry logic)
│   ├── scraper.py        # Resilient scraper with Tenacity retry support
│   ├── data_cleaner.py   # Advanced HTML parsing & email de-obfuscation
│   ├── process_data.py   # Batch processing & ETL orchestration
│   ├── database.py       # SQL management & bulk insertion logic
│   └── ingest_data.py    # Seamless migration from CSV to SQLite
└── README.md             # Final Submission Documentation
```

---

## Technical Implementation Deep-Dive

### 1. Resilient Data Acquisition
University websites often use irregular URL patterns. Our scraper leverages:
- **Recursive Pattern Matching**: Handles profiles stored under `/faculty/`, `/adjunct/`, and other distinct paths.
- **Resilience**: Uses the `Tenacity` library to handle intermittent network failures with exponential backoff.
- **Polite Scraping**: Implements custom Chromium headers and request delays to mimic human browsing behavior.

### 2. The ETL Pipeline
Converting raw HTML into a search engine requires significant cleaning:
- **Email De-obfuscation**: University emails are often masked (e.g., `[at]` vs `@`). The system automatically decodes these patterns during processing.
- **Missing Value Strategy**: Instead of leaving NULLs, every missing field is standardized to "Not Provided" to ensure consistent UI rendering.
- **Biographical Repair**: Heuristic logic detects if a "Specialization" field actually contains a full biography and corrects the mapping automatically.

### 3. High-Performance Search
The system uses the SQLite **LIKE** operator combined with B-Tree indexes on `name` and `email` to provide sub-millisecond search results across 109 biographies and specializations.

---

## How to Access the Data

This project is built for various stakeholders, from researchers to software developers.

### A. The Search Dashboard (For Everyone)
The Streamlit UI provides a visual way to explore the directory.
```bash
# To run the UI
streamlit run app/main_app.py
```
- **Local URL**: `http://localhost:8501`
- **Network URL**: `http://10.200.24.147:8501`
- **Exports**: Use the sidebar buttons to download the entire 109-record dataset in **CSV** or **JSON** format instantly.

### B. The REST API (For Developers)
For those integrating this data into other apps.
```bash
# To start the API server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- **Direct Download (CSV)**: `http://10.200.24.147:8000/api/faculty/export/csv`
- **Direct Download (JSON)**: `http://10.200.24.147:8000/api/faculty/export/json`

### C. The Export Utility (For Data Analysts)
If you prefer Jupyter, we have provided a "one-click" export script.
- **File**: `notebooks/05_data_export.ipynb`
- **Result**: Running this notebook will generate `faculty_data_export.csv` and `.json` in the local directory.

---

## Tech Stack & Statistics

- **Backend**: Python 3.x, FastAPI, Pydantic, Uvicorn.
- **Data**: Pandas, SQLite3, BeautifulSoup4, LXML.
- **UI**: Streamlit.
- **Stats**: 109 Records | 10 Searchable Fields | 100% Data Completion.

---

**Last Updated**: 2026-01-21  
**Author Status**: Phase 7 Complete | Production Ready  
**Final Submission Version**: 1.0.0
