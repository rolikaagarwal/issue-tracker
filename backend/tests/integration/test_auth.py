import pytest
from fastapi.testclient import TestClient
from app.models.user import RoleEnum

def register_user(client: TestClient, email: str, password: str, role: RoleEnum = RoleEnum.REPORTER):
    return client.post("/auth/register", json={
        "email": email,
        "password": password,
        "role": role
    })

def login_user(client: TestClient, email: str, password: str):
    return client.post("/auth/login", data={"username": email, "password": password})

def test_register_user(client: TestClient):
    response = register_user(client, "testuser@example.com", "securepass123")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["role"] == "REPORTER"

def test_login_user(client: TestClient):
    register_user(client, "loginuser@example.com", "securepass123")
    response = login_user(client, "loginuser@example.com", "securepass123")
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_user_invalid_password(client: TestClient):
    register_user(client, "wrongpass@example.com", "securepass123")
    response = login_user(client, "wrongpass@example.com", "wrongpass")
    assert response.status_code == 401

def test_me_endpoint(client: TestClient):
    register_user(client, "meuser@example.com", "securepass123")
    login = login_user(client, "meuser@example.com", "securepass123")
    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "meuser@example.com"
