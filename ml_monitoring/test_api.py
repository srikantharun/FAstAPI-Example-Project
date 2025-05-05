import requests
import pandas as pd
import json
import time
import random

def test_prediction_api(base_url="http://localhost:8000/api/v1"):
    """
    Test the prediction API with random data.
    
    Args:
        base_url: Base URL of the API
    """
    print("Testing prediction API...")
    
    # Load test data
    try:
        current_data = pd.read_csv("./data/current_data.csv")
        print(f"Loaded {len(current_data)} samples from test data")
    except Exception:
        print("Failed to load test data, generating random features")
        features = {f"feature{i+1}": random.normalvariate(0, 1) for i in range(5)}
        prediction_data = {"features": features}
        response = requests.post(
            f"{base_url}/predictions/predict",
            json=prediction_data
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Prediction result: {result}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
        
        return
    
    # Get feature columns
    feature_cols = [col for col in current_data.columns if col.startswith("feature")]
    
    # Test with multiple samples
    prediction_ids = []
    for i in range(min(10, len(current_data))):
        features = current_data.iloc[i][feature_cols].to_dict()
        
        # Make prediction
        prediction_data = {"features": features}
        response = requests.post(
            f"{base_url}/predictions/predict",
            json=prediction_data
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Sample {i+1} prediction: {result['prediction']}")
        else:
            print(f"Error for sample {i+1}: {response.status_code} - {response.text}")
            continue
        
        # Get predictions list to find the ID
        if i == 0:  # Only do this once
            predictions_response = requests.get(f"{base_url}/predictions/predictions")
            if predictions_response.status_code == 200:
                predictions = predictions_response.json()["predictions"]
                if predictions:
                    prediction_ids = [p["id"] for p in predictions[:min(10, len(predictions))]]
    
    # Update actual values for some predictions
    print("\nUpdating actual values...")
    for i, pred_id in enumerate(prediction_ids):
        if not pred_id or i >= len(current_data):
            continue
            
        actual_value = float(current_data.iloc[i]["target"])
        
        actual_data = {
            "prediction_id": pred_id,
            "actual_value": actual_value
        }
        
        response = requests.post(
            f"{base_url}/predictions/update-actual-value",
            json=actual_data
        )
        
        if response.status_code == 200:
            print(f"Updated actual value for prediction {pred_id}")
        else:
            print(f"Error updating actual value: {response.status_code} - {response.text}")

def test_monitoring_apis(base_url="http://localhost:8000/api/v1"):
    """
    Test the monitoring APIs.
    
    Args:
        base_url: Base URL of the API
    """
    print("\nTesting monitoring APIs...")
    
    # Generate model performance report
    print("Generating model performance report...")
    response = requests.get(f"{base_url}/monitoring/monitor-model")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Model performance report generated: {result}")
    else:
        print(f"Error generating model performance report: {response.status_code} - {response.text}")
    
    # Generate data drift report
    print("\nGenerating data drift report...")
    response = requests.get(f"{base_url}/monitoring/monitor-target")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Data drift report generated: {result}")
    else:
        print(f"Error generating data drift report: {response.status_code} - {response.text}")
    
    # Get model metrics
    print("\nGetting model metrics...")
    response = requests.get(f"{base_url}/monitoring/metrics")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Model metrics: {result}")
    else:
        print(f"Error getting model metrics: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Wait for the API to be available
    print("Waiting for the API to be available...")
    time.sleep(2)
    
    # Test prediction API
    test_prediction_api()
    
    # Test monitoring APIs
    test_monitoring_apis()