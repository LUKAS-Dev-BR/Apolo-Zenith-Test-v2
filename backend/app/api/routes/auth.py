from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import secrets
import hashlib
import time

router = APIRouter()

API_KEYS_DB = {}

class APIKeyCreate(BaseModel):
    name: str

class APIKeyResponse(BaseModel):
    key: str
    name: str
    created_at: float

@router.post("/keys", response_model=APIKeyResponse)
async def create_api_key(request: APIKeyCreate):
    key = f"az-{secrets.token_hex(24)}"
    key_hash = hashlib.sha256(key.encode()).hexdigest()
    
    API_KEYS_DB[key_hash] = {
        "name": request.name,
        "created_at": time.time(),
        "key_prefix": key[:12]
    }
    
    return APIKeyResponse(
        key=key,
        name=request.name,
        created_at=time.time()
    )

@router.get("/keys")
async def list_api_keys():
    keys = []
    for key_hash, data in API_KEYS_DB.items():
        keys.append({
            "key_prefix": data["key_prefix"],
            "name": data["name"],
            "created_at": data["created_at"]
        })
    return keys

@router.delete("/keys/{key_hash}")
async def delete_api_key(key_hash: str):
    if key_hash in API_KEYS_DB:
        del API_KEYS_DB[key_hash]
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Key not found")
