# Faculty Finder

**Industry-level, modular web scraping and data engineering project for faculty directory management.**

## Project Status

**Current State: Phase 7 Complete (Interactive Search UI)**
- Successfully extracted and processed 109 faculty profiles from DA-IICT.
- Implemented a complete ETL pipeline from raw HTML to SQL storage.
- Developed a high-performance REST API (FastAPI) for programmatic access.
- Launched a human-friendly search dashboard (Streamlit) for data exploration and export.

## Project Structure

```
faculty_finder/
 app/                  # FastAPI & Streamlit application layer
    main.py            # API entry point
    api.py             # API data access logic
    schemas.py         # Pydantic models
    main_app.py        # Streamlit search dashboard
 data/
    raw/               # Raw HTML source files (109 profiles)
    processed/         # Cleaned CSV dataset
 database/
    faculty.db         # SQLite source of truth
 notebooks/
    01_web_scraping.ipynb
    02_data_cleaning.ipynb
    03_data_storage.ipynb
    04_evaluation.ipynb # API & Search testing
 src/
    config.py          # Global settings & constants
    scraper.py         # Resilient web scraping logic
    data_cleaner.py    # HTML parsing and extraction
    process_data.py    # Batch ETL pipeline
    database.py        # Database management layer
    ingest_data.py     # SQL migration script
 README.md             # Project documentation (Submission)
 requirements.txt      # Dependency manifest
```

## Data Accessibility

This project is built for collaboration. Data can be accessed in three ways:

### 1. Interactive Dashboard (User-Facing)
The most convenient way to explore and export data.
```bash
streamlit run app/main_app.py
```
- **Search**: Instance search across names, biographies, and specializations.
- **Exports**: Download the entire dataset in **CSV** or **JSON** format via the sidebar.

### 2. Programmatic Access (Developer-Facing)
A fully-featured REST API for external application integration.
```bash
uvicorn app.main:app --reload
```
- **Documentation**: Automatically generated at `http://127.0.0.1:8000/docs`.
- **Endpoints**: `/api/faculty`, `/api/faculty/search`, `/api/faculty/{id}`.

### 3. Direct Access (Researcher-Facing)
- **Database**: Access `database/faculty.db` directly using any SQLite client.
- **Static Files**: Cleaned data is also available in `data/processed/faculty_data.csv`.

## Core Implementation Details

### Data Pipeline (Phases 1-5)
1. **Scraping**: Used `BeautifulSoup4` with custom retry logic and polite request headers to download 109 profiles across 5 different university directory structures.
2. **Cleaning**: Standardized messy HTML into structured data. Handled email de-obfuscation and consolidated empty fields to "Not Provided".
3. **Storage**: Designed a relational schema in SQLite with secondary indexes on `name` and `email` for sub-millisecond query performance.

### Service Layer (Phases 6-7)
- **API**: Built with FastAPI to serve async requests. Implemented pagination and full-text search logic.
- **UI**: Developed with Streamlit to bridge the gap between technical data storage and human-readable exploration.

## Tech Stack

- **Data Acquisition**: Requests, BeautifulSoup4, LXML, Tenacity.
- **Data Engineering**: Pandas, SQLite3.
- **Backend Services**: FastAPI, Pydantic, Uvicorn.
- **Frontend/UX**: Streamlit.

## Final Statistics
- **Records**: 109 profiles.
- **Data Quality**: 100% standardized (zero nulls).
- **Searchable Text**: Names, Education, Bios, Specializations.

---

**Last Updated**: 2026-01-21  
**Project Status**: Production Ready | Version 1.0.0
