import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.routes import chat, media, auth, agents
from app.core.infrastructure.queue_manager import QueueManager
from app.core.infrastructure.kv_store import KVStore
from app.core.database.db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="Apolo Zenith 1.9",
    description="IA Multimodal Unificada",
    version="1.9.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

queue_manager = QueueManager()
kv_store = KVStore()

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(media.router, prefix="/api/media", tags=["media"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])

@app.get("/")
async def root():
    return {
        "message": "Apolo Zenith 1.9 API",
        "version": "1.9.0",
        "context_window": "100 quindecillion tokens (10^48)",
        "capabilities": [
            "LLM Causal 199B",
            "Text-to-Image",
            "Text-to-Video",
            "Text-to-Audio",
            "Text-to-Music",
            "Coding Agent",
            "3D Modeling Agent",
            "6 Reasoning Modes"
        ]
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.9.0"}

@app.get("/api/capabilities")
async def capabilities():
    return {
        "llm": {
            "parameters": "199B",
            "context_window": "100 quindecillion tokens (10^48)",
            "reasoning_modes": ["normal", "medium", "high", "very_high", "ultra_high", "ultra_mega_high"]
        },
        "multimodal": {
            "image": True,
            "video": True,
            "audio": True,
            "music": True
        },
        "agents": {
            "coding": {
                "frontend_senior": True,
                "backend_senior": True,
                "programming_languages": 9000,
                "designer_professional": True
            },
            "modeling_3d": True
        }
    }
