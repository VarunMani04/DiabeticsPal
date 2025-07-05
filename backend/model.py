import torch
from diabetes_prediction_implementation import bpnn

class DiabetesModel:
    def __init__(self):
        self.model = bpnn(input=8, hid1=64, hid2=32, hid3=16, numclass=2)
        self.model.load_state_dict(torch.load('model.pth'))
        self.model.eval()

    def predict(self, input_data):
        # Convert input data to numpy array
        input_array = np.array([
            input_data['gender'], input_data['age'], input_data['hypertension'],
            input_data['heart_disease'], input_data['smoking_history'],
            input_data['bmi'], input_data['HbA1c_level'],
            input_data['blood_glucose_level']
        ]).reshape(1, -1)
        
        # Scale the input data
        ss = StandardScaler()
        ss.fit(input_array)
        scaled_data = ss.transform(input_array)
        
        # Convert to tensor
        tensor_data = torch.FloatTensor(scaled_data)
        
        # Make prediction
        with torch.no_grad():
            output = self.model(tensor_data)
            prediction = torch.argmax(output, dim=1).item()
            probability = torch.softmax(output, dim=1).numpy()[0]
            
        return {
            'prediction': int(prediction),
            'probability': float(probability[prediction]),
            'risk_level': 'High' if prediction == 1 else 'Low'
        }
