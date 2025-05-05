import requests
import json
import time

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1"

def test_predict():
    """Test the prediction endpoint."""
    url = f"{BASE_URL}/predictions/predict"
    
    # Prediction data with 5 features
    payload = {
        "features": {
            "feature1": 0.5,
            "feature2": -0.2,
            "feature3": 0.3,
            "feature4": -0.1,
            "feature5": 0.8
        }
    }
    
    # Make the request
    response = requests.post(url, json=payload)
    
    # Print the results
    print(f"Prediction Response:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    return response.json()

def test_predictions_list():
    """Test the predictions list endpoint."""
    url = f"{BASE_URL}/predictions/predictions"
    
    # Make the request
    response = requests.get(url)
    
    # Print the results
    print(f"Predictions List Response:")
    print(f"Status Code: {response.status_code}")
    print(f"Total Predictions: {response.json().get('total', 0)}")
    predictions = response.json().get('predictions', [])
    print(f"Number of Predictions Returned: {len(predictions)}")
    if predictions:
        print(f"First Prediction: {json.dumps(predictions[0], indent=2)}")
    print()

def test_monitoring_endpoints():
    """Test the monitoring endpoints."""
    # Test model monitoring endpoint
    url = f"{BASE_URL}/monitoring/monitor-model"
    
    print("Testing model monitoring endpoint...")
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")
    print()
    
    # Test data drift endpoint
    url = f"{BASE_URL}/monitoring/monitor-target"
    
    print("Testing data drift monitoring endpoint...")
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")
    print()

def test_update_actual_value(prediction_id, actual_value):
    """Test updating actual value for a prediction."""
    url = f"{BASE_URL}/predictions/update-actual-value"
    
    payload = {
        "prediction_id": prediction_id,
        "actual_value": actual_value
    }
    
    # Make the request
    response = requests.post(url, json=payload)
    
    # Print the results
    print(f"Update Actual Value Response:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def main():
    # Test prediction endpoint
    prediction_result = test_predict()
    
    # Wait a bit for the prediction to be saved
    time.sleep(1)
    
    # Test predictions list
    test_predictions_list()
    
    # Make more predictions
    for _ in range(5):
        test_predict()
        time.sleep(0.5)
    
    # Get predictions list to find a prediction ID
    url = f"{BASE_URL}/predictions/predictions"
    response = requests.get(url)
    predictions = response.json().get('predictions', [])
    
    if predictions:
        # Update actual value for the first prediction
        prediction_id = predictions[0]['id']
        test_update_actual_value(prediction_id, 1.5)
    
    # Wait a bit for the update to be processed
    time.sleep(1)
    
    # Test monitoring endpoints
    test_monitoring_endpoints()

if __name__ == "__main__":
    main()