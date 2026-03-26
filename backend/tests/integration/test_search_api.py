import pytest
from httpx import AsyncClient
from app.main import app
from app.api.dependencies import require_role

# 1. Mock a user so we don't need a real login token
@pytest.fixture
def mock_user_session():
    """
    This replaces the security check with a fake admin user.
    """
    async def override_require_role():
        return {"id": 1, "role": "ADMIN", "username": "test_user"}
    
    app.dependency_overrides[require_role] = override_require_role
    yield
    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_search_restaurants_by_name(client: AsyncClient, mock_user_session):
    """
    Feat3-FR1: Search using keywords.
    Updated URL to /api/v1/restaurants/
    """
    response = await client.get("/api/v1/restaurants/?q=Restaurant")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "items" in data
    assert isinstance(data["items"], list)

@pytest.mark.asyncio
async def test_filter_restaurants_by_category(client: AsyncClient, mock_user_session):
    """
    Feat3-US1: Filter by category.
    Updated URL to /api/v1/restaurants/
    """
    response = await client.get("/api/v1/restaurants/?category=Italian")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check if filters work correctly
    for restaurant in data["items"]:
        assert restaurant["category"] == "Italian"

@pytest.mark.asyncio
async def test_pagination_metadata(client: AsyncClient, mock_user_session):
    """
    Feat3-FR2: Pagination check.
    Updated URL to /api/v1/restaurants/
    """
    response = await client.get("/api/v1/restaurants/?page=1&size=2")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["page"] == 1
    assert data["size"] == 2
    assert "total" in data
    assert "pages" in data
    assert len(data["items"]) <= 2