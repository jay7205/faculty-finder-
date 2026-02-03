# Faculty Finder AI: Phase 2 Recommender System

### Reconstruction Guide for Evaluators
This repository represents the full reconstruction of the DA-IICT Faculty Information System, upgraded into an AI-Powered Recommendation Engine.

---

### Project Statistics
| Metric | Intelligence Detail |
| :--- | :--- |
| **Total Dataset** | 109 Comprehensive Faculty Profiles |
| **Extraction Speed** | ~1.2s per profile (Controlled for network politeness) |
| **Data Integrity** | 100% Normalized (Zero Nulls; Handled via Heuristic Imputation) |
| **Avg Bio Depth** | 81.0 Words per profile |
| **Avg Specialization** | 12.1 Words per profile |

#### Source Contribution Breakdown
| Directory Category | Count | Contribution % |
| :--- | :--- | :--- |
| **Main Faculty** | 61 | 55.9% |
| **Adjunct Faculty** | 28 | 25.7% |
| **Professor of Practice** | 9 | 8.3% |
| **Adjunct (International)** | 6 | 5.5% |
| **Distinguished Professor** | 5 | 4.6% |

---

## Phase 2: AI & Data Science
We have transitioned from simple keyword search to a Semantic Recommender.

### The Recommender Engine (src/recommender.py)
- **Technology**: TF-IDF (Term Frequency-Inverse Document Frequency) + Cosine Similarity.
- **Why TF-IDF?**: It provides a balance of high-performance matching and extreme transparency (Explainable AI), which is ideal for academic project evaluation.
- **Weighted Specialization**: The system gives 2x semantic weight to the "specialization" field compared to the "biography" to ensure research-match accuracy.
- **Score Normalization**: Raw cosine scores are calibrated into user-friendly percentage matches (e.g., "92% Match").

### Premium UI Dashboard (app/main_app.py)
- **Aesthetic**: Modern, minimalist dark mode (Obsidian/Slate theme).
- **Responsive Grid**: High-density 3-column layout showing 12-15 profiles per screen.
- **Contextual Discovery**: Dynamic sidebar for full biographies, linked directly to university source pages.

---

## Running with Docker (Recommended)
The easiest way for a professor to run this project is using Docker.

1. **Start Services**:
    ```bash
    docker compose up --build
    ```
2. **Access App**: Open [http://localhost:8501](http://localhost:8501)
3. **Access API**: Open [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Manual Setup & Reconstruction
If running locally without Docker, follow this sequence:

### 1. Rebuild the Memory (Database)
1. **Scrape**: `python src/scraper.py` (Captures 109 raw HTML profiles).
2. **ETL**: `python src/process_data.py` (Cleans, de-obfuscates emails, creates CSV).
3. **Ingest**: `python src/ingest_data.py` (Migrates to SQLite with B-Tree indexes).
4. **Embed**: `python src/embeddings.py` (Phase 2 Step: Generates AI vectors).

### 2. Launch
- **Backend**: `uvicorn app.main:app`
- **Frontend**: `streamlit run app/main_app.py`

---

## Technical Challenges & Solutions

### 1. Advanced Email De-obfuscation
- **Challenge**: The target website uses anti-spam obfuscation for emails.
- **Solution**: Implemented a regex-based normalization engine that automatically decodes these patterns.

### 2. Recursive Scraping & URL Normalization
- **Challenge**: Navigating through 5 different directories with a mix of relative and absolute links.
- **Solution**: Built a URL Pattern Matcher that enforces absolute pathing and uses slugification for consistent filenames.

### 3. Heuristic Data Extraction
- **Challenge**: Irregular HTML structure where sections are not tied to consistent IDs.
- **Solution**: Developed a Sibling Traversal Heuristic. The system identifies header text anchors and extracts the subsequent sibling nodes.

---

## Tech Stack Summary
- **AI/ML**: Scikit-Learn (TF-IDF), NumPy (Cosine Similarity), Pickle (Vector Storage).
- **Web Scraping**: Requests, BeautifulSoup4, LXML.
- **Core Engineering**: Pandas, SQLite3 (Relational Storage).
- **Microservices**: FastAPI, Uvicorn (REST Backend).
- **UX/UI**: Streamlit (Reactive Dashboard).
- **Stats**: 109 Records | 12 AI-searchable fields | 100% Reconstruction accuracy.

---

## Submission Components
- `documentation/LLM_Usage_Logs.md`: Unified log of all AI prompts and support.
- `documentation/viva_preparation_guide.md`: Comprehensive guide for project defense.
- `documentation/streamlit_cloud.md`: Live deployment link and cloud settings.
- `documentation/deployment_fixes.md`: Technical troubleshooting for Docker.
