
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from jose import jwt
from ..config import settings

ALGORITHM = "HS256"
router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequestParams(BaseModel):
    username: str
    role: str  # 'admin' or 'user'


def create_auth_token(sub: str, role: str, expires_delta: timedelta, is_refresh: bool = False):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": sub,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)

@router.post("/login")
def login(req: LoginRequestParams):
    if req.role not in {"admin", "user"}:
        raise HTTPException(400, "role must be 'admin' or 'user'")
    access = create_auth_token(req.username, req.role, timedelta(minutes=settings.access_token_expire_minutes))
    return {"access_token": access, "token_type": "bearer"}
