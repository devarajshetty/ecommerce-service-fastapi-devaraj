from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timezone
from .config import settings

ALGORITHM = "HS256"
security = HTTPBearer()

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        if exp is not None:
            if datetime.now(timezone.utc).timestamp() > float(exp):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

def require_admin_auth(creds: HTTPAuthorizationCredentials = Depends(security)):
    payload = decode_token(creds.credentials)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")

def require_user_auth(creds: HTTPAuthorizationCredentials = Depends(security)) -> str:
    payload = decode_token(creds.credentials)
    if payload.get("role") != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User role required")
    return payload.get("sub")
