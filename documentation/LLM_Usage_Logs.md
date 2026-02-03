# Faculty Finder: LLM Usage Logs

This document tracks all technical prompts and LLM support used across both Phase 1 and Phase 2 of the project.

---

## Phase 1: Foundation (Scraping & Storage)

### 1. Handling Complex URL Patterns
**Prompt:**  
> "I am scraping the DA-IICT faculty directory but my code only picks up about 60 links. I noticed there are different categories like adjunct and international faculty that use different URL patterns. Some are relative and some are absolute. How can I fix my extraction logic to catch all 109 profiles and handle these different path types?"

### 2. Managing Site Connection Issues
**Prompt:**  
> "The scraper keeps crashing because the university site sometimes times out. I want to use the tenacity library for automatic retries. How do I wrap my fetch function to try again 3 times with a short delay before it actually fails?"

### 3. Decoding Masked Email Addresses
**Prompt:**  
> "Faculty emails on the site are written like 'name [at] daiict [dot] ac [dot] in'. I need a Python function to turn these back into real email addresses while I clean the data. What is the most reliable way to handle these different strings?"

### 4. SQL Database Schema Design
**Prompt:**  
> "I have my data in a CSV but I want to move it to SQLite for better search performance. Can you help me write a clean SQL schema that includes all my fields and adds indexes on name and email so the search stays fast even with more data?"

### 5. API Response Structure for Pagination
**Prompt:**  
> "In my FastAPI search endpoint, I need to return both the records and the total count so I can build pagination in the frontend later. How should I set up the Pydantic models to handle this combined response?"

### 6. Streamlit Data Export logic
**Prompt:**  
> "I am trying to add a download feature to my Streamlit dashboard. I have a dataframe with the 109 records and I want users to be able to download it as CSV or JSON. What is the correct way to set up the download_button with the right file types?"

### 7. Enabling Local Network Access
**Prompt:**  
> "The app works on my localhost but others on the same Wi-Fi cannot see it. What settings do I need to change in uvicorn and streamlit so it listens on my actual IP address instead of just 127.0.0.1?"

---

## Phase 2: AI & Deployment upgrades

### 8. Recommendation Engine (TF-IDF)
**Objective**: Shift from keyword search to semantic similarity without using heavy transformer models.
**Prompt**:
> "I want to build a faculty recommender for a big data project. We already have 109 profiles in a SQLite DB with name, specialization, and biography. I want to use TF-IDF instead of sentence-transformers because it's lighter and more explainable. Write a Python script `embeddings.py` that generates TF-IDF vectors for combined specialization/biography, saves the fitted vectorizer as a pickle, and stores the vectors in a BLOB column in SQLite."

### 9. Professional UI Redesign
**Objective**: Build a minimalist, dark-themed dashboard that remains stable when profiles are viewed.
**Prompt**:
> "Redesign my Streamlit app for Stage 2. 
> 1. Use a minimalistic dark theme (Obsidian/Slate colors).
> 2. No emojis.
> 3. Use a 3-column grid for faculty profiles.
> 4. Ensure that the 'View Details' button opens a sidebar without squeezing the main grid buttons vertically.
> 5. Use Streamlit callbacks (on_click) for reliable state management.
> 6. Remove all excessive vertical whitespace so we can fit at least 2-3 rows of faculty on one screen."

### 10. Dockerization
**Objective**: Containerize the app for professional submission.
**Prompt**:
> "Create a Dockerfile and docker-compose.yml for this project. The system uses FastAPI and Streamlit. Ensure the PYTHONPATH is handled so 'src' imports work correctly inside the container."
