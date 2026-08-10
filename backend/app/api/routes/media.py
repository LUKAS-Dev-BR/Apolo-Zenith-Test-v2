from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class MediaRequest(BaseModel):
    media_type: str
    prompt: str
    parameters: Optional[dict] = None

@router.post("/generate")
async def generate_media(request: MediaRequest):
    from app.core.infrastructure.queue_manager import QueueManager
    
    queue = QueueManager()
    job_id = queue.enqueue(request.dict())
    
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
