from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_predict_endpoint():
    """Test the `/predict` endpoint with a valid request."""
    response = client.post(
        "/predict",
        json={
            "bedrooms": 3,
            "bathrooms": 2,
            "sqft_living": 1000,
            "sqft_lot": 1000,
            "floors": 1,
            "waterfront": 0,
            "view": 0,
            "condition": 3,
            "grade": 7,
            "sqft_above": 1000,
            "sqft_basement": 0,
            "yr_built": 1990,
            "yr_renovated": 0,
            "zipcode": "98102",
            "lat": 47.6097,
            "long": -122.3331,
            "sqft_living15": 1340,
            "sqft_lot15": 7650,
        },
    )
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert "metadata" in response.json()


def test_predict_endpoint_validation_error():
    """Test the `/predict` endpoint with invalid data, expecting a validation error."""
    response = client.post(
        "/predict", json={"bedrooms": -1}
    )  # Example of invalid input
    assert response.status_code == 422  # Validation error
