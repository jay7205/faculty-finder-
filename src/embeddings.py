import logging
import pickle
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from src.database import DatabaseManager
from src.config import DATABASE_PATH, BASE_DIR, VECTORIZER_PATH

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TFIDFEmbeddingGenerator:
    def __init__(self):
        self.db = DatabaseManager(DATABASE_PATH)
        self.vectorizer = TfidfVectorizer(
            stop_words='english', 
            ngram_range=(1, 2),
            max_features=5000
        )

    def prepare_text(self, faculty: dict) -> str:
        spec = str(faculty.get('specialization', ''))
        bio = str(faculty.get('biography', ''))
        
        if spec == 'Not Provided': spec = ''
        if bio == 'Not Provided': bio = ''
        
        combined_text = f"{spec} {spec} {bio}"
        return combined_text.strip()

    def generate_and_store_all(self):
        logger.info("Fetching all faculty records for TF-IDF training...")
        faculty_list = self.db.get_all_faculty()
        
        if not faculty_list:
            logger.warning("No data found to process.")
            return

        corpus = [self.prepare_text(f) for f in faculty_list]
        
        logger.info("Fitting TF-IDF Vectorizer and transforming corpus...")
        tfidf_matrix = self.vectorizer.fit_transform(corpus)
        
        with open(VECTORIZER_PATH, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        logger.info(f"Fitted vectorizer saved to {VECTORIZER_PATH}")

        logger.info(f"Storing {len(faculty_list)} TF-IDF vectors in the database...")
        for i, faculty in enumerate(faculty_list):
            vector_blob = pickle.dumps(tfidf_matrix[i])
            self.db.update_faculty_embedding(faculty['id'], vector_blob)
            
        logger.info("TF-IDF processing and storage complete.")

if __name__ == "__main__":
    generator = TFIDFEmbeddingGenerator()
    generator.generate_and_store_all()
