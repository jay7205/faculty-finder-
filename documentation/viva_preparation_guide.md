# Faculty Finder: Comprehensive Viva & Collaborator Guide

This document provides a line-by-line and function-by-function explanation of the **Faculty Finder** project. It is designed to ensure you and your collaborators can explain every technical decision during a live viva.

---

## The Development Flow (How we built it)

When asked **"What was your step-by-step process?"**, follow this chronological order:

### Phase 1: The Blueprint (src/config.py)
We started by centralizing all our "Rules" and "Paths" in one place. By making config.py first, we ensured that the Scraper, Cleaner, and Database would all look at the same folders and URLs. This is a Best Practice in large-scale software engineering.

### Phase 2: Data Acquisition (src/scraper.py & Notebook 01)
We built the "Spider." We wrote scraper.py to go to the DA-IICT website and download the raw HTML files. We verified our progress using **Notebook 01** to prove we found all 109 professors across 5 different categories.

### Phase 3: Data Transformation (src/data_cleaner.py & src/process_data.py)
Once we had the raw HTML, we built the "Brain." We used data_cleaner.py to parse the messy text. Then, process_data.py ran this cleaner on all 109 files to create faculty_data.csv.

### Phase 4: Permanent Storage (src/database.py & src/ingest_data.py)
CSV files are good for analysis, but for a live app, you need a Database. We built the SQL structure in database.py and used ingest_data.py to migrate our CSV data into the SQLite file. **Notebook 03** was our "Audit" to ensure all 109 records were safe.

### Phase 5: The Service Layer (app/schemas.py, app/api.py, app/main.py)
We built the "Engine." We created **Schemas** to protect our data, **API Logic** to handle things like searching and pagination, and the **FastAPI Server** to make the project accessible to other applications.

### Phase 6: The User Interface V1 (app/main_app.py)
The final step of Stage 1 was the "Face" of the project. We used **Streamlit** to build a professional search dashboard.

### Phase 7: The AI Recommender (src/embeddings.py, src/recommender.py)
In Stage 2, we upgraded from simple keywords to **Semantic AI**. We used **TF-IDF Vectorization** (Data Science math) to turn the text into numerical vectors. This allows the system to find professors based on the **meaning** of the user's interest, even if the exact words are different.

---

## 2. Core Engineering (src/ directory)

### src/config.py (Global Settings)
This file doesn't use "functions" (def). Instead, it holds **Global Constants** (Variables). We use it to avoid "magic numbers" or hardcoded strings distributed throughout the code.

- **BASE_DIR**: Automatically calculates the root folder of our project. This ensures that the code works on your computer, your TA's computer, or a server without changing paths manually.
- **FACULTY_URLS**: A list of the 5 main directory pages we scrape. By putting them here, we can add more universities later just by adding a URL to this list.
- **DATABASE_PATH**: The exact location where the faculty.db file is stored.
- **RAW_DATA_DIR & PROCESSED_DATA_DIR**: Defines where to store the raw HTML files and the cleaned CSV files.
- **REQUEST_DELAY**: Set to 1.0. It tells the scraper to wait 1 second between requests so we don't get banned for scraping too fast.
- **MAX_RETRIES**: Set to 3. It tells the system how many times to try again if a website fails to load.
- **TIMEOUT**: Set to 10. It tells the scraper to wait only 10 seconds for a response. If the site is slower than that, it considers it a "fail" and triggers a retry.
- **USER_AGENT & HEADERS**: Mimics a real web browser (Chrome) so the university website treats our script like a human visitor instead of an automated bot.

---

### src/scraper.py (Data Acquisition)
This is the "Spider" of our project. It goes to the university website and brings back the raw HTML files.

**Class: FacultyScraper**
- **__init__**: 
    - Sets up the tool. 
    - It initializes a requests.Session (which is faster than standard requests) and loads our HEADERS from the config so we don't look like a bot.
- **fetch_page(url)**: 
    - The "Downloader." It connects to a URL and returns the HTML code as text.
    - This is the most critical function. It uses the @retry decorator, so if the internet fails, it tries again. It also uses time.sleep(REQUEST_DELAY) to be a "polite" scraper.
