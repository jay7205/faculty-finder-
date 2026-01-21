# Faculty Finder

**Industry-level, modular web scraping and data engineering project for faculty directory management.**

## Project Status

**Current State: Phase 5 Complete (Data Storage)**
- Successfully extracted data for 109 faculty profiles.
- Cleaned and standardized all records.
- Implemented SQLite database for structured storage.

## Project Structure

```
faculty_finder/
 data/
    raw/              # Raw HTML profiles
    processed/        # Cleaned CSV data
 database/
    faculty.db        # SQLite database
 notebooks/
    01_web_scraping.ipynb
    02_data_cleaning.ipynb
    03_data_storage.ipynb
 src/
    config.py         # Global settings
    scraper.py        # Web scraping logic
    data_cleaner.py   # HTML parsing and extraction
    process_data.py   # ETL pipeline script
    database.py       # Database management
    ingest_data.py    # Data migration script
    __init__.py
 app/                  # FastAPI application (pending)
 requirements.txt
 .gitignore
```

## Data Access

This project provides multiple ways for collaborators to access the faculty data:

### 1. Interactive UI (Recommended)
Launch the Streamlit dashboard to search, view profiles, and download exports:
```bash
streamlit run app/main_app.py
```
- **Downloads**: Use the sidebar to export the entire database as **CSV** or **JSON**.

### 2. Direct File Access
- **SQLite Database**: Found at `database/faculty.db`. Use any SQLite viewer to query.
- **CSV Format**: A processed version is available at `data/processed/faculty_data.csv`.

### 3. Programmatic Access (API)
The project includes a FastAPI backend for programmatic integration:
```bash
uvicorn app/main:app --reload
```
- **Endpoints**: `/api/faculty`, `/api/faculty/search`, `/api/faculty/{id}`.

## Tech Stack
- **Database**: SQLite
- **API**: FastAPI
- **UI**: Streamlit
- **Scraping**: BeautifulSoup4, Requests

## Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Pipeline
```bash
# 1. Scrape raw data
python src/scraper.py

# 2. Process and clean data
python src/process_data.py

# 3. Load data into database
python src/ingest_data.py
```

## Tech Stack

- **Requests**: HTTP library for fetching web pages.
- **BeautifulSoup4**: HTML parsing and data extraction.
- **LXML**: Fast processing for structured documents.
- **Tenacity**: Retry logic for network resilience.
- **Pandas**: Data transformation and cleaning.
- **SQLite**: Local relational database.
- **FastAPI**: REST API framework (next phase).

## Data Summary

- **Total Records**: 109
- **Storage**: SQLite + CSV
- **Fields**: Name, Image URL, Education, Email, Biography, Specialization, Teaching, Publications, Raw Source File, University.
- **Quality**: No missing values; standardized to "Not Provided".

## Next Steps

1. Implement FastAPI REST endpoints for data access.
2. Add full-text search capabilities across faculty bios and specializations.
3. Finalize documentation for API usage.

## Files Generated

- Raw HTML files in `data/raw/`
- Processed CSV in `data/processed/`
- SQLite database in `database//`

## Module Usage

```python
from src.database import DatabaseManager

db = DatabaseManager()
faculty_list = db.get_all_faculty()

for faculty in faculty_list:
    print(faculty['name'], faculty['specialization'])
```

## Configuration

Settings are managed in `src/config.py`:
- Target URLs for scraping.
- Request delays and retry limits.
- File system paths for data storage.
- Database configuration.

---

**Last Updated**: 2026-01-21
**Current Phase**: Phase 6 - API Development (Next)
