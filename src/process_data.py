import os
import pandas as pd
import logging
import numpy as np
from src.data_cleaner import FacultyCleaner
from src.config import RAW_DATA_DIR, PROCESSED_DATA_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_all_profiles():
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    cleaner = FacultyCleaner()
    all_data = []
    
    files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith('.html')]
    
    for file_name in files:
        file_path = os.path.join(RAW_DATA_DIR, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
            data = cleaner.extract_faculty_data(html, file_name)
            all_data.append(data)
            
    df = pd.DataFrame(all_data)
    df['name'] = df['name'].str.replace(r'\s*\(On Leave\)', '', regex=True)
    df = df.replace(r'^\s*$', np.nan, regex=True)
    df = df.fillna("Not Provided")
    
    output_path = os.path.join(PROCESSED_DATA_DIR, 'faculty_data.csv')
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    process_all_profiles()
