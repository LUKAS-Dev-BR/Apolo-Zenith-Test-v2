from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
import aiosqlite
import json
import random

from app.core.database.db import get_db
from app.api.routes.auth import get_current_user

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    reasoning_mode: str = "normal"
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: int
    intent: Optional[str] = None
    media_request: Optional[dict] = None

class ConversationCreate(BaseModel):
    title: str = "Nova Conversa"

class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: str

class ConversationOut(BaseModel):
    id: int
    title: str
    created_at: str
    updated_at: str
    message_count: int = 0

FALLBACK_RESPONSES = [
    "Olá! Sou o Apolo Zenith 1.9, uma inteligência artificial multimodal. Como posso ajudá-lo hoje?",
    "Entendi sua mensagem. Estou processando sua solicitação com capacidades de texto, imagem, vídeo e áudio.",
    "Obrigado pela mensagem! Estou aqui para ajudar com qualquer coisa que precisar.",
    "Processando sua solicitação... Posso ajudar com geração de texto, imagens, vídeos, áudio e muito mais.",
    "Interessante! Deixe-me processar isso. Sou capaz de gerar conteúdo multimodal de última geração.",
]

@router.post("/conversations")
async def create_conversation(req: ConversationCreate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("INSERT INTO conversations (user_id, title) VALUES (?, ?)", (user["id"], req.title))
    await db.commit()
    conv_id = cursor.lastrowid
    return {"id": conv_id, "title": req.title}

@router.get("/conversations")
async def list_conversations(user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("""
        SELECT c.id, c.title, c.created_at, c.updated_at,
               (SELECT COUNT(*) FROM messages WHERE conversation_id = c.id) as message_count
        FROM conversations c WHERE c.user_id = ?
        ORDER BY c.updated_at DESC
    """, (user["id"],))
    rows = await cursor.fetchall()
    return [dict(r) for r in rows]

@router.get("/conversations/{conv_id}")
async def get_conversation(conv_id: int, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM conversations WHERE id = ? AND user_id = ?", (conv_id, user["id"]))
    conv = await cursor.fetchone()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    msg_cursor = await db.execute("SELECT id, role, content, created_at FROM messages WHERE conversation_id = ? ORDER BY created_at", (conv_id,))
    messages = [dict(m) for m in await msg_cursor.fetchall()]
    return {"id": conv["id"], "title": conv["title"], "created_at": conv["created_at"], "messages": messages}

@router.delete("/conversations/{conv_id}")
async def delete_conversation(conv_id: int, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("DELETE FROM conversations WHERE id = ? AND user_id = ?", (conv_id, user["id"]))
    await db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    return {"ok": True}

@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    conv_id = request.conversation_id
    
    if not conv_id:
        title = request.message[:50] + ("..." if len(request.message) > 50 else "")
        cursor = await db.execute("INSERT INTO conversations (user_id, title) VALUES (?, ?)", (user["id"], title))
        await db.commit()
        conv_id = cursor.lastrowid
    
    cursor = await db.execute("SELECT * FROM conversations WHERE id = ? AND user_id = ?", (conv_id, user["id"]))
    if not await cursor.fetchone():
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    await db.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, 'user', ?)", (conv_id, request.message))
    await db.execute("UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (conv_id,))
    await db.commit()
    
    output = random.choice(FALLBACK_RESPONSES)
    
    try:
        from app.core.llm.model import ApoloLLM
        llm = ApoloLLM()
        output = llm.generate(request.message, request.reasoning_mode)
    except Exception:
        pass
    
    await db.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, 'assistant', ?)", (conv_id, output))
    await db.commit()
    
    try:
        parsed = json.loads(output)
        if parsed.get("intent") == "generate_media":
            return ChatResponse(response="Gerando mídia solicitada...", conversation_id=conv_id, intent="generate_media", media_request=parsed)
    except json.JSONDecodeError:
        pass
    
    return ChatResponse(response=output, conversation_id=conv_id)
