import jwt
import os
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.user_repo import get_user_by_username, create_user
from app.core.password_hasher import verify_password

SECRET_KEY = os.getenv("SECRET_KEY", "bytebites-dev-secret")
TOKEN_EXPIRE_HOURS = 1  # extracted as constant for easy configuration

def register(db: Session, username: str, password: str):
    """Register a new user, raises 400 if username already exists."""
    if get_user_by_username(db, username):
        raise HTTPException(status_code=400, detail="Username already taken")
    user = create_user(db, username, password)
    return {"id": user.id, "username": user.username, "role": user.role}

def login(db: Session, username: str, password: str):
    """Authenticate user credentials and return a JWT token."""
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = jwt.encode(
        {
            "sub": user.id,
            "role": user.role,
            "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRE_HOURS)
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    return {"access_token": token, "token_type": "bearer"}