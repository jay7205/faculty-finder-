import sqlite3
import os
from typing import List, Optional, Tuple
from src.database import DatabaseManager
from src.config import DATABASE_PATH

class FacultyAPI:
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db = DatabaseManager(db_path)

    def get_all(self, page: int = 1, limit: int = 10) -> Tuple[int, List[dict]]:
        offset = (page - 1) * limit
        conn = self.db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM faculty")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT * FROM faculty LIMIT ? OFFSET ?", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        
        return total, [dict(row) for row in rows]

    def get_by_id(self, faculty_id: int) -> Optional[dict]:
        conn = self.db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM faculty WHERE id = ?", (faculty_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def search(self, query: str, limit: int = 20) -> List[dict]:
        conn = self.db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        search_term = f"%{query}%"
        cursor.execute("""
            SELECT * FROM faculty 
            WHERE name LIKE ? 
            OR specialization LIKE ? 
            OR biography LIKE ?
            LIMIT ?
        """, (search_term, search_term, search_term, limit))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
