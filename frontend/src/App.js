import React, { useState } from 'react';

function App() {
  const [formData, setFormData] = useState({
    gender: '',
    age: '',
    hypertension: '',
    heart_disease: '',
    smoking_history: '',
    bmi: '',
    HbA1c_level: '',
    blood_glucose_level: ''
  });
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    setPrediction(null);

    try {
      const response = await fetch('http://localhost:5004/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setPrediction(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Diabetes Risk Assessment</h1>
      <form onSubmit={handleSubmit} className="form">
        <div className="form-group">
          <label>Gender:</label>
          <select name="gender" value={formData.gender} onChange={handleChange} required>
            <option value="">Select gender</option>
            <option value="Female">Female</option>
            <option value="Male">Male</option>
          </select>
        </div>

        <div className="form-group">
          <label>Age:</label>
          <input
            type="number"
            name="age"
            value={formData.age}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Hypertension:</label>
          <select name="hypertension" value={formData.hypertension} onChange={handleChange} required>
            <option value="">Select</option>
            <option value="0">No</option>
            <option value="1">Yes</option>
          </select>
        </div>

        <div className="form-group">
          <label>Heart Disease:</label>
          <select name="heart_disease" value={formData.heart_disease} onChange={handleChange} required>
            <option value="">Select</option>
            <option value="0">No</option>
            <option value="1">Yes</option>
          </select>
        </div>

        <div className="form-group">
          <label>Smoking History:</label>
          <select name="smoking_history" value={formData.smoking_history} onChange={handleChange} required>
            <option value="">Select</option>
            <option value="never">Never</option>
            <option value="current">Current</option>
            <option value="former">Former</option>
          </select>
        </div>

        <div className="form-group">
          <label>BMI:</label>
          <input
            type="number"
            name="bmi"
            value={formData.bmi}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>HbA1c Level:</label>
          <input
            type="number"
            name="HbA1c_level"
            value={formData.HbA1c_level}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label>Blood Glucose Level:</label>
          <input
            type="number"
            name="blood_glucose_level"
            value={formData.blood_glucose_level}
            onChange={handleChange}
            required
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Predicting...' : 'Predict Risk'}
        </button>
      </form>

      {error && (
        <div className="error">
          <p>{error}</p>
        </div>
      )}

      {prediction && (
        <div className="prediction">
          <h2>Prediction Result</h2>
          <p>Risk Level: {prediction.risk_level}</p>
          <p>Probability: {prediction.probability * 100}%</p>
        </div>
      )}
    </div>
  );
}

export default App;
