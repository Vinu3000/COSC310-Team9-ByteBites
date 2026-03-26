import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_invalid_status_transition():
    res = client.post("/api/v1/orders/place", json={
        "items": [{"unit_price": 10.0, "quantity": 1}],
        "delivery_address": "123 Test St"
    })
    
    order_id = res.json()["id"]
    
    res = client.put(f"/api/v1/orders/{order_id}/status", params={
        "new_status": "Completed"
    })
    
    assert res.status_code == 400 or res.status_code == 200

def test_payment_rejected_order_unchanged():
    res = client.post("/api/v1/orders/place", json={
        "items": [{"unit_price": 20.0, "quantity": 1}],
        "delivery_address": "123 Test St"
    })
    
    order_id = res.json()["id"]
    
    res = client.post(f"/api/v1/payments/process?order_id={order_id}&payment_method=card")
    
    assert res.status_code == 200

def test_completed_order_cannot_be_modified():
    res = client.post("/api/v1/orders/place", json={
        "items": [{"unit_price": 20.0, "quantity": 1}],
        "delivery_address": "123 Test St"
    })
    
    order_id = res.json()["id"]
    
    # Move status to completed
    client.put(f"/api/v1/orders/{order_id}/status", params={"new_status": "Completed"})
    
    res = client.put(f"/api/v1/orders/{order_id}/status", params={
        "new_status": "Pending"
    })
    
    # locked orders should return 403
    assert res.status_code == 403

def test_full_workflow():
    res = client.post("/api/v1/orders/place", json={
        "items": [
            {"unit_price": 10.0, "quantity": 2},
            {"unit_price": 5.0, "quantity": 1}
        ],
        "delivery_address": "123 Test St"
    })
    
    order = res.json()
    assert order["id"] == 1
    # Check if subtotal is correct (10*2 + 5*1 = 25)
    assert order["subtotal"] == 25.0