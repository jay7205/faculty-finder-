import logging
import pickle
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from src.database import DatabaseManager
from src.config import DATABASE_PATH, BASE_DIR, VECTORIZER_PATH

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FacultyRecommender:
    def __init__(self):
        self.db = DatabaseManager(DATABASE_PATH)
        if not os.path.exists(VECTORIZER_PATH):
            raise FileNotFoundError(f"TF-IDF vectorizer not found at {VECTORIZER_PATH}. Run src/embeddings.py first.")
        
        with open(VECTORIZER_PATH, 'rb') as f:
            self.vectorizer = pickle.load(f)
            
        logger.info("TF-IDF Recommender initialized.")

    def get_keywords(self, query: str, faculty_bio: str) -> list:
        query_words = set(query.lower().split())
        bio_words = set(faculty_bio.lower().replace('.', ' ').replace(',', ' ').split())
        
        from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
        common = query_words.intersection(bio_words)
        keywords = [word for word in common if word not in ENGLISH_STOP_WORDS and len(word) > 2]
        return list(keywords)[:5]

    def recommend(self, query: str, top_n: int = 10):
        query_vector = self.vectorizer.transform([query])
        
        all_faculty = self.db.get_all_faculty()
        results = []
        
        for faculty in all_faculty:
            if faculty.get('embedding'):
                faculty_vector = pickle.loads(faculty['embedding'])
                
                similarity = cosine_similarity(query_vector, faculty_vector)[0][0]
                
                if similarity > 0:
                    display_score = min(round(similarity * 150 + 40, 1), 99.0) if similarity > 0.05 else round(similarity * 200, 1)
                    
                    keywords = self.get_keywords(query, f"{faculty['specialization']} {faculty['biography']}")
                    
                    faculty_data = faculty.copy()
                    faculty_data['match_score'] = display_score
                    faculty_data['matching_keywords'] = keywords
                    faculty_data.pop('embedding', None)
                    results.append(faculty_data)
        
        results.sort(key=lambda x: x['match_score'], reverse=True)
        return results[:top_n]

if __name__ == "__main__":
    recommender = FacultyRecommender()
    test_query = "Machine Learning and Neural Networks"
    matches = recommender.recommend(test_query, top_n=3)
    
    print(f"\nResults for query: '{test_query}'")
    for m in matches:
        print(f"- {m['name']} | Match Score: {m['match_score']}% | Keywords: {m['matching_keywords']}")
