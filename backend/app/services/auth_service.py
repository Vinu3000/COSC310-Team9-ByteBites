import jwt
import os
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.user_repo import find_by_username, create_user
from app.core.password_hasher import verify_password

SECRET_KEY = os.getenv("SECRET_KEY", "bytebites-dev-secret")

def register(db: Session, username: str, password: str):
    # Check if username is already taken
    if find_by_username(db, username):
        raise HTTPException(status_code=400, detail="Username already taken")
    
    user = create_user(db, username, password)
    return {"id": user.id, "username": user.username, "role": user.role}

def login(db: Session, username: str, password: str):
    # Find the user and check their password
    user = find_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Create a JWT token that expires in 1 hour
    token = jwt.encode(
        {
            "sub": user.id,        # who the token belongs to
            "role": user.role,     # their role for RBAC
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    return {"access_token": token, "token_type": "bearer"}