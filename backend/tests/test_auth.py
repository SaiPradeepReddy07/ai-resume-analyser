"""
Authentication Test Suite
Verifies registration, validation rules, login, JWT token issuance, and protected endpoint access.
"""

def test_register_success(client):
    response = client.post("/api/auth/register", json={
        "name": "Jane Doe",
        "email": "jane@example.com",
        "password": "SecurePassword123!",
        "confirm_password": "SecurePassword123!"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Jane Doe"
    assert data["email"] == "jane@example.com"
    assert "password" not in data
    assert "password_hash" not in data


def test_register_password_mismatch(client):
    response = client.post("/api/auth/register", json={
        "name": "Jane Doe",
        "email": "jane2@example.com",
        "password": "Password123!",
        "confirm_password": "DifferentPassword123!"
    })
    assert response.status_code == 422


def test_register_duplicate_email(client, test_user):
    response = client.post("/api/auth/register", json={
        "name": "Another User",
        "email": test_user.email,
        "password": "Password123!",
        "confirm_password": "Password123!"
    })
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_login_success(client, test_user):
    response = client.post("/api/auth/login", json={
        "email": test_user.email,
        "password": "Password123!"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == test_user.email


def test_login_invalid_password(client, test_user):
    response = client.post("/api/auth/login", json={
        "email": test_user.email,
        "password": "WrongPassword999!"
    })
    assert response.status_code == 401


def test_get_me_authenticated(client, auth_headers, test_user):
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["name"] == test_user.name


def test_get_me_unauthorized(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401
