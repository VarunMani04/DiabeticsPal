import os
from flask import Flask, request, jsonify
from diabetes_prediction_implementation import DiabetesPredictor

# Initialize the predictor
predictor = DiabetesPredictor()

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict_route():
    try:
        data = request.json
        if not isinstance(data, dict):
            return jsonify({'error': 'Invalid input format. Expected JSON object.'}), 400
        
        result = predictor.predict(data)
        return jsonify(result)
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        return jsonify({'error': error_msg}), 400

@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Test the predictor with sample data
        test_data = {
            'gender': 'Female',
            'age': 45.0,
            'hypertension': 0,
            'heart_disease': 0,
            'smoking_history': 'never',
            'bmi': 25.5,
            'HbA1c_level': 6.5,
            'blood_glucose_level': 120.0
        }
        predictor.predict(test_data)
        return jsonify({'status': 'healthy'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    print(f"Starting Flask server on port 5004...")
    app.run(debug=True, port=5004, host='127.0.0.1')
