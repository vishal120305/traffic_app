import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const featureNames = [
    "Peak type", "Time", "Day of Week", "Weather", "Holiday", "Event", "School Hours",
    "Population Density", "Road Type", "Number of Lanes", "Lane Width (m)", "Road Surface",
    "Slope", "Speed Limit (km/h)", "Traffic Signal", "Stop Sign", "Construction Zone", 
    "Speed Bumps", "Distance to Nearest Junction (m)", "Distance to Nearest Signal (m)", 
    "Traffic Volume", "Average Speed (km/h)", "Vehicle Type Mix", "Accident History", 
    "Industrial Area", "Commercial Area", "Residential Area", "Green Zone", 
    "Public Transport Access", "Parking Availability", "Nearby Schools", "Nearby Hospitals",
    "Nearby Malls", "Weather Description", "Camera Surveillance", "Emergency Lane",
    "Pedestrian Crossings", "Time Since Last Accident", "Road Condition"
  ];

  const [features, setFeatures] = useState(new Array(40).fill(''));
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (index, value) => {
    const updated = [...features];
    updated[index] = value;
    setFeatures(updated);
  };

  const handleReset = () => {
    setFeatures(new Array(40).fill(''));
    setPrediction(null);
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const numericFeatures = features.map(f => Number(f));
      const res = await axios.post('http://127.0.0.1:5000/predict', {
        features: numericFeatures
      });
      setPrediction(res.data.prediction);
    } catch (err) {
      alert("Prediction failed: " + err.message);
    }
    setLoading(false);
  };

  const renderInput = (name, i) => {
    // Example: sliders for Time, Weather, Day of Week
    if (name === "Time") {
      return (
        <div key={i} className="input-group">
          <label>{name}: {features[i]}</label>
          <input type="range" min="0" max="23" value={features[i]} onChange={(e) => handleChange(i, e.target.value)} />
        </div>
      );
    } else if (name === "Weather") {
      return (
        <div key={i} className="input-group">
          <label>{name}: {features[i]}</label>
          <input type="range" min="1" max="5" value={features[i]} onChange={(e) => handleChange(i, e.target.value)} />
        </div>
      );
    } else if (name === "Day of Week") {
      return (
        <div key={i} className="input-group">
          <label>{name}: {features[i]}</label>
          <input type="range" min="1" max="7" value={features[i]} onChange={(e) => handleChange(i, e.target.value)} />
        </div>
      );
    } else {
      return (
        <div key={i} className="input-group">
          <label>{name}</label>
          <input type="number" value={features[i]} onChange={(e) => handleChange(i, e.target.value)} />
        </div>
      );
    }
  };

  return (
    <div className="App">
      <h1>🚦 Traffic Flow Prediction</h1>
      <div className="form">
        {featureNames.map((name, i) => renderInput(name, i))}
        <div className="button-group">
          <button onClick={handleSubmit}>Predict</button>
          <button onClick={handleReset} className="reset">Reset</button>
        </div>
        {loading && <div className="loader"></div>}
        {prediction !== null && !loading && (
          <h2>Predicted Traffic Level: <span className="result">{prediction}</span></h2>
        )}
      </div>
    </div>
  );
}

export default App;
