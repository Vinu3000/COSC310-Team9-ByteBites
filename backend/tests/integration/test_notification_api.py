import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_notification_flow(client: AsyncClient):
    """
    Feat8-US1: Check if a notification is created when an order is placed.
    """
    # 1. Place an order (should trigger notification)
    payload = {"restaurant_id": 1, "items": ["Pizza"], "total_price": 20.0}
    # Using the /api/v1 prefix as seen in your structure
    await client.post("/api/v1/orders/place", json=payload)

    # 2. Check the notifications endpoint
    response = await client.get("/api/v1/notifications/")
    
    assert response.status_code == 200
    data = response.json()
    
    # 3. Verify we have at least one message
    assert len(data) > 0
    assert "accepted" in data[-1]["message"].lower()
