from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import json

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    reasoning_mode: str = "normal"
    context: Optional[list] = None

class ChatResponse(BaseModel):
    response: str
    intent: Optional[str] = None
    media_request: Optional[dict] = None

@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    from app.core.llm.model import ApoloLLM
    
    llm = ApoloLLM()
    output = llm.generate(request.message, request.reasoning_mode)
    
    try:
        parsed = json.loads(output)
        if parsed.get("intent") == "generate_media":
            return ChatResponse(
                response="Gerando mídia solicitada...",
                intent="generate_media",
                media_request=parsed
            )
    except json.JSONDecodeError:
        pass
    
    return ChatResponse(response=output)

@router.get("/health")
async def chat_health():
    return {"status": "healthy"}
