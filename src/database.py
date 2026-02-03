import sqlite3
import logging
from typing import List, Dict, Any, Optional
from src.config import DATABASE_PATH

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS faculty (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                image_url TEXT,
                education TEXT,
                contact_no TEXT,
                address TEXT,
                email TEXT,
                biography TEXT,
                specialization TEXT,
                teaching TEXT,
                publications TEXT,
                raw_source_file TEXT,
                university TEXT DEFAULT 'DA-IICT',
                embedding BLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_name ON faculty(name);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON faculty(email);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_university ON faculty(university);")
        
        conn.commit()
        conn.close()
        logger.info(f"Database initialized at {self.db_path}")

    def insert_faculty_bulk(self, faculty_list: List[Dict[str, Any]]) -> int:
        if not faculty_list:
            return 0
            
        conn = self.get_connection()
        cursor = conn.cursor()
        
        insert_query = """
            INSERT INTO faculty (
                name, image_url, education, contact_no, address, email, 
                biography, specialization, teaching, publications, 
                raw_source_file, university
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        data_to_insert = []
        for f in faculty_list:
            data_to_insert.append((
                f.get('name'),
                f.get('image_url'),
                f.get('education'),
                f.get('contact_no'),
                f.get('address'),
                f.get('email'),
                f.get('biography'),
                f.get('specialization'),
                f.get('teaching'),
                f.get('publications'),
                f.get('raw_source_file'),
                f.get('university', 'DA-IICT')
            ))
            
        try:
            cursor.executemany(insert_query, data_to_insert)
            conn.commit()
            count = cursor.rowcount
            logger.info(f"Successfully inserted {count} records.")
            return count
        except sqlite3.Error as e:
            logger.error(f"Database error during bulk insert: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_all_faculty(self) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM faculty")
        rows = cursor.fetchall()
        
        conn.close()
        return [dict(row) for row in rows]

    def clear_table(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM faculty")
        conn.commit()
        conn.close()

    def update_faculty_embedding(self, faculty_id: int, embedding_blob: bytes):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE faculty SET embedding = ? WHERE id = ?", (embedding_blob, faculty_id))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error updating embedding for ID {faculty_id}: {e}")
            conn.rollback()
        finally:
            conn.close()

    def get_faculty_by_id(self, faculty_id: int) -> Optional[Dict[str, Any]]:
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM faculty WHERE id = ?", (faculty_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
