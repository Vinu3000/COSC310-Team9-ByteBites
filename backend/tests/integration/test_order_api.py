import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_order_status_locking_logic(client: AsyncClient):
    """
    Test Feat4-FR1: Check if COMPLETED orders are locked.
    """
    # Step 1: Place an order
    order_payload = {
        "restaurant_id": 1,
        "items": ["Burger", "Fries"],
        "total_price": 15.99
    }
    create_res = await client.post("/api/v1/orders/place", json=order_payload)
    order_id = create_res.json()["id"]

    # Step 2: Set status to COMPLETED
    await client.put(f"/api/v1/orders/{order_id}/status?new_status=COMPLETED")

    # Step 3: Try to change it back to PENDING (This should fail!)
    fail_res = await client.put(f"/api/v1/orders/{order_id}/status?new_status=PENDING")
    
    # Expect 403 Forbidden because it is locked
    assert fail_res.status_code == 403
    assert "cannot be modified" in fail_res.json()["detail"]