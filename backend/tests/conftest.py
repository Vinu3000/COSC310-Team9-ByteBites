import pytest
import asyncio
# ASGITransport is like a bridge between the test and our FastAPI app
from httpx import AsyncClient, ASGITransport 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app 
from app.database import Base, get_db 
from app.models.menu import MenuItem
from app.models.restaurant import Restaurant

# Use a simple SQLite memory database for testing
TEST_DB_URL = "sqlite://"

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def db():
    """
    Create a new database for every single test.

    """
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Give the database session to the test
    db_session = TestingSessionLocal()
    yield db_session
    
    # Close and clean everything after the test is done
    db_session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
async def client(db):
    """
    Create a fake 'browser' (client) to call our API.
    """
    # Don't use the real DB, use the test DB
    def mock_get_db():
        yield db

    # Put our fake DB into the app
    app.dependency_overrides[get_db] = mock_get_db
    
    # Open the connection to the app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    
    # Clean up the fake DB setting
    app.dependency_overrides.clear()