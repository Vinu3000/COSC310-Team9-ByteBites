import pytest
from app.main import app
from httpx import AsyncClient
from app.api.dependencies import require_role

# test async functions
pytestmark = pytest.mark.asyncio

# --- Simple Mock Functions ---

@pytest.fixture
def mock_admin():
    async def override_admin():
        return {"id": 1, "role": "ADMIN"}
    # Direct override
    app.dependency_overrides[require_role] = override_admin

@pytest.fixture
def mock_manager():
    async def override_manager():
        return {"id": 2, "role": "MANAGER", "managed_restaurant_id": 1}
    app.dependency_overrides[require_role] = override_manager

# --- Integration Tests ---

async def test_admin_can_delete_item(client: AsyncClient, mock_admin):
    """
    Test 1: Can the Admin delete an item? 
    It should NOT be 401 (Unauthorized).
    """
    # Try to delete menu item number 1
    response = await client.delete("/menu/1")
    
    # Check if it worked (204) or if the item just wasn't there (404)
    assert response.status_code == 204 or response.status_code == 404

async def test_manager_cannot_delete_other_item(client: AsyncClient, mock_manager):
    """
    Test 2: Can a Manager delete an item from ANOTHER restaurant?
    It should be 403 (Forbidden).
    """
    # Manager of Rest 1 tries to delete item 500 (which is in Rest 2)
    response = await client.delete("/menu/500") 
    
    assert response.status_code == 403

async def test_search_works_for_everyone(client: AsyncClient):
    """
    Test 3: Does search work without any login?
    It should be 200 (OK).
    """
    response = await client.get("/menu/search?q=Pasta")
    assert response.status_code == 200
    
    # Should be 200 OK
    assert response.status_code == 200