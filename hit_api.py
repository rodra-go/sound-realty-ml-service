import requests

# The base URL for your FastAPI application
BASE_URL = "http://localhost:8000"

# JSON payload for the 'predict' endpoint
predict_payload = {
    "bedrooms": 3.0,
    "bathrooms": 2.5,
    "sqft_living": 2220.0,
    "sqft_lot": 6380.0,
    "floors": 1.5,
    "waterfront": 0.0,
    "view": 0.0,
    "condition": 4.0,
    "grade": 8.0,
    "sqft_above": 1660.0,
    "sqft_basement": 560.0,
    "yr_built": 1931.0,
    "yr_renovated": 0.0,
    "zipcode": "98115",
    "lat": 47.6974,
    "long": -122.313,
    "sqft_living15": 950.0,
    "sqft_lot15": 6380.0,
}

# JSON payload for the 'predict_basic' endpoint
predict_basic_payload = {
    "bedrooms": 3.0,
    "bathrooms": 2.5,
    "sqft_living": 2220.0,
    "sqft_lot": 6380.0,
    "floors": 1,
    "sqft_above": 1660.0,
    "sqft_basement": 560.0,
    "zipcode": "98115",
}


def hit_predict_endpoint():
    response = requests.post(f"{BASE_URL}/predict", json=predict_payload)
    if response.status_code == 200:
        print(f"Predict endpoint response:\n{response.json()}\n\n")
    else:
        print("Error hitting predict endpoint:", response.status_code)


def hit_predict_basic_endpoint():
    response = requests.post(f"{BASE_URL}/predict_basic", json=predict_basic_payload)
    if response.status_code == 200:
        print(f"Predict basic endpoint response:\n{response.json()}\n\n")
    else:
        print("Error hitting predict basic endpoint: ", response.status_code)


if __name__ == "__main__":
    hit_predict_endpoint()
    hit_predict_basic_endpoint()
