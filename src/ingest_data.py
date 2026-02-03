import pandas as pd
import logging
import os
import sys
from src.config import PROCESSED_DATA_DIR, DATABASE_PATH
from src.database import DatabaseManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def ingest_data():
    csv_path = os.path.join(PROCESSED_DATA_DIR, 'faculty_data.csv')
    
    if not os.path.exists(csv_path):
        logger.error(f"Processed data file not found at {csv_path}.")
        return

    df = pd.read_csv(csv_path)
    df['university'] = 'DA-IICT'
    
    if 'raw_source_file' not in df.columns:
        df['raw_source_file'] = 'Unknown'

    records = df.to_dict(orient='records')
    db_manager = DatabaseManager(DATABASE_PATH)
    db_manager.init_db()
    db_manager.clear_table()
    db_manager.insert_faculty_bulk(records)

if __name__ == "__main__":
    ingest_data()
