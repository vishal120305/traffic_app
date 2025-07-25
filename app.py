from flask import Flask, request, jsonify
import joblib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load your trained model
model = joblib.load("traffic_model.pkl")  # Replace with actual filename if different

@app.route('/', methods=['GET'])
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Traffic Flow Prediction System</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                background: white; 
                border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 { font-size: 2.5em; margin-bottom: 10px; }
            .header p { font-size: 1.2em; opacity: 0.9; }
            .content { padding: 30px; }
            .prediction-form {
                background: #f8f9fa;
                padding: 25px;
                border-radius: 10px;
                margin-bottom: 30px;
                border: 2px solid #e9ecef;
            }
            .form-section {
                margin-bottom: 25px;
            }
            .form-section h3 {
                color: #495057;
                margin-bottom: 15px;
                padding-bottom: 8px;
                border-bottom: 2px solid #dee2e6;
            }
            .features-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-bottom: 20px;
            }
            .feature-group {
                background: white;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #dee2e6;
            }
            .feature-group label {
                display: block;
                font-weight: 600;
                color: #495057;
                margin-bottom: 5px;
                font-size: 0.9em;
            }
            .feature-group input {
                width: 100%;
                padding: 8px 12px;
                border: 1px solid #ced4da;
                border-radius: 5px;
                font-size: 14px;
                transition: border-color 0.3s;
            }
            .feature-group input:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.25);
            }
            .button-group {
                display: flex;
                gap: 15px;
                justify-content: center;
                margin-top: 25px;
            }
            .btn {
                padding: 12px 30px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            .btn-secondary {
                background: #6c757d;
                color: white;
            }
            .btn-secondary:hover {
                background: #5a6268;
                transform: translateY(-2px);
            }
            .btn-sample {
                background: #28a745;
                color: white;
            }
            .btn-sample:hover {
                background: #218838;
                transform: translateY(-2px);
            }
            .result-section {
                margin-top: 30px;
                padding: 25px;
                background: #f8f9fa;
                border-radius: 10px;
                border: 2px solid #e9ecef;
                display: none;
            }
            .result-success {
                border-color: #28a745;
                background: #d4edda;
            }
            .result-error {
                border-color: #dc3545;
                background: #f8d7da;
            }
            .result-content {
                text-align: center;
            }
            .prediction-value {
                font-size: 2.5em;
                font-weight: bold;
                color: #28a745;
                margin: 15px 0;
            }
            .loading {
                display: none;
                text-align: center;
                padding: 20px;
            }
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 15px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .api-info {
                background: #e7f3ff;
                padding: 20px;
                border-radius: 10px;
                border-left: 5px solid #007bff;
                margin-top: 30px;
            }
            .status-badge {
                display: inline-block;
                background: #28a745;
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.9em;
                font-weight: 600;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚗 Traffic Flow Prediction System</h1>
                <p>Advanced ML-powered traffic analysis using XGBoost</p>
                <span class="status-badge">✅ System Online</span>
            </div>
            
            <div class="content">
                <div class="prediction-form">
                    <h2 style="color: #495057; margin-bottom: 20px; text-align: center;">
                        📊 Enter Traffic Features for Prediction
                    </h2>
                    
                    <form id="predictionForm">
                        <div class="form-section">
                            <h3>🚦 Traffic Features (40 values required)</h3>
                            <div class="features-grid" id="featuresGrid">
                                <!-- Features will be generated by JavaScript -->
                            </div>
                        </div>
                        
                        <div class="button-group">
                            <button type="button" class="btn btn-sample" onclick="fillSampleData()">
                                📝 Fill Sample Data
                            </button>
                            <button type="button" class="btn btn-secondary" onclick="clearForm()">
                                🗑️ Clear All
                            </button>
                            <button type="submit" class="btn btn-primary">
                                🔮 Predict Traffic Flow
                            </button>
                        </div>
                    </form>
                    
                    <div class="loading" id="loading">
                        <div class="spinner"></div>
                        <p>Processing your prediction...</p>
                    </div>
                    
                    <div class="result-section" id="resultSection">
                        <div class="result-content" id="resultContent">
                            <!-- Results will be displayed here -->
                        </div>
                    </div>
                </div>
                
                <div class="api-info">
                    <h3 style="color: #007bff; margin-bottom: 15px;">🔧 System Information</h3>
                    <ul style="list-style: none; padding: 0;">
                        <li style="margin: 8px 0;"><strong>Model:</strong> XGBoost 2.1.4</li>
                        <li style="margin: 8px 0;"><strong>Framework:</strong> Flask 2.3.3 + Gunicorn</li>
                        <li style="margin: 8px 0;"><strong>Features:</strong> 40 numerical traffic parameters</li>
                        <li style="margin: 8px 0;"><strong>API Health:</strong> <a href="/health" target="_blank">Check Status</a></li>
                    </ul>
                </div>
            </div>
        </div>

        <script>
            // Generate feature input fields
            function generateFeatureInputs() {
                const grid = document.getElementById('featuresGrid');
                const featureNames = [
                    'Hour', 'Day of Week', 'Month', 'Temperature', 'Humidity',
                    'Wind Speed', 'Visibility', 'Pressure', 'Weather Code', 'Is Weekend',
                    'Is Holiday', 'Lane Count', 'Speed Limit', 'Road Type', 'Traffic Density',
                    'Vehicle Count', 'Heavy Vehicle %', 'Average Speed', 'Congestion Level', 'Incident Count',
                    'Construction Zone', 'School Zone', 'Commercial Area', 'Residential Area', 'Industrial Area',
                    'Peak Hour', 'Off Peak', 'Rush Hour', 'Night Time', 'Dawn Time',
                    'Dusk Time', 'Clear Weather', 'Rainy Weather', 'Snowy Weather', 'Foggy Weather',
                    'Traffic Signal', 'Roundabout', 'Highway', 'City Road', 'Rural Road'
                ];
                
                for (let i = 0; i < 40; i++) {
                    const featureGroup = document.createElement('div');
                    featureGroup.className = 'feature-group';
                    
                    const label = document.createElement('label');
                    label.textContent = `${featureNames[i] || 'Feature ' + (i + 1)}`;
                    
                    const input = document.createElement('input');
                    input.type = 'number';
                    input.step = 'any';
                    input.name = `feature_${i}`;
                    input.id = `feature_${i}`;
                    input.placeholder = '0.0';
                    input.required = true;
                    
                    featureGroup.appendChild(label);
                    featureGroup.appendChild(input);
                    grid.appendChild(featureGroup);
                }
            }
            
            // Fill sample data
            function fillSampleData() {
                const sampleData = [
                    12, 2, 6, 22.5, 65, 15.2, 10, 1013.2, 1, 0,
                    0, 4, 60, 1, 0.7, 150, 0.15, 45.2, 2, 0,
                    0, 0, 1, 0, 0, 1, 0, 1, 0, 0,
                    0, 1, 0, 0, 0, 1, 0, 1, 0, 0
                ];
                
                for (let i = 0; i < 40; i++) {
                    document.getElementById(`feature_${i}`).value = sampleData[i];
                }
            }
            
            // Clear form
            function clearForm() {
                for (let i = 0; i < 40; i++) {
                    document.getElementById(`feature_${i}`).value = '';
                }
                document.getElementById('resultSection').style.display = 'none';
            }
            
            // Handle form submission
            document.getElementById('predictionForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                // Collect features
                const features = [];
                for (let i = 0; i < 40; i++) {
                    const value = parseFloat(document.getElementById(`feature_${i}`).value);
                    if (isNaN(value)) {
                        alert(`Please enter a valid number for ${document.querySelector(`label[for="feature_${i}"]`).textContent}`);
                        return;
                    }
                    features.push(value);
                }
                
                // Show loading
                document.getElementById('loading').style.display = 'block';
                document.getElementById('resultSection').style.display = 'none';
                
                try {
                    const response = await fetch('/predict', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ features: features })
                    });
                    
                    const result = await response.json();
                    
                    // Hide loading
                    document.getElementById('loading').style.display = 'none';
                    
                    // Show result
                    const resultSection = document.getElementById('resultSection');
                    const resultContent = document.getElementById('resultContent');
                    
                    if (response.ok) {
                        resultSection.className = 'result-section result-success';
                        resultContent.innerHTML = `
                            <h3 style="color: #28a745; margin-bottom: 15px;">✅ Prediction Successful</h3>
                            <div class="prediction-value">${result.prediction.toFixed(6)}</div>
                            <p style="color: #495057; font-size: 1.1em;">
                                <strong>Traffic Flow Prediction Value</strong><br>
                                <small>Higher values indicate increased traffic flow</small>
                            </p>
                        `;
                    } else {
                        resultSection.className = 'result-section result-error';
                        resultContent.innerHTML = `
                            <h3 style="color: #dc3545; margin-bottom: 15px;">❌ Prediction Error</h3>
                            <p style="color: #721c24;">${result.error || 'An error occurred during prediction'}</p>
                        `;
                    }
                    
                    resultSection.style.display = 'block';
                    resultSection.scrollIntoView({ behavior: 'smooth' });
                    
                } catch (error) {
                    document.getElementById('loading').style.display = 'none';
                    
                    const resultSection = document.getElementById('resultSection');
                    const resultContent = document.getElementById('resultContent');
                    
                    resultSection.className = 'result-section result-error';
                    resultContent.innerHTML = `
                        <h3 style="color: #dc3545; margin-bottom: 15px;">❌ Connection Error</h3>
                        <p style="color: #721c24;">Failed to connect to the prediction service. Please try again.</p>
                    `;
                    
                    resultSection.style.display = 'block';
                }
            });
            
            // Initialize the form
            generateFeatureInputs();
        </script>
    </body>
    </html>
    """

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'traffic_app'}), 200

@app.route('/predict', methods=['POST'])
def predict():
    try:
        features = request.json['features']  # List of 37 features
        # ✅ Corrected to 40
        if len(features) != 40:
          return jsonify({'error': f'Expected 40 features, got {len(features)}'}), 400

        prediction = model.predict([features])[0]
        return jsonify({'prediction': float(prediction)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
