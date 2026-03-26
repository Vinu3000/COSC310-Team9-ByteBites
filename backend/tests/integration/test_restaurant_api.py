import pytest
from httpx import AsyncClient
from uuid import uuid4

@pytest.mark.asyncio
async def test_get_restaurants_pagination(client: AsyncClient):
    """
    Feat3-FR2: The system shall return paginated results.
    We must use the new /api/v1 prefix.
    """
    response = await client.get("/api/v1/restaurants/?page=1&size=10")
    
    # 2. Check if the status is 200 OK
    assert response.status_code == 200
    
    data = response.json()
    
    # 3. Verify pagination fields (must match PaginatedRestaurants schema)
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data
    assert "pages" in data 
    
    # 4. Check data types and values
    assert isinstance(data["items"], list)
    assert data["page"] == 1
    assert data["size"] == 10

@pytest.mark.asyncio
async def test_get_restaurants_filter_by_category(client: AsyncClient):
    """
    Feat3-US1: Filter restaurants by category.
    Verify if the category filter works with the new path.
    """
    # Use 'Italian' or 'Pizza' depending on your CSV data
    category = "Italian"
    response = await client.get(f"/api/v1/restaurants/?category={category}")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check if we get a valid list back
    assert "items" in data
    # If the category exists, every item should match it
    for item in data["items"]:
        assert item["category"] == category

@pytest.mark.asyncio
async def test_restaurant_not_found(client: AsyncClient):
    """
    Verify 404 error for a non-existing restaurant ID.
    Note: You need to implement GET /{id} in restaurants.py for this to pass.
    """
    random_id = str(uuid4())
    response = await client.get(f"/api/v1/restaurants/{random_id}")
    
    # If the ID does not exist, it should return 404
    assert response.status_code == 404