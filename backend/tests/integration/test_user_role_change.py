import uuid
from fastapi.testclient import TestClient
from app.models.user import RoleEnum


def unique_email(prefix="user") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:6]}@example.com"


def test_admin_can_change_user_role(client: TestClient, create_user):
    user = create_user(email=unique_email("target"), role=RoleEnum.REPORTER)

    response = client.patch(f"/users/{user.id}/role/MAINTAINER")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == user.id
    assert data["role"] == "MAINTAINER"


def test_non_admin_cannot_change_role(client: TestClient, create_user, auth_token):
    non_admin = create_user(email=unique_email("nonadmin"), role=RoleEnum.REPORTER)
    target_user = create_user(email=unique_email("target"))

    token = auth_token(email=non_admin.email, role=non_admin.role)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.patch(f"/users/{target_user.id}/role/ADMIN", headers=headers)
    assert response.status_code == 403


def test_invalid_role_returns_422(client: TestClient, create_user):
    user = create_user(email=unique_email("target"))
    response = client.patch(f"/users/{user.id}/role/INVALIDROLE")
    assert response.status_code == 422


def test_user_not_found_returns_404(client: TestClient):
    response = client.patch("/users/9999/role/ADMIN")
    assert response.status_code == 404
