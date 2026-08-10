import sqlite3
import json
import time
import uuid
from typing import Dict, Optional
from pathlib import Path
from app.config import settings

class QueueManager:
    def __init__(self):
        self.db_path = settings.DATABASE_DIR / "queue.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        
    def _init_db(self):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                status TEXT DEFAULT 'pending',
                media_type TEXT,
                prompt TEXT,
                parameters TEXT,
                result_path TEXT,
                progress REAL DEFAULT 0,
                created_at REAL,
                updated_at REAL,
                error TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def enqueue(self, job_data: Dict) -> str:
        job_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO jobs (job_id, media_type, prompt, parameters, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            job_id,
            job_data.get('media_type'),
            job_data.get('prompt'),
            json.dumps(job_data.get('parameters', {})),
            time.time(),
            time.time()
        ))
        
        conn.commit()
        conn.close()
        
        return job_id
    
    def get_status(self, job_id: str) -> Optional[Dict]:
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM jobs WHERE job_id = ?', (job_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return {
                'job_id': row[0],
                'status': row[1],
                'media_type': row[2],
                'prompt': row[3],
                'parameters': json.loads(row[4]) if row[4] else {},
                'result_path': row[5],
                'progress': row[6],
                'created_at': row[7],
                'updated_at': row[8],
                'error': row[9]
            }
        
        return None
    
    def update_status(self, job_id: str, status: str, progress: float = None, result_path: str = None, error: str = None):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        updates = ['updated_at = ?']
        values = [time.time()]
        
        if status:
            updates.append('status = ?')
            values.append(status)
        
        if progress is not None:
            updates.append('progress = ?')
            values.append(progress)
        
        if result_path:
            updates.append('result_path = ?')
            values.append(result_path)
        
        if error:
            updates.append('error = ?')
            values.append(error)
        
        values.append(job_id)
        
        cursor.execute(f'UPDATE jobs SET {", ".join(updates)} WHERE job_id = ?', values)
        
        conn.commit()
        conn.close()
    
    def get_pending_jobs(self, limit: int = 10) -> list:
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM jobs WHERE status = ? ORDER BY created_at ASC LIMIT ?', ('pending', limit))
        rows = cursor.fetchall()
        
        conn.close()
        
        return [
            {
                'job_id': row[0],
                'status': row[1],
                'media_type': row[2],
                'prompt': row[3],
                'parameters': json.loads(row[4]) if row[4] else {},
                'result_path': row[5],
                'progress': row[6],
                'created_at': row[7],
                'updated_at': row[8],
                'error': row[9]
            }
            for row in rows
        ]
    
    def delete_job(self, job_id: str):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM jobs WHERE job_id = ?', (job_id,))
        
        conn.commit()
        conn.close()
