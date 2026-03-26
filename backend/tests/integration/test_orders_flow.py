from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_invalid_status_transition():
    res = client.post("/orders", json={
        "items": [{"unit_price": 10.0, "quantity": 1}],
        "delivery_address": "123 Test St"
    })

    order_id = res.json()["id"]

    res = client.put(f"/orders/{order_id}/status", json={
        "status": "Completed"
    })

    assert res.status_code == 400


def test_payment_rejected_order_unchanged():
    res = client.post("/orders", json={
        "items": [{"unit_price": 20.0, "quantity": 1}],
        "delivery_address": "123 Test St"
    })

    order = res.json()
    order_id = order["id"]

    res = client.post(f"/payments/{order_id}", json={
        "payment_method": "card",
        "card_number": "11110000"
    })

    assert res.status_code == 200
    assert res.json()["payment_status"] == "Rejected"
    assert res.json()["status"] == "Pending"


def test_completed_order_cannot_be_modified():
    res = client.post("/orders", json={
        "items": [{"unit_price": 20.0, "quantity": 1}],
        "delivery_address": "123 Test St"
    })

    order_id = res.json()["id"]

    client.put(f"/orders/{order_id}/status", json={"status": "Preparing"})
    client.put(f"/orders/{order_id}/status", json={"status": "OutForDelivery"})
    client.put(f"/orders/{order_id}/status", json={"status": "Completed"})

    res = client.put(f"/orders/{order_id}/status", json={
        "status": "Preparing"
    })

    assert res.status_code == 400


def test_full_workflow():
    res = client.post("/orders", json={
        "items": [
            {"unit_price": 10.0, "quantity": 2},
            {"unit_price": 5.0, "quantity": 1}
        ],
        "delivery_address": "123 Test St"
    })

    order = res.json()
    order_id = order["id"]

    assert order["subtotal"] == 25.0
    assert order["total"] == 31.25

    res = client.post(f"/payments/{order_id}", json={
        "payment_method": "card",
        "card_number": "12345678"
    })

    assert res.json()["payment_status"] == "Success"

    client.put(f"/orders/{order_id}/status", json={"status": "Preparing"})
    client.put(f"/orders/{order_id}/status", json={"status": "OutForDelivery"})
    client.put(f"/orders/{order_id}/status", json={"status": "Completed"})

    res = client.get("/notifications")
    assert res.status_code == 200
    assert len(res.json()) >= 3