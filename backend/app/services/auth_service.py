from fastapi import HTTPException
from sqlalchemy.orm import Session
import jwt

from app.config import SECRET_KEY
from app.core.password_hasher import verify_password
from app.repositories.user_repo import find_by_username, create_user


def register(db: Session, username: str, password: str):
    existing_user = find_by_username(db, username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    user = create_user(db, username, password)
    return {"message": "User created", "user_id": user.id}


def login(db: Session, username: str, password: str):
    user = find_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"user_id": user.id}, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}