# Streamlit Cloud Deployment Guide

To deploy the **Faculty Finder AI** on Streamlit Cloud so your professor can access it via a link:

## 1. Push to GitHub
If you haven't already, push this entire project to a public or private GitHub repository.

```bash
git add .
git commit -m "Final humanized version with AI Recommender"
git push origin main
```

## 2. Connect to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io).
2. Click **"New app"**.
3. Select your repository and the `main` branch.
4. **Main file path**: Set this to `app/main_app.py`.
5. Click **"Deploy!"**.

## 3. Configuration Tips
- **Dependencies**: Streamlit Cloud will automatically install everything listed in your `requirements.txt`.
- **Data Persistence**: Since we are using SQLite, the `database/faculty.db` file must be included in your GitHub repository for the app to show data immediately.
- **URL**: Once deployed, you will get a professional `.streamlit.app` URL that you can share with your professor.

---
**Note**: Ensure that the `models/tfidf_vectorizer.pkl` is also pushed to GitHub, as it is required for the Semantic Search feature.
