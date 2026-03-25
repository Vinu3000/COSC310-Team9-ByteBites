import pytest
from httpx import AsyncClient
from app.main import app
from app.api.dependencies import require_role

# Test: Keyword Search (FR1), Pagination (FR2), and Category Filtering (US1).

# 1. Mock a user so we don't need a real login token
@pytest.fixture
def mock_user_session():
    """
    This 'fixture' replaces the real security guard with a fake one.
    It tells the app: 'This user is logged in as an ADMIN'.
    """
    async def override_require_role():
        # Return a fake user dictionary
        return {"id": 1, "role": "ADMIN", "username": "test_user"}
    
    # Apply the override to our FastAPI app
    app.dependency_overrides[require_role] = override_require_role
    yield
    # Clean up after the test is done
    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_search_restaurants_by_name(client: AsyncClient, mock_user_session):
    """
    Feat3-FR1: The system shall allow users to search using keywords.
    try to search for 'Restaurant' and see if we get results.
    """
    # Send a GET request with a query parameter 'q'
    response = await client.get("/api/v1/menu/browse?q=Restaurant")
    
    # Expect a 200 OK status
    assert response.status_code == 200
    data = response.json()
    
    # The 'items' list should not be empty if data was ingested
    assert "items" in data
    assert isinstance(data["items"], list)

@pytest.mark.asyncio
async def test_filter_restaurants_by_category(client: AsyncClient, mock_user_session):
    """
    Feat3-US1: As a user, I want to filter restaurants by category.
    We check if filtering for 'Italian' works.
    """
    # Request only Italian food
    response = await client.get("/api/v1/menu/browse?category=Italian")
    
    assert response.status_code == 200
    data = response.json()
    
    # Every restaurant returned should belong to the 'Italian' category
    for restaurant in data["items"]:
        assert restaurant["category"] == "Italian"

@pytest.mark.asyncio
async def test_pagination_metadata(client: AsyncClient, mock_user_session):
    """
    Feat3-FR2: The system shall return paginated results.
    We check if 'total', 'page', and 'size' are in the response.
    """
    # Ask for page 1 with only 2 items
    response = await client.get("/api/v1/menu/browse?page=1&size=2")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check if the pagination fields exist and are correct
    assert data["page"] == 1
    assert data["size"] == 2
    assert "total" in data
    assert "pages" in data
    
    # The list of items should not have more than 2 restaurants
    assert len(data["items"]) <= 2