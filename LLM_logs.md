# Faculty Finder: LLM Logs

This document tracks technical challenges where LLM support was used to solve specific implementation blockers during the project.

---

## 1. Handling Complex URL Patterns
**Prompt:**  
"I am scraping the DA-IICT faculty directory but my code only picks up about 60 links. I noticed there are different categories like adjunct and international faculty that use different URL patterns. Some are relative and some are absolute. How can I fix my extraction logic to catch all 109 profiles and handle these different path types?"

---

## 2. Managing Site Connection Issues
**Prompt:**  
"The scraper keeps crashing because the university site sometimes times out. I want to use the tenacity library for automatic retries. How do I wrap my fetch function to try again 3 times with a short delay before it actually fails?"

---

## 3. Decoding Masked Email Addresses
**Prompt:**  
"Faculty emails on the site are written like 'name [at] daiict [dot] ac [dot] in'. I need a Python function to turn these back into real email addresses while I clean the data. What is the most reliable way to handle these different strings?"

---

## 4. SQL Database Schema Design
**Prompt:**  
"I have my data in a CSV but I want to move it to SQLite for better search performance. Can you help me write a clean SQL schema that includes all my fields and adds indexes on name and email so the search stays fast even with more data?"

---

## 5. API Response Structure for Pagination
**Prompt:**  
"In my FastAPI search endpoint, I need to return both the records and the total count so I can build pagination in the frontend later. How should I set up the Pydantic models to handle this combined response?"

---

## 6. Streamlit Data Export logic
**Prompt:**  
"I am trying to add a download feature to my Streamlit dashboard. I have a dataframe with the 109 records and I want users to be able to download it as CSV or JSON. What is the correct way to set up the download_button with the right file types?"

---

## 7. Enabling Local Network Access
**Prompt:**  
"The app works on my localhost but others on the same Wi-Fi cannot see it. What settings do I need to change in uvicorn and streamlit so it listens on my actual IP address instead of just 127.0.0.1?"

---

## 8. Final Code Refinement
**Prompt:**  
"The project is done but I want the code to look very clean and professional for submission. Help me remove all the unnecessary debug notes and comments so it looks like a finished production product. Also, make sure the documentation is formal."
