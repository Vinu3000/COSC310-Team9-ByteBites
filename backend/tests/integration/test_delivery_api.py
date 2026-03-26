import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_delivery_tracking_lifecycle(client: AsyncClient):
    # 1. Place the order
    order_data = {"restaurant_id": 1, "items": ["Sushi"], "total_price": 30.0}
    res = await client.post("/api/v1/orders/place", json=order_data)
    
    # Check if the order was actually created before grabbing the ID
    assert res.status_code == 201 
    order_id = res.json()["id"]

    # 2. Update status 
    update_res = await client.put(
        f"/api/v1/orders/{order_id}/status", 
        params={"new_status": "OUT_FOR_DELIVERY"}
    )
    assert update_res.status_code == 200

    # 3. Check tracking
    track_res = await client.get(f"/api/v1/orders/{order_id}/tracking")
    assert track_res.status_code == 200
    
    data = track_res.json()
    assert data["status"] == "OUT_FOR_DELIVERY"
    assert "on the way" in data["display_message"].lower()