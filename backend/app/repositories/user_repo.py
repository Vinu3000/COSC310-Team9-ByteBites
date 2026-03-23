from sqlalchemy.orm import Session
from app.models.domain import User
from app.core.password_hasher import hash_password

def get_user_by_username(db: Session, username: str):
    """Look up a user by their username. Returns None if not found."""
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: str):
    """Look up a user by their ID. Returns None if not found."""
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, username: str, password: str, role: str = "USER"):
    """Create and persist a new user with a hashed password."""
    new_user = User(
        username=username,
        password_hash=hash_password(password),
        role=role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user