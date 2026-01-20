# Faculty Finder - DA-IICT Data Pipeline

**Industry-level, modular web scraping and data engineering project for faculty directory management.**

## 📋 Project Overview

This is Phase 1 of the Faculty Finder project, focused on building a robust data engineering pipeline to extract, clean, store, and serve faculty information from the DA-IICT website.

## ✅ Current Status

**Phase 4 Complete - Data Transformation**
- ✓ Successfully scraped **109 faculty profiles**
- ✓ **Cleaned & Standardized** data in `data/processed/faculty_data.csv`
- ✓ **100% Data Completeness**: All missing values explicitly handled ("Not Provided")
- ✓ Robust extraction logic for all directory types

## 🏗️ Project Structure

```
faculty_finder/
├── data/
│   ├── raw/              # 109 faculty HTML files
│   └── processed/        # faculty_data.csv (Cleaned Dataset)
├── notebooks/
│   ├── 01_web_scraping.ipynb
│   └── 02_data_cleaning.ipynb
├── src/
│   ├── config.py         # Configuration and URLs
│   ├── scraper.py        # Web scraping module
│   ├── data_cleaner.py   # Data cleaning & Extraction module
│   ├── process_data.py   # ETL pipeline script
│   └── __init__.py
├── app/                  # (Next: FastAPI application)
├── database/             # (Next: SQLite storage)
├── requirements.txt
└── .gitignore
```

## 🚀 Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Data Pipeline
```bash
# 1. Scrape Data
python src/scraper.py

# 2. Clean & Process Data
python src/process_data.py
```

## 📦 Tech Stack

- **requests** - HTTP library for web requests
- **BeautifulSoup4** - HTML parsing and data extraction
- **lxml** - Fast XML/HTML parser
- **tenacity** - Retry logic with exponential backoff
- **Pandas** - Data manipulation and CSV export
- **FastAPI** *(upcoming)* - REST API framework
- **SQLite** *(upcoming)* - Database for structured storage

## 📊 Data Summary

- **Total Records Processed**: 109
- **Format**: Structured CSV (`data/processed/faculty_data.csv`)
- **Fields**: Name, Image URL, Education, Email, Biography, Specialization, Teaching, Publications, Raw Source File.
- **Data Quality**: 0 Null Values (standardized to "Not Provided").

## 🔜 Next Steps

1. **Database Storage**: Design schema and store in SQLite (Phase 5)
2. **FastAPI Service**: Create REST endpoints for data access (Phase 6)
3. **Documentation**: Add API docs (Phase 8)

## 📁 Files Generated

- **109 HTML files** in `data/raw/`
- **1 Cleaned CSV** in `data/processed/faculty_data.csv`

## 🛠️ Module Usage

```python
from src.data_cleaner import FacultyCleaner

cleaner = FacultyCleaner()
data = cleaner.extract_faculty_data(html_content, "filename.html")
print(data['biography'])
```

## ⚙️ Configuration

All settings in `src/config.py`:
- Faculty directory URLs
- Request delays (1 second - polite scraping)
- Retry limits (3 attempts)
- Data paths

---

- **Current Status**: Phase 4 Complete - Data Ready for Ingestion
- **Last Updated**: 2026-01-18
- **Next Step**: Phase 5 (Data Storage in SQLite)
