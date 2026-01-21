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
        logger.error(f"Processed data file not found at {csv_path}. Please run process_data.py first.")
        return

    logger.info(f"Reading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    df['university'] = 'DA-IICT'
    
    if 'raw_source_file' not in df.columns:
        logger.warning("raw_source_file column missing in CSV. Filling with 'Unknown'.")
        df['raw_source_file'] = 'Unknown'

    records = df.to_dict(orient='records')
    logger.info(f"Prepared {len(records)} records for insertion.")
    
    db_manager = DatabaseManager(DATABASE_PATH)
    
    logger.info("Initializing database...")
    db_manager.init_db()
    
    logger.info("Clearing old data (to avoid duplicates during re-runs)...")
    db_manager.clear_table()
    
    logger.info("Inserting records...")
    inserted_count = db_manager.insert_faculty_bulk(records)
    
    logger.info(f"Migration Complete. Total Faculty in DB: {inserted_count}")

if __name__ == "__main__":
    ingest_data()
