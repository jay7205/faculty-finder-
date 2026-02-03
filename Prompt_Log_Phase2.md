# Phase 2: AI Recommender - LLM Prompt Log

As per the LLM Usage Policy, all prompts used to generate the Phase 2 components (Semantic Engine and Premium UI) are documented here.

## Recommendation Engine (TF-IDF)
**Objective**: Shift from keyword search to semantic similarity without using heavy transformer models.
**Prompt**:
> "I want to build a faculty recommender for a big data project. We already have 109 profiles in a SQLite DB with name, specialization, and biography. I want to use TF-IDF instead of sentence-transformers because it's lighter and more explainable. Write a Python script `embeddings.py` that generates TF-IDF vectors for combined specialization/biography, saves the fitted vectorizer as a pickle, and stores the vectors in a BLOB column in SQLite."

## Professional UI Redesign
**Objective**: Build a minimalist, dark-themed dashboard that remains stable when profiles are viewed.
**Prompt**:
> "Redesign my Streamlit app for Stage 2. 
> 1. Use a minimalistic dark theme (Obsidian/Slate colors).
> 2. No emojis.
> 3. Use a 3-column grid for faculty profiles.
> 4. Ensure that the 'View Details' button opens a sidebar without squeezing the main grid buttons vertically.
> 5. Use Streamlit callbacks (on_click) for reliable state management.
> 6. Remove all excessive vertical whitespace so we can fit at least 2-3 rows of faculty on one screen."

## Dockerization
**Objective**: Containerize the app for professional submission.
**Prompt**:
> "Create a Dockerfile and docker-compose.yml for this project. The system uses FastAPI and Streamlit. Ensure the PYTHONPATH is handled so 'src' imports work correctly inside the container."
