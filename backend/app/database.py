from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# SQLite file-based database — simple, no server needed
engine = create_engine(
    "sqlite:///./bytebites.db",
    connect_args={"check_same_thread": False}  # needed for SQLite with FastAPI
)

SessionLocal = sessionmaker(bind=engine)

# Base class that all our models will inherit from
class Base(DeclarativeBase):
    pass

# This gives each request its own DB session, then closes it when done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()