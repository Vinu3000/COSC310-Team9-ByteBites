from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_request_refund_success():
    response = client.post("/refunds/1/request", json={"reason": "Changed my mind"})
    assert response.status_code == 200
    data = response.json()
    assert data["refund_status"] == "Requested"


def test_request_refund_invalid_status():
    response = client.post("/refunds/2/request", json={"reason": "Too late"})
    assert response.status_code == 400
    assert "Pending or Preparing" in response.json()["detail"]


def test_approve_refund_success():
    client.post("/refunds/1/request", json={"reason": "Testing approval"})
    response = client.put("/refunds/1/approve")
    assert response.status_code == 200
    data = response.json()
    assert data["refund_status"] == "Approved"


def test_reject_refund_requires_requested_status():
    response = client.put("/refunds/2/reject")
    assert response.status_code == 400
    assert "No pending refund request" in response.json()["detail"]