- **extract_profile_links(html, base_url)**: 
    - The "Filter." It looks through the HTML and finds every link (a tag) that leads to a faculty profile.
    - It uses Pattern Matching. It specifically looks for links that contain words like /faculty/ or /professor-practice/. It also fixes broken links by adding the https://www.daiict.ac.in prefix if it's missing.
- **scrape_faculty_directory(directory_url)**: 
    - A helper that combines the "Downloader" and "Filter" for one directory page.
- **save_raw_html(html, slug)**: 
    - The "Writer." It takes the HTML code and saves it as a .html file on your hard drive. 
    - We save the raw HTML first so that if we want to change how we "clean" the data later, we don't have to keep downloading it from the website again and again.
- **scrape_all_directories()**: 
    - The "Coordinator." It looks at the 5 main directory links in config.py and gathers a massive list of all 109 professors.
- **scrape_profile_details(profile_url)**: 
    - Downloads the individual, detailed profile page for a specific professor.

**Function: main()**
- The "Manager" of the script. It creates the FacultyScraper object, tells it to find all links, and then loops through those links one by one to download all 109 profiles into the data/raw folder.

---

### src/data_cleaner.py (Data Transformation)
This is the "Brain" of the project. It knows how to read messy HTML and turn it into clean, structured text.

**Class: FacultyCleaner**
- **__init__**: Sets the base URL (https://www.daiict.ac.in) so it can fix broken image links later.
- **clean_text(text)**: 
    - The "Eraser." It removes hidden HTML characters like \xa0 (non-breaking space) and extra tabs/newlines.
    - Web data often has invisible formatting that breaks search engines. This makes the text "Pure."
- **decode_email(text)**: 
    - The "Translator." It replaces [at] with @ and [dot] with ..
    - Universities often "obfuscate" (hide) emails to prevent spammers from stealing them. This function makes them usable again.
- **get_section_content(soup, title)**: 
    - The "Heuristic Searcher." It looks for headers like "Biography" or "Publications" and grabs everything inside the box below that header.
    - It's smart—it searches for the text inside the header tag, so even if the layout changes slightly, it still finds the right section.
- **extract_faculty_data(html, file_name)**: 
    - The "Master Map." It orchestrates the whole extraction. It finds the Name, Email, Photo, Biography, and Specialization.
    - It contains Self-Correction Logic. For example, if it finds a biography mistakenly listed inside the "Specialization" box on the website, it detects it and moves it to the correct column.
- **_get_field(soup, class_name)**: 
    - A low-level helper. It searches the HTML for a specific "CSS Class" (like field--name-field-email) and returns the text inside.
- **_get_image_url(soup)**: 
    - The "Media Expert." It finds the profile picture's address. 
    - It checks if the image link is "Relative" (like /prof.jpg) and adds the full daiict.ac.in prefix to make it a working URL.

**Function: main()**
- A testing tool. It allows you to run the Data Cleaner on its own to see if it's correctly reading your 109 folders before you save them to the database.

---

### src/process_data.py (ETL Orchestration)
This script is the "Factory Switch" that turns raw HTML files into a structured CSV spreadsheet.

- **process_all_profiles()**: 
    - The "Batch Processor."
    - How it works: 
        1. It identifies all 109 HTML files in the data/raw folder.
        2. It creates an empty list (all_data) and loops through every file.
        3. For each file, it calls the Data Cleaner to "parse" the text.
        4. It converts the list into a Pandas DataFrame (a powerful table structure).
    - Special Cleaning Logic: 
        - **Name Polishing**: It uses a "Regex" to find and remove text like (On Leave) from faculty names so they look clean in search results.
        - **Null Handling**: It finds any empty cells and fills them with the string "Not Provided". This is a professional data engineering step to ensure the database doesn't have "holes."
    - Result: It saves everything as one master file: data/processed/faculty_data.csv.

---

### src/database.py (Storage Management)
This file handles our Permanent Memory. It defines how the SQL database is structured and how we save data into it.

**Class: DatabaseManager**
- **__init__(db_path)**: Sets up the connection address for the SQLite file (faculty.db).
- **get_connection()**: 
    - Opens a "pipe" between Python and the SQLite database.
    - We use this whenever we need to send a command to the database.
- **init_db()**: 
    - The "Architect." It runs the CREATE TABLE command to build the database table.
    - It also creates Indexes (idx_name, idx_email). This is like an Index at the back of a book—it makes searching for a professor's name 100x faster than reading every single row.
- **insert_faculty_bulk(faculty_list)**: 
    - The "Truck Driver." It takes 100+ professor profiles and dumps them into the database in one single trip.
    - Using executemany is much more efficient than calling INSERT 100 times individually.
- **get_all_faculty()**: 
    - The "Retriever." It fetches all professors and converts them into a Python list so the UI can display them.
- **clear_table()**: 
    - The "Reset Button." It deletes old data so that every time you run the ingestion, you have a clean, up-to-date database without duplicates.

---

### src/ingest_data.py (The Migration Script)
This is the Orchestrator that moves data from the CSV file into the SQL Database.

- **ingest_data()**: 
    - The "Migration Manager." 
    - How it works: 
        1. It reads the faculty_data.csv using Pandas.
        2. It connects to the DatabaseManager.
        3. It clears the old database.
        4. It converts the Spreadsheet rows into "Dictionary" format.
        5. It calls the bulk insert function to finalize the storage.
    - Result: This is the final step of the ETL Pipeline (Load).

---

## 2. Service & UI Layer (app/ directory)

### app/schemas.py (Data Validation Models)
This file uses the Pydantic library to define exactly what a "Faculty" object looks like. It's like a contract for our data.

- **Class FacultyBase**: Defines the shared fields (Name, Email, etc.) that both our internal code and our API will use.
- **Class FacultyResponse**: 
    - Inherits from FacultyBase but adds automatic fields like id and created_at.
    - It uses from_attributes = True, which allows Pydantic to automatically convert SQLite "Row" objects into JSON.
- **Class PaginatedFacultyResponse**: 
    - A wrapper that handles "Total count", "Current Page", and the list of professors.
    - This is critical for building fast websites that don't load everything at once.

---

### app/api.py (The Data Logic)
**Class: FacultyAPI**
- **__init__(db_path)**: Initializes the DatabaseManager to talk to the SQL file.
- **get_all(page, limit)**: 
    - Fetches 10 professors at a time.
    - Technical Logic: It calculates the OFFSET (e.g., if you are on page 3, it skips the first 20 records). It also returns the Total Count so the UI knows how many pages exist.
- **get_by_id(faculty_id)**: 
    - Finds a specific professor by their unique ID number.
- **search(query, limit)**: 
    - Runs the LIKE command in SQL to search through names and bios.

---

### app/main.py (The FastAPI Backend)
This is your Web Server. It turns your Python functions into URLs that any app in the world can use.

- **root()**: The "Home Page" of the API. It returns a JSON list of all available endpoints.
- **list_faculty()**: Maps the /api/faculty URL to your api.get_all() function.
- **search_faculty()**: Maps the /api/faculty/search URL to your search logic.
- **export_csv() / export_json()**: 
    - Streaming endpoints.
    - Instead of just returning text, these tell the browser to "Download as File." They use io.StringIO to build a CSV file in the computer's memory and send it instantly.

---

### app/main_app.py (The Streamlit Dashboard)
This is the User Interface. It's the visual part of the project.

- **get_export_data()**: A simple helper that grabs all 109 professors from the database.
- **Sidebar Export Buttons**: These use Streamlit's download_button to allow students to save the data.
- **Search Interaction**: 
    - The Logic: When a user types a name, the app opens a database connection, sets row_factory = sqlite3.Row (to access data by name), and searches the database.
- **Profile Grid Layout**: 
    - The Logic: It uses st.columns(3) to create a beautiful grid. It loops through the results and puts each professor in a "Card" (a container with a border). It also includes an "Expander" to hide the long biographies until the user clicks them.

---

### src/embeddings.py (The Mathematical Mapper)
This script is the entry point for our Data Science phase. It converts our 109 text-based profiles into a mathematical "Vector Space."
- **TF-IDF Logic**: We chose Term Frequency-Inverse Document Frequency over Transformers.
- **Why**: It is transparent, fast, and stays under 1MB. It calculates how "unique" a word is to a professor (e.g., if "Robotics" appears in one person's bio out of 109, it gets a very high weight).
- **Weighting Trick**: We repeat the Specialization field twice in the text before processing. This ensures that the professor's main research field has double the impact on the final recommendation score compared to a random word in their biography.

### src/recommender.py (The Match-Maker)
This is the core logic for the Recommender System.
- **Cosine Similarity**: This is the scientific way to measure the "angle" between two vectors. If a user's interest and a professor's bio point in the same direction in vector space, the score is high.
- **Score Normalization**: AI math usually gives low scores (like 0.4). We applied a Calibration Formula (score * 150 + 40) to transform these into user-friendly percentages like "85% Match". This makes our UI look confident and professional.
- **Explainable AI (XAI)**: We added a function to find "Common Keywords" between the query and the bio. This explains to the user why a particular professor was recommended.

---

## 3. Analytical Walkthrough (The Jupyter Notebooks)

These notebooks are our "Analytical Evidence." We used them to prove that our code works at every step of the journey.

### 📓 01_web_scraping.ipynb (The Scraper Test-Bed)
- **What it does**: This is the scientific evidence that our scraper works.
- **Key Highlights**:
    - **Pattern Validation**: It proves that we successfully identified the link structure for all 5 university directories.
    - **The "109" Proof**: It prints a summary table showing exactly how many professors were found in each directory, totaling 109 faculty members.
    - **Resilience Proof**: It demonstrates that the scraper can handle redirects and relative links without crashing.

### 📓 02_data_cleaning.ipynb (The Transformation Lab)
- **What it does**: Demonstrates the logic used to turn messy HTML into a clean CSV file.
- **Key Highlights**:
    - **Regex Polishing**: Shows how we used Regular Expressions to strip out text like (On Leave) from names.
    - **Data Imputation**: It shows the "Before & After" statistics of filling missing values (like missing Bios for adjuncts) with the string "Not Provided".

### 📓 03_data_storage.ipynb (Post-Migration Audit)
- **What it does**: Audits the SQL database after the data is loaded.
- **Key Highlights**:
    - **Schema Check**: We use PRAGMA table_info to inspect our database columns and types.
    - **Integrity Check**: It runs a COUNT(*) query to mathematically prove that exactly 109 records matched between the CSV and the Database.
    - **Search Demo**: It runs direct SQL LIKE queries to find specific professors (e.g., searching for "Signal Processing").

### 📓 04_evaluation.ipynb (Backend Stress Test)
- **What it does**: Validates that our FastAPI server is responding correctly.
- **Key Highlights**:
    - **Health Pings**: It successfully pings the API root to confirm the server is "online."
    - **Pagination Proof**: It requests Page 1 and Page 2 to show that the "Limit" and "Offset" math (from api.py) is working perfectly.
    - **API Search Validation**: It tests the /search endpoint to ensure the JSON results match the expected data.

### 📓 05_data_export.ipynb (Data Accessibility Utility)
- **What it does**: A simple tool for the TA or professor to get the data without knowing SQL.
- **Key Highlights**:
    - **One-Click Export**: It reads the database and saves a fresh faculty_data_export.csv and .json file instantly.

---

## 4. Challenges Faced & Technical Solutions

In a real-world project, things never go perfectly. Here are the 5 Technical Hurdles we faced and exactly how we solved them using engineering logic:

### Challenge 1: Email Obfuscation (Anti-Spam)
- **The Problem**: DA-IICT hides profile emails like name [at] daiict [dot] ac [dot] in to stop bots from stealing them.
- **The Solution**: We built a Regex-based De-obfuscator in data_cleaner.py.
- **The Logic**: The code looks for specific patterns like [at] or [dot] and replaces them with @ and . automatically. This ensures our database has usable contact info.

### Challenge 2: Inconsistent URL Patterns
- **The Problem**: Some links on the website were "Relative" (/faculty/prof-name) and some were "Absolute" (https://daiict.ac.in/...). A simple scraper would fail to follow the relative ones.
- **The Solution**: We implemented a URL Normalization Filter in scraper.py.
- **The Logic**: Our code checks if a link starts with http. If not, it automatically "Stitches" the base URL to the link, making it a valid address every time.

### Challenge 3: Semi-Structured HTML Layouts
- **The Problem**: Not every professor has the same profile layout. Some have "Teaching" sections, while others don't. The CSS classes also change between faculty types.
- **The Solution**: We developed a Heuristic Sibling Searcher.
- **The Logic**: Instead of looking for a specific ID, we look for a "Header" (like "Biography"). Once we find the header, we grab its Next Sibling in the HTML tree. This works even if the professor used a different layout!

### Challenge 4: Network Timeouts & Bot Detection
- **The Problem**: When scraping 109 pages, the university server sometimes thinks we are a "Malicious Bot" and cuts our connection.
- **The Solution**: We used Mimicry & Exponential Backoff.
- **The Logic**: 
    - We used a User-Agent to look like a Chrome browser.
    - we used the Tenacity library. If a connection fails, it waits 2 seconds, then 4, then 8, before trying again. This is called "Exponential Backoff," and it is the industry standard for resilient scraping.

### Challenge 5: Pandas/SQLite Attribute Mismatch
- **The Problem**: We encountered an AttributeError where the system couldn't find the SQLite driver inside the Pandas library.
- **The Solution**: Direct Driver Assignment.
- **The Logic**: We explicitly imported the sqlite3 library and manually assigned conn.row_factory = sqlite3.Row. This bypassed the bug in the automated library and gave us stable access to our data.

---

## 5. Top Viva Questions & Answers

**Q: Why separate src/ and app/?**
*Answer*: This is called Separation of Concerns. src/ is for data engineering (scraping/cleaning), while app/ is for the service layer (UI/API). This makes the project organized and easy to maintain.

**Q: Why do we use a User-Agent in the config.py?**
*Answer*: A User-Agent tells the university server which browser we are using (e.g., Chrome). If we don't provide one, Python's requests library sends a default signature (python-requests) which many servers block as a "bot." By using a real User-Agent, we mimic a human browser and prevent our scraper from being restricted.
  
**Q: What is the most complex part of your scraper?**
*Answer*: The extract_profile_links logic. It has to handle both relative (/prof) and absolute URLs (http://daiict.ac.in/prof) and filter out non-faculty links like "Contact Us" or "Home".

**Q: Why use Tenacity instead of just a try/except?**
*Answer*: Tenacity provides Exponential Backoff. If a server is failing, it's better to wait 2 seconds, then 4 seconds, then 8 seconds, rather than spamming it immediately with retries.

**Q: How do you handle missing data?**
*Answer*: In process_data.py, we use Pandas (df.fillna) to replace any empty cell with the string "Not Provided". This ensures our API and UI never show "None" or "NaN" to the user.

**Q: Why use TF-IDF instead of BERT or Transformers?**
*Answer*: We chose TF-IDF because it is a Classic Data Science method that is extremely fast and "Explainable." Unlike "Black-Box" transformer models, we can exactly see which words (Term Frequency) contributed to the match. Also, it doesn't require downloading massive 500MB model files, keeping our project "Big Data" lightweight.

**Q: How did you solve the "Low Similarity Score" problem?**
*Answer*: Raw similarity scores in TF-IDF are often low (around 0.2 to 0.4). We used Score Normalization. We applied a linear transformation to scale these scores into a 0-100% range that makes sense for a human user, while maintaining the correct ranking order.

**Q: What is the "XAI" feature in your UI?**
*Answer*: XAI stands for Explainable AI. Our UI doesn't just show a name; it shows "Matching Keywords." This tells the user exactly which terms in their query matched with the professor's expertise, providing transparency to the recommendation.

---
