from sqlalchemy.orm import Session
from app.models.domain import User
from app.core.password_hasher import hash_password

def find_by_username(db: Session, username: str):
    # Look up a user by username in the database
    return db.query(User).filter(User.username == username).first()

def find_by_id(db: Session, user_id: str):
    # Look up a user by their ID
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, username: str, password: str, role: str = "USER"):
    # Create a new user and save to the database
    new_user = User(
        username=username,
        password_hash=hash_password(password),
        role=role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user