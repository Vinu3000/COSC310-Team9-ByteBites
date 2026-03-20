from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Unit test: duplicate username should fail
def test_duplicate_username_returns_400():
    client.post("/auth/register", json={"username": "alice", "password": "pass123"})
    response = client.post("/auth/register", json={"username": "alice", "password": "pass123"})
    assert response.status_code == 400

# Unit test: wrong password should fail
def test_invalid_login_returns_401():
    response = client.post("/auth/login", json={"username": "nobody", "password": "wrong"})
    assert response.status_code == 401

# Unit test: accessing /me without token should fail
def test_no_token_returns_401():
    response = client.get("/auth/me")
    assert response.status_code == 401
# Integration test: full register → login → access flow
def test_register_login_then_access_me():
    # Step 1: register
    client.post("/auth/register", json={"username": "bob", "password": "secret99"})
    
    # Step 2: login
    login_res = client.post("/auth/login", json={"username": "bob", "password": "secret99"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    
    # Step 3: use token to access protected route
    me_res = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["username"] == "bob"