import pytest
from app.main import app
from httpx import AsyncClient
from app.api.dependencies import require_role

# Tell pytest to handle async functions
pytestmark = pytest.mark.asyncio

# --- Simple Mock Functions ---

@pytest.fixture
def mock_admin():
    async def override_admin():
        # Fake an Admin user
        return {"id": 1, "role": "ADMIN"}
    app.dependency_overrides[require_role] = override_admin
    yield # Let the test run
    app.dependency_overrides = {} # Clean up after test

@pytest.fixture
def mock_manager():
    async def override_manager():
        # Fake a Manager for Restaurant 1
        return {"id": 2, "role": "MANAGER", "managed_restaurant_id": 1}
    app.dependency_overrides[require_role] = override_manager
    yield # Let the test run
    app.dependency_overrides = {} # Clean up after test

# --- Integration Tests ---

async def test_admin_can_delete_item(client: AsyncClient, mock_admin):

    response = await client.delete("/api/v1/menu/1")
    
    # 204 means deleted, 404 means it wasn't there
    assert response.status_code in [204, 404]

async def test_manager_cannot_delete_other_item(client: AsyncClient, mock_manager):
    """
    Test 2: Manager of Rest 1 tries to delete item from Rest 2.
    Should be 403 Forbidden.
    """
    response = await client.delete("/api/v1/menu/500") 
    
    # We expect 403 because item 500 is in another restaurant
    assert response.status_code == 403

async def test_search_works_for_everyone(client: AsyncClient):
    """
    Test 3: Does search work without login?
    Path moved from /menu/browse to /restaurants/
    """
    response = await client.get("/api/v1/restaurants/?q=pizza")
    
    # Everyone can search, so it should be 200 OK
    assert response.status_code == 200