import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils import resample
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import os
from diabetes_prediction_implementation import load_data, preprocess_data, data_split, data_scaling, DiabetesPredictor
import joblib

# Set absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
DATASET_PATH = os.path.join(BASE_DIR, 'diabetes_prediction_dataset.csv')

# Model parameters
N_ESTIMATORS = 100
RANDOM_STATE = 42

def train_model():
    try:
        # Load and preprocess data
        print("Loading and preprocessing data...")
        data = load_data()
        preprocessed_data = preprocess_data(data)
        
        # Split the data
        train_x, test_x, train_y, test_y = data_split(preprocessed_data)
        
        # Scale the data
        train_x_scaled, test_x_scaled = data_scaling(train_x, test_x)
        
        # Initialize model
        print("Initializing model...")
        model = RandomForestClassifier(n_estimators=N_ESTIMATORS, random_state=RANDOM_STATE)
        
        # Train the model
        print("Training model...")
        model.fit(train_x_scaled, train_y)
        
        # Evaluate on training set
        train_pred = model.predict(train_x_scaled)
        train_accuracy = accuracy_score(train_y, train_pred)
        
        # Evaluate on test set
        test_pred = model.predict(test_x_scaled)
        test_accuracy = accuracy_score(test_y, test_pred)
        
        # Calculate confusion matrix
        conf_matrix = confusion_matrix(test_y, test_pred)
        
        # Print evaluation metrics
        print("\nModel Evaluation:")
        print(f"Training Accuracy: {train_accuracy:.4f}")
        print(f"Test Accuracy: {test_accuracy:.4f}")
        print("\nConfusion Matrix:")
        print(conf_matrix)
        
        # Save the model
        print("\nSaving model...")
        joblib.dump(model, MODEL_PATH)
        print(f"Model saved to: {MODEL_PATH}")
        
        return True
        
    except Exception as e:
        print(f"Error during training: {str(e)}")
        return False

def evaluate_model():
    try:
        # Load the model
        print("\nEvaluating model...")
        model = joblib.load(MODEL_PATH)
        
        # Load and preprocess data
        data = load_data()
        preprocessed_data = preprocess_data(data)
        
        # Split the data
        train_x, test_x, train_y, test_y = data_split(preprocessed_data)
        
        # Scale the data
        train_x_scaled, test_x_scaled = data_scaling(train_x, test_x)
        
        # Make predictions
        predictions = model.predict(test_x_scaled)
        
        # Calculate accuracy
        accuracy = accuracy_score(test_y, predictions)
        
        # Calculate confusion matrix
        conf_matrix = confusion_matrix(test_y, predictions)
        
        # Calculate sensitivity and specificity
        tn, fp, fn, tp = conf_matrix.ravel()
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        
        # Print results
        print(f"\nEvaluation Results:")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Sensitivity: {sensitivity:.4f}")
        print(f"Specificity: {specificity:.4f}")
        print(f"\nConfusion Matrix:")
        print(conf_matrix)
        
        return True
        
    except Exception as e:
        print(f"Error during evaluation: {str(e)}")
        return False

if __name__ == '__main__':
    print("Starting model training...")
    if train_model():
        print("\nTraining completed successfully!")
        print("Evaluating model...")
        evaluate_model()
    else:
        print("Training failed!")
