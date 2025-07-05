from fastapi.testclient import TestClient
from app.models.user import RoleEnum


def register_user(client: TestClient, email: str, password: str = "testpass", role: RoleEnum = RoleEnum.REPORTER):
    return client.post("/auth/register", json={
        "email": email,
        "password": password,
        "role": role
    })


def login_user(client: TestClient, email: str, password: str = "testpass"):
    return client.post("/auth/login", data={
        "username": email,
        "password": password
    })


def test_register_duplicate_email(client: TestClient):
    """Should return 400 for duplicate email registration."""
    email = "dupe@example.com"
    register_user(client, email, "secure123")
    response = register_user(client, email, "secure123")  # Second attempt
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_nonexistent_user(client: TestClient):
    """Should return 401 when trying to login with unknown email."""
    response = login_user(client, "nosuchuser@example.com", "whatever")
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_me_unauthenticated(client: TestClient):
    """Should return 401 when accessing /auth/me without token."""
    response = client.get("/auth/me")
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]
