from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import register, login
from app.api.dependencies import get_current_user
from app.schemas.auth import RegisterRequest, LoginRequest

router = APIRouter(tags=["Authentication"])

@router.post("/register", status_code=201)
def register_user(body: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user account with a unique username and password."""
    return register(db, body.username, body.password)

@router.post("/login")
def login_user(body: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate a user and return a JWT access token."""
    return login(db, body.username, body.password)

@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    """Return the currently authenticated user's profile."""
    return current_user
