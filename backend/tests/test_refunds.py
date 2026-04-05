from fastapi.testclient import TestClient
from app.main import app
from app.api.v1.shared_data import mock_orders_db
from app.models.enums import OrderStatus

client = TestClient(app)


def setup_function():
    mock_orders_db.clear()
    mock_orders_db["order-1"] = {
        "id": "order-1",
        "items": [{"name": "Burger", "price": 10, "quantity": 1}],
        "subtotal": 10,
        "total_price": 12,
        "status": OrderStatus.PENDING,
        "payment_status": "Success",
        "refund_status": "None",
        "refund_reason": None,
    }
    mock_orders_db["order-2"] = {
        "id": "order-2",
        "items": [{"name": "Pizza", "price": 15, "quantity": 1}],
        "subtotal": 15,
        "total_price": 18,
        "status": OrderStatus.COMPLETED,
        "payment_status": "Success",
        "refund_status": "None",
        "refund_reason": None,
    }
    mock_orders_db["order-3"] = {
        "id": "order-3",
        "items": [{"name": "Fries", "price": 5, "quantity": 1}],
        "subtotal": 5,
        "total_price": 6,
        "status": OrderStatus.PENDING,
        "payment_status": "Rejected",
        "refund_status": "None",
        "refund_reason": None,
    }


def test_request_refund_success():
    response = client.post("/refunds/order-1/request", json={"reason": "Changed my mind"})
    assert response.status_code == 200
    data = response.json()
    assert data["refund_status"] == "Requested"


def test_request_refund_invalid_status():
    response = client.post("/refunds/order-2/request", json={"reason": "Too late"})
    assert response.status_code == 400
    assert "Pending or Preparing" in response.json()["detail"]


def test_request_refund_unpaid_order():
    response = client.post("/refunds/order-3/request", json={"reason": "Payment failed"})
    assert response.status_code == 400
    assert "successfully paid orders" in response.json()["detail"]


def test_approve_refund_success():
    client.post("/refunds/order-1/request", json={"reason": "Testing approval"})
    response = client.put("/refunds/order-1/approve")
    assert response.status_code == 200
    data = response.json()
    assert data["refund_status"] == "Approved"


def test_reject_refund_requires_requested_status():
    response = client.put("/refunds/order-2/reject")
    assert response.status_code == 400
    assert "No pending refund request" in response.json()["detail"]
