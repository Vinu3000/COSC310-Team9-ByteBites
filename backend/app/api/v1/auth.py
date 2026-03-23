from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database import get_db
from app.services.auth_service import login, register

router = APIRouter(prefix="/auth", tags=["Authentication"])


class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/register", status_code=201)
def register_user(body: RegisterRequest, db: Session = Depends(get_db)):
    return register(db, body.username, body.password)


@router.post("/login")
def login_user(body: LoginRequest, db: Session = Depends(get_db)):
    return login(db, body.username, body.password)


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return current_user