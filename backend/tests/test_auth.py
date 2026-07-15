def test_register_user(client):
    """
    Test registering a new user account.
    """
    payload = {
        "username": "testuser",
        "email": "testuser@leafsense.ai",
        "password": "securepassword123"
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@leafsense.ai"
    assert "id" in data

def test_register_duplicate_username(client):
    """
    Test duplicate username registration returns 400 Bad Request.
    """
    payload_1 = {
        "username": "testuser",
        "email": "testuser1@leafsense.ai",
        "password": "securepassword123"
    }
    payload_2 = {
        "username": "testuser",
        "email": "testuser2@leafsense.ai",
        "password": "securepassword123"
    }
    
    # First sign up succeeds
    response_1 = client.post("/api/auth/register", json=payload_1)
    assert response_1.status_code == 201

    # Second sign up with duplicate username fails
    response_2 = client.post("/api/auth/register", json=payload_2)
    assert response_2.status_code == 400
    assert response_2.json()["detail"] == "Username already registered."

def test_register_duplicate_email(client):
    """
    Test duplicate email registration returns 400 Bad Request.
    """
    payload_1 = {
        "username": "testuser1",
        "email": "testuser@leafsense.ai",
        "password": "securepassword123"
    }
    payload_2 = {
        "username": "testuser2",
        "email": "testuser@leafsense.ai",
        "password": "securepassword123"
    }
    
    # First sign up succeeds
    response_1 = client.post("/api/auth/register", json=payload_1)
    assert response_1.status_code == 201

    # Second sign up with duplicate email fails
    response_2 = client.post("/api/auth/register", json=payload_2)
    assert response_2.status_code == 400
    assert response_2.json()["detail"] == "Email address already registered."

def test_login_user(client):
    """
    Test login with valid credentials issues a JWT Access Token.
    """
    # 1. Register a user
    register_payload = {
        "username": "testuser",
        "email": "testuser@leafsense.ai",
        "password": "securepassword123"
    }
    client.post("/api/auth/register", json=register_payload)

    # 2. Login
    login_data = {
        "username": "testuser",
        "password": "securepassword123"
    }
    # OAuth2 specifies logins occur via x-www-form-urlencoded (data argument)
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password(client):
    """
    Test login with wrong password returns 400 Bad Request.
    """
    # 1. Register a user
    register_payload = {
        "username": "testuser",
        "email": "testuser@leafsense.ai",
        "password": "securepassword123"
    }
    client.post("/api/auth/register", json=register_payload)

    # 2. Login with wrong password
    login_data = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username, email, or password."
