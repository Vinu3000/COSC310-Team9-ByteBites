import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_delivery_tracking_lifecycle(client: AsyncClient):
    """
    Final fix for Feat5 tracking test.
    """
    # 1. Place the order
    order_data = {"restaurant_id": 1, "items": ["Sushi"], "total_price": 30.0}
    res = await client.post("/orders/place", json=order_data)
    order_id = res.json()["id"]

    # Use params= to ensure it goes as a query string
    update_res = await client.put(
        f"/orders/{order_id}/status", 
        params={"new_status": "OUT_FOR_DELIVERY"}
    )
    assert update_res.status_code == 200

    # 3. Check tracking
    track_res = await client.get(f"/orders/{order_id}/tracking")
    data = track_res.json()
    
    assert data["status"] == "OUT_FOR_DELIVERY"
    assert "on the way" in data["display_message"].lower()