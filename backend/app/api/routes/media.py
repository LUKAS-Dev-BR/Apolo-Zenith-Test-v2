from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import aiosqlite

from app.core.database.db import get_db
from app.api.routes.auth import get_current_user

router = APIRouter()

class MediaRequest(BaseModel):
    media_type: str
    prompt: str
    parameters: Optional[dict] = None
    conversation_id: Optional[int] = None

@router.post("/generate")
async def generate_media(request: MediaRequest, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    from app.core.infrastructure.queue_manager import QueueManager
    
    queue = QueueManager()
    job_id = queue.enqueue(request.dict())
    
    await db.execute(
        "INSERT INTO media (user_id, conversation_id, media_type, prompt, file_path) VALUES (?, ?, ?, ?, ?)",
        (user["id"], request.conversation_id, request.media_type, request.prompt, f"/media/pending/{job_id}")
    )
    await db.commit()
    
    return {"job_id": job_id, "status": "queued"}

@router.get("/status/{job_id}")
async def get_status(job_id: str):
    from app.core.infrastructure.queue_manager import QueueManager
    
    queue = QueueManager()
    status = queue.get_status(job_id)
    
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return status

@router.get("/progress/{job_id}")
async def get_progress(job_id: str):
    from app.core.infrastructure.kv_store import KVStore
    
    kv = KVStore()
    progress = kv.get(f"progress:{job_id}")
    
    return {"job_id": job_id, "progress": progress or 0}

@router.get("/gallery")
async def get_gallery(user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute(
        "SELECT id, media_type, prompt, file_path, created_at FROM media WHERE user_id = ? ORDER BY created_at DESC",
        (user["id"],)
    )
    return [dict(r) for r in await cursor.fetchall()]
