import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import os

def generate_synthetic_data(n_samples=1000, n_features=5, random_seed=42):
    """
    Generate synthetic data for ML model training and monitoring.
    
    Args:
        n_samples: Number of samples to generate
        n_features: Number of features to generate
        random_seed: Random seed for reproducibility
        
    Returns:
        DataFrame: Generated data
    """
    np.random.seed(random_seed)
    
    # Generate features
    X = np.random.normal(0, 1, size=(n_samples, n_features))
    
    # Generate column names
    feature_names = [f"feature{i+1}" for i in range(n_features)]
    
    # Generate coefficients
    true_coefs = np.random.uniform(-2, 2, size=n_features)
    
    # Generate target with some noise
    y = X @ true_coefs + np.random.normal(0, 0.5, size=n_samples)
    
    # Create DataFrame
    data = pd.DataFrame(X, columns=feature_names)
    data["target"] = y
    
    # Add timestamp for time series analysis
    dates = pd.date_range(start="2023-01-01", periods=n_samples, freq="H")
    data["timestamp"] = dates
    
    return data

def train_and_save_model(data, model_path="./data/model.pkl"):
    """
    Train a simple linear regression model and save it.
    
    Args:
        data: Training data
        model_path: Path to save the model
    """
    # Prepare data
    feature_cols = [col for col in data.columns if col.startswith("feature")]
    X = data[feature_cols]
    y = data["target"]
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Save model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    
    print(f"Model saved to {model_path}")
    
    return model

def main():
    # Generate data
    print("Generating synthetic data...")
    data = generate_synthetic_data(n_samples=1000, n_features=5)
    
    # Split data into reference and current datasets
    reference_data, current_data = train_test_split(
        data, test_size=0.3, random_state=42
    )
    
    # Save reference data
    os.makedirs("./data", exist_ok=True)
    reference_data.to_csv("./data/reference_data.csv", index=False)
    print("Reference data saved to ./data/reference_data.csv")
    
    # Save current data for testing
    current_data.to_csv("./data/current_data.csv", index=False)
    print("Current data saved to ./data/current_data.csv")
    
    # Train and save model
    model = train_and_save_model(reference_data)
    
    print("Data generation complete!")
    
if __name__ == "__main__":
    main()