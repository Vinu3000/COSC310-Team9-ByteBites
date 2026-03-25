import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_delivery_tracking_lifecycle(client: AsyncClient):
    """
    Tests Feat5-FR1 (Status Update) and Feat5-US1 (User Tracking).
    """
    # 1. Place an order first
    order_data = {"restaurant_id": 1, "items": ["Taco"], "total_price": 12.5}
    res = await client.post("/orders/place", json=order_data)
    order_id = res.json()["id"]

    # 2. Change status to OUT_FOR_DELIVERY (FR1)
    await client.put(f"/orders/{order_id}/delivery?new_status=OUT_FOR_DELIVERY")

    # 3. Check if user sees the tracking message (US1)
    track_res = await client.get(f"/orders/{order_id}/tracking")
    assert track_res.status_code == 200
    assert track_res.json()["status"] == "OUT_FOR_DELIVERY"
    assert "on the way" in track_res.json()["display_message"]