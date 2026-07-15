import io
from unittest.mock import patch
from app.services.prediction_service import PredictionModelSingleton

# Helper to register and log in a test user to acquire authorization headers
def get_auth_headers(client):
    register_payload = {
        "username": "tester",
        "email": "tester@leafsense.ai",
        "password": "securepassword123"
    }
    client.post("/api/auth/register", json=register_payload)

    login_data = {
        "username": "tester",
        "password": "securepassword123"
    }
    response = client.post("/api/auth/login", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@patch.object(PredictionModelSingleton, 'predict_image')
def test_predict_leaf_success(mock_predict, client):
    """
    Test uploading a leaf image successfully with proper auth headers.
    Mocks the ML model classification response.
    """
    # 1. Mock singleton classification response
    mock_predict.return_value = {
        "class_id": "Strawberry___healthy",
        "disease_name": "Healthy Strawberry",
        "scientific_name": "Fragaria ananassa",
        "confidence": 0.985,
        "is_healthy": True,
        "details": {
            "description": "Healthy foliage.",
            "symptoms": "None",
            "causes": "N/A",
            "treatment": "N/A",
            "prevention": "Standard watering."
        }
    }

    # 2. Get auth headers
    headers = get_auth_headers(client)

    # 3. Simulate uploading image file
    file_content = b"fake image bytes data"
    file_like = io.BytesIO(file_content)
    files = {"file": ("strawberry_leaf.jpg", file_like, "image/jpeg")}

    response = client.post("/api/predictions/predict", headers=headers, files=files)
    assert response.status_code == 200
    
    data = response.json()
    assert data["class_id"] == "Strawberry___healthy"
    assert data["disease_name"] == "Healthy Strawberry"
    assert data["confidence"] == 0.985
    assert data["is_healthy"] is True
    assert "strawberry plant is healthy" in data["details"]["description"]

def test_predict_leaf_unauthorized(client):
    """
    Test uploading a leaf without authorization returns 401 Unauthorized.
    """
    file_content = b"fake image bytes data"
    file_like = io.BytesIO(file_content)
    files = {"file": ("strawberry_leaf.jpg", file_like, "image/jpeg")}

    response = client.post("/api/predictions/predict", files=files)
    assert response.status_code == 401

@patch.object(PredictionModelSingleton, 'predict_image')
def test_get_history(mock_predict, client):
    """
    Test retrieving a user's prediction history logs.
    """
    mock_predict.return_value = {
        "class_id": "Apple___Apple_scab",
        "disease_name": "Apple Scab",
        "scientific_name": "Venturia inaequalis",
        "confidence": 0.88,
        "is_healthy": False,
        "details": {}
    }
    
    headers = get_auth_headers(client)
    
    # 1. Run a mock scan to populate database
    file_like = io.BytesIO(b"data")
    client.post("/api/predictions/predict", headers=headers, files={"file": ("leaf.jpg", file_like, "image/jpeg")})

    # 2. Fetch history list
    response = client.get("/api/predictions/history", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["class_id"] == "Apple___Apple_scab"
    assert data[0]["confidence"] == 0.88

@patch.object(PredictionModelSingleton, 'predict_image')
def test_delete_history_item(mock_predict, client):
    """
    Test deleting a specific prediction scan from logs.
    """
    mock_predict.return_value = {
        "class_id": "Tomato___healthy",
        "disease_name": "Healthy Tomato",
        "scientific_name": "Solanum lycopersicum",
        "confidence": 0.95,
        "is_healthy": True,
        "details": {}
    }
    
    headers = get_auth_headers(client)
    
    # 1. Run a mock scan to populate database
    file_like = io.BytesIO(b"data")
    scan_res = client.post("/api/predictions/predict", headers=headers, files={"file": ("leaf.jpg", file_like, "image/jpeg")})
    
    # Retrieve the saved prediction ID (need to fetch history list to get the ID)
    history_res = client.get("/api/predictions/history", headers=headers)
    prediction_id = history_res.json()[0]["id"]

    # 2. Delete history item
    del_response = client.delete(f"/api/predictions/history/{prediction_id}", headers=headers)
    assert del_response.status_code == 200
    assert del_response.json()["message"] == "Prediction history entry deleted successfully."

    # 3. Verify history is now empty
    history_check = client.get("/api/predictions/history", headers=headers)
    assert len(history_check.json()) == 0
