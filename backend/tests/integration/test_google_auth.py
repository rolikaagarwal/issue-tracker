from unittest.mock import patch
from fastapi.testclient import TestClient

GOOGLE_ID_TOKEN = "dummy_id_token"

def get_mock_google_payload(email="googleuser@example.com", name="Google User"):
    return {
        "email": email,
        "name": name,
        "aud": "test-client-id"
    }

def test_google_login_creates_user(client: TestClient):
    with patch("google.oauth2.id_token.verify_oauth2_token") as mock_verify:
        mock_verify.return_value = get_mock_google_payload()
        response = client.post("/google-login", json={"id_token": GOOGLE_ID_TOKEN})
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

def test_google_login_existing_user(client: TestClient, create_user):
    create_user("googleuser@example.com")
    with patch("google.oauth2.id_token.verify_oauth2_token") as mock_verify:
        mock_verify.return_value = get_mock_google_payload()
        response = client.post("/google-login", json={"id_token": GOOGLE_ID_TOKEN})
        assert response.status_code == 200
        assert "access_token" in response.json()

def test_google_login_invalid_token(client: TestClient):
    with patch("google.oauth2.id_token.verify_oauth2_token", side_effect=ValueError):
        response = client.post("/google-login", json={"id_token": "bad_token"})
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid Google token"

def test_google_login_missing_token(client: TestClient):
    response = client.post("/google-login", json={})
    assert response.status_code == 422

def test_google_login_uses_name_if_present(client: TestClient):
    mock_payload = get_mock_google_payload(name="Test Name")
    with patch("google.oauth2.id_token.verify_oauth2_token") as mock_verify:
        mock_verify.return_value = mock_payload
        response = client.post("/google-login", json={"id_token": GOOGLE_ID_TOKEN})
        assert response.status_code == 200
        assert "access_token" in response.json()
