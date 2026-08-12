from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import aiosqlite

from app.core.database.db import get_db

router = APIRouter()
security = HTTPBearer(auto_error=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "apolo-zenith-1.9-secret-key-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 72

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str

def create_token(user_id: int, username: str):
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    return jwt.encode({"sub": str(user_id), "username": username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Não autenticado")
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        username = payload.get("username")
        return {"id": user_id, "username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT id FROM users WHERE username = ? OR email = ?", (request.username, request.email))
    if await cursor.fetchone():
        raise HTTPException(status_code=400, detail="Usuário ou email já existe")
    
    password_hash = pwd_context.hash(request.password)
    cursor = await db.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (request.username, request.email, password_hash))
    await db.commit()
    user_id = cursor.lastrowid
    
    token = create_token(user_id, request.username)
    return TokenResponse(access_token=token, user_id=user_id, username=request.username)

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (request.username,))
    user = await cursor.fetchone()
    
    if not user or not pwd_context.verify(request.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    token = create_token(user["id"], user["username"])
    return TokenResponse(access_token=token, user_id=user["id"], username=user["username"])

@router.get("/me")
async def get_me(user=Depends(get_current_user)):
    return {"user_id": user["id"], "username": user["username"]}
